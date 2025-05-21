import csv
from csv import DictReader
from enum import Enum
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired
from tempfile import NamedTemporaryFile
from typing import Self

from contexttimer import Timer
from loguru import logger
from pydantic import BaseModel


class Test(BaseModel):
    input: str
    expected: str

    @classmethod
    def read(cls, path: Path) -> list[Self]:
        try:
            text = path.read_text()
        except FileNotFoundError:
            return list()
        reader = DictReader(text.splitlines() or list())
        return [cls.model_validate(row) for row in reader]

    @classmethod
    def write(cls, tests: list[Self], path: Path):
        with (path/"test.csv").open('w') as file:
            writer = csv.writer(file)
            writer.writerow(("input", "expected"))
            writer.writerows(((test.input, test.expected)
                              for test in tests))


class Status(Enum):
    Passed = 'Passed'
    Failed = 'Failed'
    Error = 'Error'


class Result(BaseModel):
    status: Status
    message: str

    @classmethod
    def error(cls, error: str) -> Self:
        return cls(status=Status.Error, message=f"Error:\n{error}")

    @classmethod
    def failed(cls, expected: str, got: str) -> Self:
        return cls(status=Status.Failed, message=f"Fail: {expected=} {got=}")

    @classmethod
    def passed(cls) -> Self:
        return cls(status=Status.Passed, message=f"OK!")


def test(solution: str, tests: list[Test]) -> list[Result]:
    with Timer(output=logger.trace, fmt="Tested in {:.3f} seconds"):
        with NamedTemporaryFile(mode='w') as script:
            print(solution, file=script, flush=True)
            return [
                run(script.name, test)
                for test in tests
            ]


def run(script: str, test: Test) -> Result:
    child = Popen(
        ['python3', script],
        stdin=PIPE, stdout=PIPE, stderr=PIPE,
        text=True,
    )
    try:
        got, error = map(str.strip, child.communicate(test.input, 10))
    except TimeoutExpired:
        child.kill()
        return Result.error("TimeOut")
    if error:
        return Result.error(error)
    if got != test.expected:
        return Result.failed(test.expected, got)
    return Result.passed()
