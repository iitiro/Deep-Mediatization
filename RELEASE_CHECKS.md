# Release verification

- 8 regression tests passed.
- Full notebook executed in preview mode with the bundled interview guide and survey headers; no credentials were requested.
- A synthetic interview traversed the full mocked analysis pipeline through quotation verification, Excel export, and analytical text export.
- Tests cover support-file exclusion, case-insensitive transcript extension handling, chunk-size bounds, quotation verification, structured-response parsing, explicit model selection, and clean notebook format.
- Real interview transcripts are absent; empirical findings and live model availability/quality were not independently regenerated or assessed.

## Verification environment

Checked locally on 2026-11-20 with Python 3.14.2 on macOS. Runtime and test dependency versions are recorded in `constraints.txt`. Dependency resolution was also checked for the SPPACEU requirements targeting Python 3.12; the GitHub Actions platform/version matrix has been configured but has not run as part of this local audit.

## Repeat the offline checks

```sh
python -m pip install -r requirements-dev.txt -c constraints.txt
python -m pytest -q
```

No paid API calls were made. Tests use synthetic data and mocked service responses where external inputs are required. No Git commit, release tag, push, or GitHub Release was created by this preparation.
