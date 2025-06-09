import csv
from collections import Counter
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Generator, Self

from loguru import logger
from pydantic.dataclasses import dataclass

from .tester import Status, Test, test


def try_read(path: Path) -> str | None:
    try:
        return path.read_text()
    except FileNotFoundError:
        return None


class Report(Counter):
    def __str__(self):
        names = "/".join(s.name for s in Status)
        values = "/".join(str(self[s]) for s in Status)
        return f"{names}: {values}"

    def status(self) -> Status:
        return next(status for status in reversed(Status)
                    if self[status])


@dataclass
class Problem:
    name: str
    text: str
    tests: list[Test]
    solution: str
    tags: set[str]

    @classmethod
    def read(cls, path: Path) -> Self:
        name = try_read(path/"name.txt") or path.parts[-1]

        try:
            text = (path/"text.md").read_text()
        except FileNotFoundError:
            raise ValueError(f"Can't find text.md in {path}")

        try:
            solution = (path/"solution.py").read_text()
        except FileNotFoundError:
            solution = "raise NotImplementedError"
            logger.warning(f"Can't find solution in {path}")

        tests = Test.read(path/"test.csv")
        if not tests:
            logger.warning(f"Can't find tests in {path}")

        tags = set(path.parts)
        return cls(name, text, tests, solution, tags)

    @staticmethod
    def create(path: Path, text: str):
        path.mkdir()
        with (path/"text.md").open('w') as file:
            print(text, file=file)

    def check(self, solution: str) -> Status:
        logger.trace(f"Problem: {self.name}")
        result = Report(r.status for r in test(solution, self.tests))
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

            problem = Problem.read(root)
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


def main():
    problems = ProblemSet.from_folder()
    for problem in problems.problems:
        print(problem.solution)
        for test in problem.tests:
            print(test.model_dump_json())
    logger.info(problems.self_check())
