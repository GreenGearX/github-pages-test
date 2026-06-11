import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
async def _():
    import marimo as mo
    import micropip
    import io

    await micropip.install("markitdown-no-magika[pdf]")
    await micropip.install("pypdf")

    await micropip.install("https://raw.githubusercontent.com/ubvu/wibt-tool/refs/heads/refactor/dist/wibt_tool-0.1.0-py3-none-any.whl")



    from wibt_tool.config import AppConfig

    from wibt_tool.utils.openai_client import OpenAIClient
    from wibt_tool.prompt_manager import PromptManager
    from wibt_tool.agent_factory import AgentFactory

    from wibt_tool.pipelines.summary_pipeline import SummaryOrchestrator
    from wibt_tool.pipelines.translation_pipeline import TranslationOrchestrator


    from markitdown_no_magika import MarkItDown
    from pypdf import PdfReader

    return (
        AgentFactory,
        AppConfig,
        MarkItDown,
        OpenAIClient,
        PdfReader,
        PromptManager,
        SummaryOrchestrator,
        io,
        mo,
    )


@app.cell
def _(
    AgentFactory,
    AppConfig,
    OpenAIClient,
    PromptManager,
    SummaryOrchestrator,
):
    config = AppConfig.from_dict({
        "api_url" : "https://nebula.cs.vu.nl/api/v1", 
        "api_token" : "sk-a2ad1d4c2b4244448cefdc93fec50be1",
        "MODEL": "gpt-oss-120b-120k",
        "MODEL_TEMP": 0,
        "SUMMARY_MODEL": "gemma3-12b-120k",
        "SUMMARY_MODEL_TEMP": 0.5,
        "READ_EVAL_MODEL": "gpt-oss-120b-120k",
        "READ_EVAL_MODEL_TEMP": 0,
        "REFINEMENT_MODEL": "gpt-oss-120b-120k",
        "REFINEMENT_MODEL_TEMP": 1,
        "PREDRAFT_MODEL": "gpt-oss-120b-120k",
        "PREDRAFT_MODEL_TEMP": 0,
        "DRAFT_MODEL": "gemma3-12b-120k",
        "DRAFT_MODEL_TEMP": 0,
        "REFINE_DRAFT_MODEL": "gemma3-12b-120k",
        "REFINE_DRAFT_MODEL_TEMP": 0,
        "PROOFREAD_MODEL": "gemma3-12b-120k",
        "PROOFREAD_MODEL_TEMP": 0,
        "DIRECT_TRANSLATION_MODEL": "translategemma:12b",
        "DIRECT_TRANSLATION_TEMP": 0,
        "FACT_EXTRACTION_MODEL": "gpt-oss-120b-120k",
        "FACT_EXTRACTION_MODEL_TEMP": 0,
        "FACT_VALIDATION_MODEL": "gpt-oss-120b-120k,gemma3-12b-120k,gemma3-12b-120k",
        "FACT_VALIDATION_MODEL_TEMP": "0.5,0.5,0.5",
        "ALIGNMENT_MODEL": "gpt-oss-120b-120k",
        "ALIGNMENT_MODEL_TEMP": 0,
        "ADVOCATE_MODEL": "gpt-oss-120b-120k",
        "ADVOCATE_MODEL_TEMP": 0,
        "SKEPTIC_MODEL": "gpt-oss-120b-120k",
        "SKEPTIC_MODEL_TEMP": 0,
        "ADJUDICATOR_MODEL": "gpt-oss-120b-120k",
        "ADJUDICATOR_MODEL_TEMP": 0,
        "CONTEXT": "general"
    }
    )

    llm_endpoint = OpenAIClient(token=config.api_token, endpoint=config.api_url)

    prompt_manager = PromptManager(config=config)

    agent_factory = AgentFactory(config=config, prompt_manager=prompt_manager, llm_endpoint=llm_endpoint)

    summary_orchestrator = SummaryOrchestrator(agent_factory, prompt_manager, config, "static", False)

    summary_result = summary_orchestrator.run(
        paper="paper", 
        summary_ctx="general", 
        fact_ctx="general", 
        iterations=1
    )
    return


@app.cell
def _(mo):
    mo.md("""
    # Title
    """)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 22)
    slider
    return


@app.cell
def _(mo):
    file_button = mo.ui.file(kind="button")
    file_button
    return (file_button,)


@app.cell
def _(file_button, mo):
    _output = None
    if file_button.value:
        _output = mo.md(f"Button upload: {file_button.name()}")

    _output
    return


@app.cell
def _(MarkItDown, PdfReader, file_button, io, mo):

    md = MarkItDown()
    _output = None
    if file_button.value:
        uploaded_file = file_button.value[0]
        file_bytes = uploaded_file.contents
        file_name = uploaded_file.name
        file_stream = io.BytesIO(file_bytes)

        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
        # page = reader.pages[0]
            text += page.extract_text()
        _output = mo.md(f"{text}")

        # _output = mo.md(f"{md.convert_stream(file_stream, file_extension=".pdf", file_name=file_name)}")

    _output
    return


if __name__ == "__main__":
    app.run()
