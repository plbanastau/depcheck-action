# depcheck-action

> GitHub Action that audits outdated dependencies and opens PRs with upgrade suggestions.

---

## Installation

```bash
pip install depcheck-action
```

Or install from source:

```bash
pip install git+https://github.com/your-org/depcheck-action.git
```

---

## Usage

Add the following workflow to your repository at `.github/workflows/depcheck.yml`:

```yaml
name: Dependency Audit

on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:

jobs:
  depcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run depcheck-action
        uses: your-org/depcheck-action@v1
        with:
          package-manager: pip
          auto-pr: true
          branch-prefix: "deps/upgrade"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Input              | Description                              | Default  |
|--------------------|------------------------------------------|----------|
| `package-manager`  | Package manager to audit (`pip`, `npm`)  | `pip`    |
| `auto-pr`          | Automatically open upgrade PRs           | `true`   |
| `branch-prefix`    | Prefix for created branches              | `deps/`  |

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss any major changes.

---

## License

[MIT](LICENSE) © your-org