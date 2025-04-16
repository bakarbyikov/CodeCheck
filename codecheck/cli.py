import typer

app = typer.Typer()


@app.command()
def model():
    from .model import main
    main()


@app.command()
def tester():
    from .tester import main
    main()


def main():
    app()
