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

## Running the tests

```
python -m unittest discover -s tests
```

## License

MIT, see `LICENSE`.
