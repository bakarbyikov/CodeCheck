from pathlib import Path
from loguru import logger
import typer
from typing_extensions import Annotated

from codecheck.model.model import Model
from codecheck.dataset.tester import Problem, Test

app = typer.Typer()


@app.command()
def new(
    path: Annotated[Path, typer.Argument(
        resolve_path=True,
    )],
    text: Annotated[str, typer.Option(prompt=True)]
):
    Problem.create(path, text)


@app.command()
def solve(
    path: Annotated[Path, typer.Argument(
        resolve_path=True,
    )],
):
    problem = Problem.open(path)
    solution = Model().create_solution(problem.text)
    logger.info(solution)
    (path/"solution.py").write_text(solution)


@app.command()
def audit(
    path: Annotated[Path, typer.Argument(
        resolve_path=True,
    )],
):
    problem = Problem.open(path)
    tests = Model().create_tests(problem.text)
    logger.info(*tests, sep='\n')
    Test.write(tests, path)


@app.command()
def check(
    path: Annotated[Path, typer.Argument(
        resolve_path=True,
    )],
):
    problem = Problem.open(path)
    logger.info(problem.self_check())

def main():
    Problem("Oleg", "Hello").create(Path.cwd())
