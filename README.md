# Deep Mediatization

Investigate how platforms and AI reshape performing and screen arts through expert-interview coding and cross-case synthesis.

## Research focus

A qualitative research workflow for studying deep mediatization and AI-driven change in creative production, professional roles, and cultural visibility. The notebook is designed around 11 expert interviews and thematic alignment with a separate survey.

## Repository contents

- `mediatization_kii_ai_coding_EN_FINAL.ipynb` — speaker-role identification, deductive and emergent coding, quotation verification, within-case synthesis, and cross-case analysis.
- `Interview Guide.txt` — interview guide.
- `survey_FINAL.xlsx` — survey workbook.
- `mediatization_kii_analysis_FINAL.xlsx` — analysis workbook.

## Use the notebook

Open the notebook in a Python/Jupyter environment and install its imported dependencies, including `pandas`, `openpyxl`, and `openai`. Supply interview transcripts as `.txt` files; these are not included in the repository.

Update `INPUT_DIR`, `INTERVIEW_GUIDE_PATH`, and `SURVEY_XLSX` to match your files. The configured filenames differ from the filenames included here. Set `RUN_ANALYSIS = False` while reviewing the configuration and preview, then enable execution when ready. The checked-in notebook currently sets this flag to `True`.

Configure an OpenAI API key through the notebook's credential flow. Executing the analysis makes paid API requests and exports analytical tables and text.

## Evidence and interpretation

The workflow checks coded quotations against source transcripts, preserves original-language excerpts, and tracks dissenting cases. AI-generated coding requires researcher review. Interview findings support qualitative interpretations rather than population prevalence estimates.

## License

[MIT](LICENSE).
