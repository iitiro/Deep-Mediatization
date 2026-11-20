from pathlib import Path
from types import SimpleNamespace
import json
import pytest
from notebook_helpers import ROOT, notebook_namespace


@pytest.fixture
def ns(monkeypatch):
    monkeypatch.chdir(ROOT)
    return notebook_namespace("mediatization_kii_ai_coding_EN_FINAL.ipynb")


def test_notebook_default_preview_uses_bundled_support_files(ns):
    assert ns["RUN_ANALYSIS"] is False
    assert ns["INTERVIEW_GUIDE_PATH"].is_file()
    assert ns["SURVEY_XLSX"].is_file()
    assert len(ns["load_survey_headers"]()) > 20
    assert not any(h.lower() == "timestamp" for h in ns["load_survey_headers"]())


def test_support_files_are_not_interviews(ns, tmp_path):
    (tmp_path / "Interview Guide.txt").write_text("guide")
    (tmp_path / "example.TXT").write_text("transcript")
    (tmp_path / "KII_list.txt").write_text("directory")
    ns["INTERVIEW_GUIDE_PATH"] = tmp_path / "Interview Guide.txt"
    ns["KII_LIST_PATH"] = tmp_path / "KII_list.txt"
    assert ns["discover_transcripts"](tmp_path) == [tmp_path / "example.TXT"]


def test_quotes_must_exist_in_source(ns):
    assert ns["verify_quote"]("Verified   quotation", "A Verified quotation appears here.")
    assert not ns["verify_quote"]("invented words", "A Verified quotation appears here.")


def test_long_units_are_bounded(ns):
    units = [{"unit_type": "raw", "index": 1, "label": "RAW", "text": "example " * 1000}]
    chunks = ns["chunk_units"](units, max_chars=500)
    assert len(chunks) > 1
    assert all(sum(len(ns["render_unit"](unit)) for unit in chunk) <= 500 for chunk in chunks)
    assert all(chunk for chunk in chunks)


def test_structured_response_parsing_without_api(ns):
    ns["SLEEP_BETWEEN_REQUESTS"] = 0
    class Responses:
        def create(self, **kwargs):
            assert kwargs["store"] is False
            assert kwargs["text"]["format"]["strict"] is True
            return SimpleNamespace(status="completed", output_text=json.dumps({"value": "example"}), usage=None, id="mock")
    result = ns["call_structured"](SimpleNamespace(responses=Responses()), model="mock", instructions="test", input_text="example", schema={"type": "object"}, schema_name="test", max_output_tokens=50, stage="test", transcript_id="synthetic")
    assert result == {"value": "example"}


def test_pipeline_requires_explicit_models(ns, monkeypatch):
    ns["CODING_MODEL"] = ns["SYNTHESIS_MODEL"] = ""
    with pytest.raises(ValueError, match="OPENAI_MODEL"):
        ns["run_pipeline"]()


def test_mocked_full_pipeline_verifies_evidence_and_exports(ns, tmp_path, monkeypatch):
    import pandas as pd
    transcripts = tmp_path / "transcripts"
    transcripts.mkdir()
    (transcripts / "synthetic_interview.txt").write_text("Speaker A: How do digital tools affect your work?\nSpeaker B: Digital tools help me prepare performances.")
    ns.update(INPUT_DIR=transcripts, OUTPUT_DIR=tmp_path / "out", CACHE_DIR=tmp_path / "cache", RESULT_XLSX=tmp_path / "out" / "analysis.xlsx", ARTICLE_MEMO_MD=tmp_path / "out" / "memo.md", CODING_MODEL="mock", SYNTHESIS_MODEL="mock", SLEEP_BETWEEN_REQUESTS=0)
    monkeypatch.setenv("OPENAI_API_KEY", "test-credential")
    def populate(schema):
        if "enum" in schema:
            return schema["enum"][0]
        kind = schema.get("type")
        if kind == "object":
            return {key: populate(value) for key, value in schema["properties"].items()}
        if kind == "array":
            return []
        if kind == "integer":
            return schema.get("minimum", 1)
        if kind == "number":
            return 1.0
        if kind == "boolean":
            return True
        return "Synthetic test output"
    class Responses:
        def create(self, **kwargs):
            fmt = kwargs["text"]["format"]
            result = populate(fmt["schema"])
            if fmt["name"] == "interview_structure":
                result.update(interviewer_label="Speaker A", expert_label="Speaker B", respondent_name_from_text="Synthetic expert", sector="theatre")
            elif fmt["name"] == "coded_interview_chunk":
                item = populate(ns["EVIDENCE_ITEM_SCHEMA"])
                item["quote"] = "Digital tools help me prepare performances."
                result["evidence"] = [item]
            return SimpleNamespace(status="completed", output_text=json.dumps(result), usage=None, id="mock")
    ns["OpenAI"] = lambda **kwargs: SimpleNamespace(responses=Responses())
    workbook, memo = ns["run_pipeline"]()
    assert workbook.is_file() and memo.is_file()
    evidence = pd.read_excel(workbook, sheet_name="Coded_evidence")
    assert len(evidence) == 1
    assert evidence["quote_verified"].all()
    assert pd.read_excel(workbook, sheet_name="Run_log")["status"].eq("ok").all()


def test_published_notebooks_are_clean_and_valid():
    import nbformat
    from notebook_helpers import ROOT
    for path in ROOT.glob("*.ipynb"):
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                assert not cell.outputs
                assert cell.execution_count is None
