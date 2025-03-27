import sys
from collections import Counter
from csv import DictReader
from enum import Enum, auto
from io import StringIO
from itertools import count
from pathlib import Path
from typing import Self

from loguru import logger
from pydantic.dataclasses import dataclass


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

    def run(self, solution: str, verbosity=0) -> Result:
        result = self._run(solution)
        if verbosity > 0:
            i, expected, got = self.index, self.expected, result.info
            match result.status:
                case Status.Passed:
                    logger.success(f"Test #{i} passed {expected=} {got=}")
                case Status.Failed:
                    logger.error(f"Test #{i} failed {expected=} {got=}")
                case Status.Error:
                    logger.error(f"Test #{i} failed with {got}")
        return result

    def _run(self, solution: str) -> Result:
        sys.stdin = StringIO(self.input)
        sys.stdout = out = StringIO()

        try:
            exec(solution, {}, {})
        except Exception as e:
            return Result(Status.Error, str(e))

        got = out.getvalue().strip()
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
                tests = Test.from_file(root/"test.csv")
            except FileNotFoundError:
                logger.warning(f"Can't find tests in {root}")
                continue

            try:
                text = (root/"text.txt").read_text()
            except FileNotFoundError:
                logger.warning(f"Can't find text in {root}")
                continue

            try:
                name = (root/"name.txt").read_text()
            except FileNotFoundError:
                name = root.name

            if name in found:
                for i in count(1):
                    indexed = f"{name}_{i}"
                    if indexed not in found:
                        name = indexed
                        break
                logger.warning(
                    f"Problem {name=} is not unique, replacing with {indexed}")

            found[name] = cls(name, text, tests, str(root))
        return found

    def check(self, solution: str, verbosity=0) -> dict[Status, int]:
        stats = Counter(test.run(solution, verbosity-1).status 
                        for test in self.tests)
        if verbosity > 0:
            names = "/".join(s.name for s in Status)
            values = "/".join(str(stats[s]) for s in Status)
            logger.info(f"{names}: {values}")
        return stats


if __name__ == "__main__":
    problems = Problem.from_folder("DataSet/Tests")
    melons = problems["melons"]
    solution = "1/0"
    melons.check(solution, verbosity=2)
