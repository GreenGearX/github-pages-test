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
        TranslationOrchestrator,
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
    TranslationOrchestrator,
):
    _query_params = mo.query_params()
    _api_url = _query_params['api_url']
    _api_token = _query_params['api_token']

    config = AppConfig.from_dict({
        "api_url" : _api_url, 
        "api_token" : _api_token,
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
    translation_orchestrator = TranslationOrchestrator(agent_factory, config)
    return summary_orchestrator, translation_orchestrator


@app.cell
def _(mo):
    mo.md("""
    # Wetenschap in Begrijpelijke Taal - Tool
    Met deze tool kun je van een wetenschappelijk artikel een sammenvatting in begrijpbaar Nederlands laten maken door LLMs.
    """)
    return

@app.cell
def _(mo):
    mo.md("""
    ## Instellingen
    Je kunt enkele aanpassingen maken in hoe de samenvatting wordt gemaakt. Als je niet weet of je een aanpassing wilt maken, dan zijn de huidige instellingen een goed startpunt.
    ### Aantal kandidaatsamenvattingen
    Deze tool maakt een aantal verschillende samenvattingen en kiest daarna de beste. Je krijgt dus slechts één samenvatting te zien. Meer samenvattingen genereren om uit te kiezen verhoogt de kans op een betere samenvatting, maar vergt meer tijd. Gebruik de slider hieronder om het aantal samenvattingen te kiezen.
    """)
    return

@app.cell
def _(mo):
    slider = mo.ui.slider(1, 10, value=5, show_value=True, label="Aantal kandidaten:")
    slider
    return

@app.cell
def _(mo):
    mo.md("""
    ### Gebruik
    Deze tool kan samenvattingen maken voor verschillende soorten gebruik. Kies 'beleidsvorming' voor een samenvatting die gericht is op het informeren bij het vormen van (politiek) beleid. Kies 'psychologie' voor een samenvatting die gericht is om psychologen te informeren. Kies 'algemeen' om een samenvatting te genereren die meer algemeen is dan de vorige twee keuzes. 
    """)
    return


@app.cell
def _(mo):
    context = mo.ui.dropdown(
        options={
            "algemeen": "general",
            "psycholgie": "psychology",
            "beleidsvorming" : "tweede-kamer"
        },
        value="algemeen" 
    )
    context
    return (context,)

@app.cell
def _(mo):
    mo.md("""
    ## Paper
    Klik op 'upload' om de paper waarvan je een samenvatting wilt te uploaden. Druk vervolgens op 'maak samenvatting' om de samenvatting te laten genereren.
    """)
    return


@app.cell
def _(mo):
    file_button = mo.ui.file(kind="button")
    file_button
    return (file_button,)


@app.cell
def _(file_button, mo):
    _output = None
    start_button = mo.ui.run_button(label="maak samenvatting")
    if file_button.value:
        _output = start_button

    _output
    return


@app.cell
def _(MarkItDown, PdfReader, file_button, io, mo):
    paper = None
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
            text += page.extract_text()
        _output = mo.accordion({"Paper tekst": mo.md(f"{text}")})
        paper = text

        # _output = mo.md(f"{md.convert_stream(file_stream, file_extension=".pdf", file_name=file_name)}")

    _output
    return (paper,)


@app.cell
async def _(mo, paper, summary_orchestrator, translation_orchestrator):
    _output = None
    if paper and start_button.value:
        _iterations = slider.value
        _context = context.value
        with mo.status.progress_bar(total=_iterations, title="Bezig met samenvattingen genereren", completion_title="Klaar met samenvattingen genereren") as bar:
    
            for i in range(_iterations):
                summary_result = await summary_orchestrator.run(
                    paper=paper, 
                    summary_ctx=_context, 
                    fact_ctx=_context, 
                    iterations=1
                )
                bar.update()


        summary = summary_result['summary']

        translation = await translation_orchestrator.run(
                summary=summary, 
                translation_ctx=_context
            )
        _output = mo.accordion({ "Engels": mo.md(summary), "Nederlands": mo.md(translation)})
    _output
    return


if __name__ == "__main__":
    app.run()
