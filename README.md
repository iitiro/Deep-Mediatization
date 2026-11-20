# Deep Mediatization

Investigate how platforms and AI reshape performing and screen arts through expert-interview coding and cross-case synthesis.

## Research materials

The workflow is designed around 11 expert interviews and thematic alignment with a separate survey.

- `mediatization_kii_ai_coding_EN_FINAL.ipynb` — role identification, deductive and emergent coding, quotation verification, interview synthesis, cross-case analysis, and export.
- `Interview Guide.txt` — the included interview guide.
- `survey_FINAL.xlsx` — the included survey workbook; the `base` sheet supplies question headers for alignment.
- `mediatization_kii_analysis_FINAL.xlsx` — a previously exported research analysis, retained as a reference artifact. Rerunning the notebook writes a new file under `outputs/`.

Original interview transcripts are **not included**, so the published analysis cannot be independently regenerated from this archive alone.

## Setup

Python 3.12 or newer is recommended. Run these commands from the repository directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -c constraints.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.
`constraints.txt` records the dependency versions used for the local release checks.

## Preview the notebook

```sh
jupyter lab mediatization_kii_ai_coding_EN_FINAL.ipynb
```

Open it from the repository directory and run all cells. `RUN_ANALYSIS = False` is the default: preview loads the included support files and reports the available transcripts without requesting credentials or calling an API.

## Run on interview transcripts

1. Put UTF-8 `.txt` transcripts in `data/transcripts/`, or set `MEDIATIZATION_INPUT_DIR` to another directory.
2. Optionally add `data/KII_list.txt` with expert metadata in the format described in the notebook. Interviewer/expert identification supports speaker-labeled and numbered Q&A transcripts.
3. Set `OPENAI_API_KEY` and `OPENAI_MODEL`. Select a Responses API model supporting strict JSON-schema output. Separate `OPENAI_CODING_MODEL` and `OPENAI_SYNTHESIS_MODEL` values override `OPENAI_MODEL` for each stage.
4. Review the preview and configuration, then set `RUN_ANALYSIS = True` and rerun from the configuration cell.

Live execution sends interview content to OpenAI and incurs API charges. No model is silently selected for you. Credentials are read from the environment and are never embedded in the notebook.

Generated workbooks, analytical text, and caches go under `outputs/`; `MEDIATIZATION_OUTPUT_DIR` can override that path. Support-file paths refer to the included filenames. Large transcript units are split to respect the chunk limit; cache identifiers include model selection and the codebook.

## Evidence and interpretation

Coded quotations are checked against source chunks, original-language excerpts are retained, and dissenting cases are preserved. Analytical text and emergent-code labels are requested in English. Researcher review is required for speaker attribution, coding, interpretation, and any translated quotations. Interview findings support qualitative interpretation rather than population prevalence estimates.

## Offline checks

```sh
python -m pip install -r requirements-dev.txt -c constraints.txt
python -m pytest -q
```

The test suite does not require API credentials. GitHub Actions is configured to repeat these checks on Python 3.12, 3.13, and 3.14 after push.

## License

[MIT](LICENSE).
