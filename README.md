# hivemind-ladder-demo

A small public sample project. The Hivemind AX mission ladder uses it as the code under review for
two of its levels:

- **Level 5** asks for the five most recently merged pull requests of this repository.
- **Level 6** asks an audit to check documented controls against source code, and this repository
  is the code it reads.

This is **not** Hivemind AX source code. It is a deliberately small, self-contained Python package
with tests, written so that its history and its code are safe to read with a token that can only
read public repositories.

## Layout

- `src/approvals/` — the package
- `tests/` — standard-library `unittest` tests

## What the package does

- **Audit log** (`src/approvals/audit_log.py`): an append-only log whose entries are linked by a
  SHA-256 hash chain. `verify()` returns the first altered entry, and `append()` refuses to extend
  a chain that no longer verifies.
- **Approval gate** (`src/approvals/gate.py`): actions below a risk threshold run and are logged;
  actions at or above it wait for a reviewer, who cannot be the requester. The decision records
  who decided and when.
- **Retention sweep** (`src/approvals/retention.py`): removes working records older than a limit.
  Audit entries are not working records, so the sweep cannot remove them.

## Running the tests

```
python -m unittest discover -s tests
```

## License

MIT, see `LICENSE`.
