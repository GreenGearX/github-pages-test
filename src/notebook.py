import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


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
def _():
    return


if __name__ == "__main__":
    app.run()
