"""CLI/concurrency regression tests. State and subprocesses are isolated."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).with_name("claims.py")


class ClaimsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="modding-claims-test-")
        self.addCleanup(self.temp.cleanup)
        self.state = Path(self.temp.name) / "state"

    def command(self, *args):
        return [sys.executable, "-B", str(SCRIPT), *args, "--state-dir", str(self.state)]

    def run_cli(self, *args, code=0):
        result = subprocess.run(self.command(*args), capture_output=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout or result.stderr)

    def claim(self, owner="agent-a", *resources, code=0):
        return self.run_cli("claim", "--owner", owner, "--task", "isolated test",
                            "--resources", *(resources or ("module:example",)), code=code)

    def test_status_is_read_only(self):
        self.assertEqual(self.run_cli("status")["claims"], {})
        self.assertFalse(self.state.exists())

    def test_claim_check_release_and_idempotence(self):
        first = self.claim("agent-a", "Module:Example", "Docs")
        self.assertEqual(first, self.claim("agent-a", "module:example", "docs"))
        self.run_cli("check", "--owner", "agent-a", "--resources", "DOCS", "module:example")
        data = self.run_cli("release", "--owner", "agent-a", "--resources", "docs", "module:example")
        self.assertEqual(data["claims"], {})
        self.assertEqual(data["revision"], 2)

    def test_batch_conflict_never_partially_claims(self):
        baseline = self.claim("agent-a", "docs")
        self.claim("agent-b", "module:free", "docs", code=3)
        current = self.run_cli("status")
        self.assertEqual(current["claims"], baseline["claims"])
        self.assertEqual(current["revision"], baseline["revision"])

    def test_release_and_check_wrong_owner_fail_atomically(self):
        self.claim("agent-a", "module:a")
        self.claim("agent-b", "module:b")
        baseline = (self.state / "claims.json").read_bytes()
        for command in ("check", "release"):
            self.run_cli(command, "--owner", "agent-a", "--resources", "module:a", "module:b", code=3)
        self.assertEqual((self.state / "claims.json").read_bytes(), baseline)

    def test_layout_is_global_in_both_directions(self):
        self.claim("agent-a", "module:a")
        self.claim("agent-b", "layout", code=3)
        self.claim("agent-a", "layout")
        self.claim("agent-b", "module:b", code=3)

    def test_handoff_is_atomic(self):
        self.claim("agent-a", "docs", "module:a")
        data = self.run_cli("handoff", "--owner", "agent-a", "--to-owner", "agent-b",
                            "--task", "agreed handoff", "--resources", "docs", "module:a")
        self.assertTrue(all(c["owner"] == "agent-b" for c in data["claims"].values()))
        self.run_cli("check", "--owner", "agent-a", "--resources", "docs", code=3)

    def test_handoff_cannot_split_layout(self):
        self.claim("agent-a", "layout", "module:a")
        for resource in ("layout", "module:a"):
            self.run_cli("handoff", "--owner", "agent-a", "--to-owner", "agent-b",
                         "--task", "partial", "--resources", resource, code=3)
        self.run_cli("handoff", "--owner", "agent-a", "--to-owner", "agent-b",
                     "--task", "complete", "--resources", "layout", "module:a")

    def test_corrupt_and_duplicate_state_are_preserved(self):
        self.state.mkdir()
        for content in ('{broken', '{"schema":1,"schema":1,"revision":0,"claims":{}}',
                        '{"schema":1,"revision":false,"claims":{}}'):
            (self.state / "claims.json").write_text(content, encoding="utf-8")
            self.claim(code=4)
            self.assertEqual((self.state / "claims.json").read_text(encoding="utf-8"), content)
            self.assertFalse((self.state / ".transaction").exists())

    def test_stale_transaction_is_not_stolen(self):
        lock = self.state / ".transaction"
        lock.mkdir(parents=True)
        (lock / "process.json").write_text('{"pid":0,"started_at":"old"}', encoding="utf-8")
        self.run_cli("claim", "--owner", "agent-a", "--task", "test", "--resources", "docs",
                     "--wait-seconds", "0", code=5)
        self.assertTrue(lock.exists())
        self.assertFalse((self.state / "claims.json").exists())

    def test_claims_do_not_expire_with_age(self):
        self.claim("agent-a", "docs")
        path = self.state / "claims.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["claims"]["docs"]["claimed_at"] = "1900-01-01T00:00:00+00:00"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.claim("agent-b", "docs", code=3)

    def test_killed_transaction_preserves_committed_claims_and_blocks_new_writers(self):
        self.claim("agent-a", "docs")
        baseline = (self.state / "claims.json").read_bytes()
        ready = Path(self.temp.name) / "ready"
        code = """
import importlib.util, sys, time
from pathlib import Path
spec = importlib.util.spec_from_file_location('claims', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with module.guard(Path(sys.argv[2]), 1):
    Path(sys.argv[3]).write_text('ready', encoding='utf-8')
    time.sleep(30)
"""
        process = subprocess.Popen([sys.executable, "-B", "-c", code, str(SCRIPT), str(self.state), str(ready)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(self.stop_process, process)
        deadline = time.monotonic() + 10
        while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.02)
        self.assertTrue(ready.exists(), 'Child did not acquire the isolated transaction')
        process.kill()
        process.communicate(timeout=10)
        self.run_cli("claim", "--owner", "agent-b", "--task", "after interruption",
                     "--resources", "module:b", "--wait-seconds", "0", code=5)
        self.assertEqual((self.state / "claims.json").read_bytes(), baseline)
        self.assertTrue((self.state / ".transaction").exists())

    def spawn(self, owner, *resources):
        process = subprocess.Popen(self.command("claim", "--owner", owner, "--task", "concurrent test",
                                                "--resources", *resources),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        self.addCleanup(self.stop_process, process)
        return process

    @staticmethod
    def stop_process(process):
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=10)

    def test_concurrent_shared_claim_has_one_winner_and_no_partial_claims(self):
        processes = [self.spawn(f"agent-{i}", "shared", f"module:{i}") for i in range(8)]
        for process in processes:
            process.communicate(timeout=15)
        self.assertEqual(sorted(p.returncode for p in processes), [0] + [3] * 7)
        data = self.run_cli("status")
        self.assertEqual(len(data["claims"]), 2)
        self.assertEqual(data["revision"], 1)
        self.assertIsNone(data["transaction"])

    def test_concurrent_disjoint_claims_preserve_every_writer(self):
        processes = [self.spawn(f"agent-{i}", f"module:{i}") for i in range(8)]
        for process in processes:
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, stdout + stderr)
        data = self.run_cli("status")
        self.assertEqual(len(data["claims"]), 8)
        self.assertEqual(data["revision"], 8)


if __name__ == "__main__":
    unittest.main()
