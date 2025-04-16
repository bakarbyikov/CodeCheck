import re
import sys
from typing import Optional

import ollama
from contexttimer import Timer
from loguru import logger
from tqdm import tqdm

from ..api.schema import Message, Test, TestsResponse
from ..dataset.tester import Problem, ProblemSet, Report, Status


class Prompts:

    @staticmethod
    def solve(problem: str):
        return (
            "Solve this problem using python. "
            "Don't use third party libraries. "
            "Read values from stdin. "
            "Write answer into stdout. "
            f"\n###\n{problem}\n###\n"
        )

    @staticmethod
    def tests(problem: str):
        return (
            "List few testcases for this problem:"
            f"\n###\n{problem}\n###\n"
            "Use JSON schema:\n"
            "Testcase = {'input': str, 'expected': str}\n"
            "Result = {'tests': List[Testcase]}\n"
            "Return: Result"
        )


class Model:
    code_pattern = re.compile("```(?:python)?([^`]*)",
                              re.DOTALL)
    json_pattern = re.compile("```json([^`]*)", re.DOTALL)

    def __init__(self, model="qwen2.5-coder:3b"):
        self.model = model
        me = id(self)
        self.logger = logger.bind(model=me)
        logger.add(f"model.log", level="TRACE",
                   filter=lambda record: record["extra"].get("model") == me)

    def message(self, messages: list[dict[str, str]]) -> str:
        response = ollama.chat(
            self.model,
            messages,
        )
        content = response.message.content
        self.logger.trace(f"\n{messages}\n=>\n{content}")
        return content

    def ask(self, text: str) -> str:
        messages = [
            {"role": "system",
             "content": "You are an expert AI coding assistant."},
            {"role": "user", "content": text}
        ]
        return self.message(messages)

    def extract_code(self, text: str) -> Optional[str]:
        found = self.code_pattern.search(text)
        if found is None:
            logger.trace("Python code not found")
            return found
        return found.group(1).strip()

    def extract_json(self, text: str) -> Optional[str]:
        found = self.json_pattern.search(text)
        if found is None:
            logger.trace("Json not found")
            return found
        return found.group(1).strip()

    def extract_tests(self, text: str) -> list[Test]:
        tests = (self.extract_json(text)
                 or self.extract_code(text))
        if not tests:
            return list()
        return TestsResponse.model_validate_json(tests).tests

    def gen(self, prompt: str) -> str:
        args = dict(
            model=self.model,
            prompt=prompt,
            options=dict(
                seed=42
            )
        )
        answer = ollama.generate(**args).response
        self.logger.trace(f"\n{prompt}\n=>\n{answer}")
        return answer

    def create_solution(self, problem: str) -> Optional[str]:
        prompt = Prompts.solve(problem)
        return self.extract_code(self.gen(prompt))

    def create_tests(self, problem: str) -> list[Test]:
        prompt = Prompts.tests(problem)
        return self.extract_tests(self.gen(prompt))

    def chat(self, messages: list[Message]) -> Optional[str]:
        problem = messages[0].content
        messages[0] = Message(
            role="user",
            content=Prompts.solve(problem)
        )
        return self.extract_code(self.message(messages))

    def test(self, problem: Problem) -> Status:
        with Timer() as timer:
            solution = self.create_solution(problem.text)
        logger.trace(f"Solved in {timer.elapsed:0.2f} seconds")
        if not solution:
            return Status.Error
        return problem.check(solution)


def main():
    problems = ProblemSet.from_folder("DataSet/Tests")
    to_test = list(problems.by_tag("Tests"))

    model = Model("qwen2.5-coder:3b")
    results = Report(map(model.test, tqdm(to_test, file=sys.stderr)))
    logger.info(results)
