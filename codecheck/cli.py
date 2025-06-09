from importlib import import_module

import typer

from codecheck.misc import enable_trace
from codecheck.dataset.cli import app as dataset

app = typer.Typer()
app.add_typer(dataset, name="dataset")

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
    enable_trace()
    app()
