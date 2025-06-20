# Developer Contributing Notes

This section supplements the main [CONTRIBUTING.md](https://github.com/adrianwedd/Agentic-Index/blob/main/CONTRIBUTING.md).

## Regenerating Fixtures

Tests rely on a snapshot of the README stored in `tests/fixtures/README_fixture.md`.
Whenever `scripts/inject_readme.py` changes or you update the ranking data,
regenerate the fixture so it stays in sync:

```bash
make regen-fixtures
```

The command rebuilds `README.md` and copies the result into the fixture file.
Pre-commit and CI will fail if the snapshot drifts.

README tables are injected automatically by CI once per day. You can trigger an
immediate update via GitHub:

1. Navigate to **Actions** → **Daily README Injection**.
2. Click **Run workflow** and set `force` to `true`.

## Editable Install

After cloning the repository, install the CLI in editable mode so the
`agentic-index` command is available on your path:

```bash
pip install -e .
```
