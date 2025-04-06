import re
import sys
from typing import Any

from contexttimer import Timer
import ollama
from loguru import logger
from tqdm import tqdm

from misc import *
from tester import Problem, ProblemSet, Report, Status


class Model:
    code_pattern = re.compile("```(?:python)?([^`]*)", re.DOTALL)
    json_pattern = re.compile("```json([^`]*)", re.DOTALL)

    def __init__(self, config: dict[str, Any] = Qwen_7b_Q8):
        me = id(self)
        self.logger = logger.bind(model=me)
        logger.add(f"model.log", level="TRACE",
                   filter=lambda record: record["extra"].get("model") == me)

    def message(self, messages: list[dict[str, str]]) -> str:
        response = ollama.chat(
            "qwen2.5-coder:7b",
            # "qwen2.5-coder:3b",
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

    def extract_code(self, text: str) -> str:
        found = self.code_pattern.search(text)
        if found is None:
            logger.trace("Python code not found")
            return found
        return found.group(1).strip()

    def extract_json(self, text: str) -> str:
        found = self.json_pattern.search(text)
        if found is None:
            logger.trace("Json not found")
            return found
        return found.group(1).strip()

    def create_solution(self, problem: str) -> str:
        prompt = f"Solve next problem using python.Don't use third party libraries. Don't add prompt in input.\n###\n{problem}\n###\n"
        return self.extract_code(self.ask(prompt))

    def create_tests(self, problem: str, code: str) -> str:
        prompt = 'List some testcases to fully test entire code using JSON schema:\n Testcase = {"input": str, "expected": str}\nReturn: List[Testcase]'
        prompt = "\n###\n".join((prompt, problem, code))
        result = self.ask(prompt)
        print(result)
        return self.extract_json(result) or self.extract_code(result)

    def chat(self, problem: str):
        prompt = f"Solve next problem using python.\n###\n{problem}\n###\n"
        messages = list()
        while True:
            messages.append({"role": "user", "content": prompt})
            sol = self.extract_code(self.message(messages))
            messages.append({"role": "assistant",
                            "content": f"```python\n{sol}\n```"})
            prompt = yield sol

    def test(self, problem: Problem) -> Status:
        with Timer() as timer:
            solution = self.create_solution(problem.text)
        logger.trace(f"Solved in {timer.elapsed:0.2f} seconds")
        if not solution:
            return Status.Error
        return problem.check(solution)


if __name__ == "__main__":
    problems = ProblemSet.from_folder("DataSet/Tests")
    to_test = list(problems.by_tag("Tests"))

    model = Model(Qwen_7B_q2)
    results = Report(map(model.test, tqdm(to_test, file=sys.stderr)))
    logger.info(results)
