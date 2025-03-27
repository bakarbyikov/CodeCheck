import re
import sys
from typing import Any

from contexttimer import Timer
from llama_cpp import Llama
from loguru import logger
from tqdm import tqdm

from misc import (Coder_GRPO_3B, Coder_GRPO_3B_Q8, Qwen_7B_q2, Qwen_7b_Q8,
                  Qwen_14B_Q5)
from tester import Problem, Report, Status

logger.remove()
logger.add(sys.stderr, level="DEBUG")


class Model:
    code_pattern = re.compile("```python([^`]*)", re.DOTALL)
    json_pattern = re.compile("```json([^`]*)", re.DOTALL)

    def __init__(self, config: dict[str, Any] = Qwen_7b_Q8):
        me = id(self)
        self.logger = logger.bind(model=me)
        logger.add(f"model.log",
                   filter=lambda record: record["extra"].get("model") == me)
        self.llm = Llama.from_pretrained(**config)
        self.temp = 1

    def message(self, messages: list[dict[str, str]]) -> str:
        response = self.llm.create_chat_completion(
            messages, temperature=self.temp)
        content = response["choices"][0]["message"]["content"]
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
        return found and found.group(1).strip()

    def extract_json(self, text: str) -> str:
        found = self.json_pattern.search(text)
        return found and found.group(1).strip()

    def create_solution(self, problem: str) -> str:
        prompt = f"Solve next problem using python.\n###\n{problem}\n###\n"
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

    def test(self, problem: Problem, verbosity=0):
        with Timer() as timer:
            solution = self.create_solution(problem.text)
        if verbosity > 0:
            logger.info(f"Problem {problem.name}")
            logger.info(f"Solved in {timer.elapsed:0.2f} seconds")
        result = problem.check(solution, verbosity=verbosity-1)
        for status in reversed(Status):
            if result[status]:
                return status
        else:
            assert False, f"Problem without tests"


if __name__ == "__main__":
    problems = Problem.from_folder("DataSet/Tests")
    melons = problems["melons_en"]

    model = Model(Coder_GRPO_3B_Q8)
    results = Report(map(model.test, tqdm([melons]*25, file=sys.stderr)))
    logger.info(results)
