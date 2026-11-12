# Contributing

Thanks for helping make document extraction more reliable and accessible.

## Good first contributions
- Arabic and mixed-script normalization tests.
- Synthetic invoice/receipt fixtures.
- OCR adapter implementations.
- Locale-aware date and decimal parsing.
- Validation rules with references and tests.
- Documentation and reproducible benchmark scripts.

## Before opening a PR
1. Open or find an issue describing the change.
2. Keep changes focused.
3. Add tests for new behavior and bug fixes.
4. Run the test suite and lint checks.
5. Update docs where relevant.
6. Never add real invoices, personal data, secrets or unlicensed datasets.

## Dataset contributions

Include provenance, license, permitted use, attribution requirements and annotation format. A public URL does not automatically permit redistribution.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

Pull requests should explain the problem, approach, tests, compatibility impact and license implications.
