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

from misc import try_read


class SolutionError(Exception):
    pass


class Status(Enum):
    Passed = auto()
    Failed = auto()
    Error = auto()


@dataclass
class Result:
    status: Status
    expected: str
    got: str
    error: str

    @classmethod
    def from_inputs(cls, expected: str, got: str, error: str) -> Self:
        if error:
            status = Status.Error
        elif got != expected:
            status = Status.Failed
        else:
            status = Status.Passed
        return cls(status, expected, got, error)

    def __str__(self):
        match self.status:
            case Status.Passed:
                return f"passed"
            case Status.Failed:
                return f"failed expected: {self.expected}, got: {self.got}"
            case Status.Error:
                return f"error:\n{self.error}"


class Report(Counter):
    def __str__(self):
        names = "/".join(s.name for s in Status)
        values = "/".join(str(self[s]) for s in Status)
        return f"{names}: {values}"
    
    def status(self) -> Status:
        return next(status for status in reversed(Status)
                    if self[status])


@dataclass
class Test:
    index: int
    input: str
    expected: str

    @classmethod
    def from_file(cls, path: Path) -> list[Self]:
        text = try_read(path)
        # if not text:
        #     return list()
        reader = DictReader(text.splitlines() or list())
        return [cls(i, **row) for i, row in enumerate(reader)]

    def run(self, solution: str) -> Result:
        with NamedTemporaryFile(mode='w') as script:
            print(solution, file=script, flush=True)

            child = Popen(['python3', script.name],
                          stdin=PIPE, stdout=PIPE, stderr=PIPE,
                          text=True, )
            got, error = map(str.strip, child.communicate(self.input))
        result = Result.from_inputs(self.expected, got, error)
        logger.trace(f"Test #{self.index} {result}")
        return result


@dataclass
class Problem:
    name: str
    text: str
    solution: str | None
    tests: list[Test]
    tags: set[str]

    @classmethod
    def open(cls, path: Path) -> Self:
        name = try_read(path/"name.txt") or path.parts[-1]
        
        text = try_read(path/"text.md")
        if not text:
            logger.warning(f"Can't find text in {path}")
            return None

        solution = try_read(path/"solution.py")
        if not solution:
            logger.warning(f"Can't find solution in {path}")

        tests = Test.from_file(path/"test.csv")
        if not tests:
            logger.warning(f"Can't find tests in {path}")

        tags = path.parts

        return cls(name, text, solution, tests, tags)

    def check(self, solution: str) -> Status:
        logger.trace(f"Problem: {self.name}")
        result = Report(test.run(solution).status
                        for test in self.tests)
        logger.trace(result)
        return result.status()

    def self_check(self) -> Status:
        return self.check(self.solution)

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


@dataclass
class ProblemSet:
    problems: list[Problem]

    @classmethod
    def from_folder(cls, folder: str = "DataSet/Tests"):
        problems = list()
        for root, dirs, files in Path(folder).walk():
            if not files:
                continue

            problem = Problem.open(root)
            if not problem:
                continue
            
            problems.append(problem)
        return cls(problems)

    def self_check(self) -> Report:
        result = Report(map(Problem.self_check, self.problems))
        logger.trace(f"ProblemSet selftest: {result}")
        return result

    def by_tag(self, tag: str) -> Generator[Problem, None, None]:
        yield from filter(partial(Problem.has_tag, tag=tag), self.problems)

    def tags(self) -> dict[str, int]:
        return Counter(chain.from_iterable(problem.tags for problem in self.problems))


if __name__ == "__main__":
    problems = ProblemSet.from_folder()
    logger.info(problems.self_check())
    
    # logger.info(problems.tags())
    # melons, *_=problems.by_tag("melons")
    # solution="1/0"
    # logger.info(melons.check(solution))
