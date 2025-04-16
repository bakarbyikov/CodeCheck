from importlib import import_module

import typer

app = typer.Typer()

@app.command()
def run(folder: str, file: str):
    name = folder.replace("/", ".") + "." + file
    module = import_module(name, "codecheck")
    module.main()

@app.command()
def serve():
    from .api import endpoint
    endpoint.main()

def main():
    app()
