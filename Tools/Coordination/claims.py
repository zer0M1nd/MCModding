"""Persistent cooperative writer claims. Python 3.10+, standard library only.

Advisory local-filesystem protocol, not access control. No automatic expiry.
See Docs/Coordination/TOOLS.md. Never use separate state directories for peers.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
import uuid

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,119}\Z")
DEFAULT_STATE = Path(__file__).resolve().parents[2] / ".coord"


class ClaimError(Exception):
    def __init__(self, message: str, code: int = 4):
        super().__init__(message)
        self.code = code


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_state(path: Path) -> dict:
    if not path.exists():
        return {"schema": 1, "revision": 0, "claims": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
    except (ValueError, UnicodeError) as exc:
        raise ClaimError(f"Invalid state; refusing to reset or overwrite: {exc}") from exc
    if not isinstance(data, dict) or type(data.get("schema")) is not int or data["schema"] != 1:
        raise ClaimError("Unsupported or missing schema; explicit migration required")
    if type(data.get("revision")) is not int or data["revision"] < 0:
        raise ClaimError("Invalid revision")
    if not isinstance(data.get("claims"), dict):
        raise ClaimError("Invalid claims table")
    for resource, claim in data["claims"].items():
        if not NAME.fullmatch(resource) or resource != resource.casefold():
            raise ClaimError(f"Invalid or non-canonical resource: {resource}")
        if not isinstance(claim, dict):
            raise ClaimError(f"Invalid claim for {resource}")
        if not isinstance(claim.get("owner"), str) or not NAME.fullmatch(claim["owner"]):
            raise ClaimError(f"Invalid owner for {resource}")
        if not isinstance(claim.get("task"), str) or not claim["task"].strip():
            raise ClaimError(f"Missing task for {resource}")
        if not isinstance(claim.get("claimed_at"), str) or not claim["claimed_at"]:
            raise ClaimError(f"Missing claim time for {resource}")
    claims = data["claims"]
    if "layout" in claims and any(c["owner"] != claims["layout"]["owner"] for c in claims.values()):
        raise ClaimError("Invalid state: Layout conflicts with another owner")
    return data


def transaction_info(directory: Path):
    lock = directory / ".transaction"
    if not lock.exists():
        return None
    try:
        return json.loads((lock / "process.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return {"state": "initializing-or-incomplete", "path": str(lock)}


@contextmanager
def guard(directory: Path, wait_seconds: float):
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / ".transaction"
    deadline = time.monotonic() + wait_seconds
    while True:
        try:
            lock.mkdir()
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise ClaimError("Transaction busy; inspect metadata and process identity. No automatic recovery.", 5)
            time.sleep(min(0.05, max(0, deadline - time.monotonic())))
    try:
        metadata = {"id": uuid.uuid4().hex, "pid": os.getpid(), "started_at": now()}
        with (lock / "process.json").open("x", encoding="utf-8") as stream:
            json.dump(metadata, stream)
            stream.flush()
            os.fsync(stream.fileno())
        yield
    finally:
        # Only remove our own transaction files; no recursive deletion.
        (lock / "process.json").unlink(missing_ok=True)
        lock.rmdir()


def save_state(path: Path, data: dict):
    temporary = path.parent / (".pending-" + uuid.uuid4().hex + ".json")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def emit(value: dict, *, error: bool = False):
    print(json.dumps(value, ensure_ascii=False, indent=2), file=sys.stderr if error else sys.stdout)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["status", "claim", "check", "release", "handoff"])
    parser.add_argument("--owner", help="Unique session identifier; never impersonate another owner")
    parser.add_argument("--task", help="Brief non-secret purpose; required for claim and handoff")
    parser.add_argument("--resources", nargs="+", default=[])
    parser.add_argument("--to-owner", help="Previously agreed recipient for handoff")
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--wait-seconds", type=float, default=5.0)
    args = parser.parse_args(argv)
    if not 0 <= args.wait_seconds <= 60:
        parser.error("--wait-seconds must be between 0 and 60")
    if args.command != "status":
        if not args.owner or not NAME.fullmatch(args.owner) or not args.resources:
            parser.error("Valid --owner and nonempty --resources are required")
        if any(not NAME.fullmatch(resource) for resource in args.resources):
            parser.error("Resource names must be short ASCII identifiers, not file paths")
    if args.command in {"claim", "handoff"} and (not args.task or not args.task.strip()):
        parser.error("--task is required for claim and handoff")
    if args.command == "handoff":
        if not args.to_owner or not NAME.fullmatch(args.to_owner) or args.to_owner == args.owner:
            parser.error("handoff requires a distinct valid --to-owner")
    elif args.to_owner:
        parser.error("--to-owner applies only to handoff")
    resources = sorted({resource.casefold() for resource in args.resources})
    path = args.state_dir / "claims.json"

    def ensure_owned(claims):
        missing = [r for r in resources if r not in claims or claims[r]["owner"] != args.owner]
        if missing:
            raise ClaimError("Not owned by this session: " + ", ".join(missing), 3)

    if args.command == "status":
        emit({**read_state(path), "transaction": transaction_info(args.state_dir)})
        return 0
    if args.command == "check":
        data = read_state(path)
        ensure_owned(data["claims"])
        emit(data)
        return 0

    with guard(args.state_dir, args.wait_seconds):
        data = read_state(path)
        claims = data["claims"]
        changed = False
        if args.command == "claim":
            conflicts = {r: c for r, c in claims.items() if c["owner"] != args.owner
                         and (r in resources or r == "layout" or "layout" in resources)}
            if conflicts:
                raise ClaimError("Conflicting claims: " + json.dumps(conflicts, ensure_ascii=False), 3)
            for resource in resources:
                if resource not in claims:
                    claims[resource] = {"owner": args.owner, "task": args.task, "claimed_at": now()}
                    changed = True
        else:
            ensure_owned(claims)
            if args.command == "release":
                for resource in resources:
                    del claims[resource]
            else:
                projected = {r: (args.to_owner if r in resources else c["owner"]) for r, c in claims.items()}
                if "layout" in projected and any(owner != projected["layout"] for owner in projected.values()):
                    raise ClaimError("Handoff would split Layout; transfer all held resources together", 3)
                for resource in resources:
                    claims[resource] = {"owner": args.to_owner, "task": args.task, "claimed_at": now(),
                                        "transferred_from": args.owner}
            changed = True
        if changed:
            data["revision"] += 1
            data["last_change"] = {"command": args.command, "owner": args.owner, "resources": resources, "at": now()}
            save_state(path, data)
    emit(data)
    return 0


if __name__ == "__main__":
    for output in (sys.stdout, sys.stderr):
        if hasattr(output, "reconfigure"):
            output.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except ClaimError as exc:
        emit({"error": str(exc), "code": exc.code}, error=True)
        sys.exit(exc.code)
    except OSError as exc:
        emit({"error": str(exc), "code": 1}, error=True)
        sys.exit(1)
