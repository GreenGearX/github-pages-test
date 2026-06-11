import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
async def _():
    import marimo as mo
    import micropip
    import io

    await micropip.install("markitdown-no-magika[pdf]")

    from markitdown_no_magika import MarkItDown

    return MarkItDown, io, mo


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
def _(MarkItDown, file_button, io, mo):
    # Simple instantiation, clear intent

    md = MarkItDown()
    _output = None
    if file_button.value:
        uploaded_file = file_button.value[0]
        file_bytes = uploaded_file.contents
        file_name = uploaded_file.name
        file_stream = io.BytesIO(file_bytes)

        _output = mo.md(f"{md.convert_stream(file_stream, file_name=file_name)}")

    _output
    return


if __name__ == "__main__":
    app.run()
