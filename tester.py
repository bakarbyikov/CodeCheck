import sys
from csv import DictReader
from io import StringIO
from itertools import count
from pathlib import Path
from typing import Self

from loguru import logger
from pydantic.dataclasses import dataclass


class SolutionError(Exception):
    pass

@dataclass
class Test:
    input: str
    expected: str
    required: bool

    @classmethod
    def from_file(cls, path: Path) -> list[Self]:
        with path.open() as file:
            reader = DictReader(file)
            return [cls(**row) for row in reader]


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
                logger.warning(f"Can't find text in {root}")

            try:
                text = (root/"text.txt").read_text()
            except FileNotFoundError:
                logger.warning(f"Can't find text in {root}")

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


def run(solution: str, input: str) -> str:
    sys.stdin = StringIO(input)
    sys.stdout = out = StringIO()

    try:
        exec(solution, {}, {})
    except Exception as e:
        raise SolutionError(e)
    
    return out.getvalue().strip()



def test(solution: str, problem: Problem):
    passed = 0
    for i, test in enumerate(problem.tests):
        expected = test.expected
        try:
            got = run(solution, test.input)
        except SolutionError as exception:
            logger.error(f"Test #{i} failed with {exception}")
            continue
        if got != test.expected:
            logger.error(f"Test #{i} failed {expected=} {got=}")
            continue
        logger.success(f"Test #{i} passed {expected=} {got=}")
        passed += 1
    logger.info(f"Passed {passed}/{len(problem.tests)} tests")

if __name__ == "__main__":
    problems = Problem.from_folder("DataSet/Tests")
    melons = problems["melons"]
    solution = "1/0"
    test(solution, melons)
