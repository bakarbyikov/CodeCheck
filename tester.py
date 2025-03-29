from collections import Counter
from csv import DictReader
from enum import Enum, auto
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile
from typing import Self

from loguru import logger
from pydantic.dataclasses import dataclass

import misc


class SolutionError(Exception):
    pass


class Status(Enum):
    Passed = auto()
    Failed = auto()
    Error = auto()


@dataclass
class Result:
    status: Status
    info: str


class Report(Counter):
    def __str__(self):
        names = "/".join(s.name for s in Status)
        values = "/".join(str(self[s]) for s in Status)
        return f"{names}: {values}"


@dataclass
class Test:
    index: int
    input: str
    expected: str
    required: bool

    @classmethod
    def from_file(cls, path: Path) -> list[Self]:
        with path.open() as file:
            reader = DictReader(file)
            return [cls(index=i, **row) for i, row in enumerate(reader)]

    def run(self, solution: str) -> Result:
        result = self._run(solution)
        i, expected, got = self.index, self.expected, result.info
        match result.status:
            case Status.Passed:
                logger.trace(f"Test #{i} passed {expected=} {got=}")
            case Status.Failed:
                logger.trace(f"Test #{i} failed {expected=} {got=}")
            case Status.Error:
                logger.trace(f"Test #{i} error: {got}")
        return result

    def _run(self, solution: str) -> Result:
        with NamedTemporaryFile(mode='w') as script:
            print(solution, file=script, flush=True)

            child = Popen(['python3', script.name],
                          stdin=PIPE, stdout=PIPE, stderr=PIPE,
                          text=True, )
            got, stderr = map(str.strip, child.communicate(self.input))

        if stderr:
            return Result(Status.Error, stderr)
        if got != self.expected:
            return Result(Status.Failed, got)
        return Result(Status.Passed, got)


@dataclass
class Problem:
    name: str
    text: str
    tests: list[Test]
    path: str

    @classmethod
    def from_folder(cls, folder: str) -> dict[str, Self]:
        found = dict()
        for root, dirs, files in Path(folder).walk():
            if not files:
                continue

            try:
                problem = cls.open(root)
            except FileNotFoundError:
                continue

            if problem.name in found:
                logger.warning(f"Problem {problem.name=} is not unique")
                continue

            found[problem.name] = problem
        return found

    @classmethod
    def open(cls, path: Path) -> Self:
        try:
            tests = Test.from_file(path/"test.csv")
        except FileNotFoundError:
            logger.warning(f"Can't find tests in {path}")
            raise

        try:
            text = (path/"text.md").read_text()
        except FileNotFoundError:
            logger.warning(f"Can't find text in {path}")
            raise

        try:
            name = (path/"name.txt").read_text().strip()
        except FileNotFoundError:
            name = path.name

        return cls(name, text, tests, str(path))

    def check(self, solution: str) -> Report:
        result = Report(test.run(solution).status
                        for test in self.tests)
        logger.trace(result)
        return result


if __name__ == "__main__":
    problems = Problem.from_folder("DataSet/Tests")
    logger.info(problems.keys())
    melons = problems["melons"]
    solution = "1/0"
    print(melons.check(solution))
