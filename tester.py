from collections import Counter
from csv import DictReader
from enum import Enum, auto
from functools import partial
from itertools import chain
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import NamedTemporaryFile
from typing import Generator, Self

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
            got, errors = map(str.strip, child.communicate(self.input))

        if errors:
            return Result(Status.Error, errors)
        if got != self.expected:
            return Result(Status.Failed, got)
        return Result(Status.Passed, got)


@dataclass
class Problem:
    text: str
    tests: list[Test]
    tags: set[str]

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

        tags = path.parts

        return cls(text, tests, tags)

    def check(self, solution: str) -> Report:
        result = Report(test.run(solution).status
                        for test in self.tests)
        logger.trace(result)
        return result

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


@dataclass
class ProblemSet:
    problems: list[Problem]

    @classmethod
    def from_folder(cls, folder: str):
        problems = list()
        for root, dirs, files in Path(folder).walk():
            if not files:
                continue

            try:
                problem = Problem.open(root)
            except FileNotFoundError:
                continue

            problems.append(problem)
        return cls(problems)

    def by_tag(self, tag: str) -> Generator[Problem, None, None]:
        yield from filter(partial(Problem.has_tag, tag=tag), self.problems)

    def tags(self) -> dict[str, int]:
        return Counter(chain.from_iterable(problem.tags for problem in self.problems))


if __name__ == "__main__":
    problems = ProblemSet.from_folder("DataSet/Tests")
    logger.info(problems.tags())
    melons, *_ = problems.by_tag("melons")
    solution = "1/0"
    print(melons.check(solution))
