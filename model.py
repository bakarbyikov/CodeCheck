import re

from contexttimer import Timer
from llama_cpp import Llama
from loguru import logger

from tester import Problem

logger.add("model.log")


class Model:
    code_pattern = re.compile("```python([^`]*)", re.DOTALL)
    json_pattern = re.compile("```json([^`]*)", re.DOTALL)

    def __init__(self):
        self.llm = Llama.from_pretrained(
            repo_id="Qwen/Qwen2.5-Coder-7B-Instruct-GGUF",
            filename="qwen2.5-coder-7b-instruct-q8_0.gguf",
            verbose=False,
            n_gpu_layers=-1,
            n_threads=16,
            n_ctx=1 << 10,
        )
    
    def message(self, messages: list[dict[str, str]]) -> str:
        response = self.llm.create_chat_completion(messages)
        content = response["choices"][0]["message"]["content"]
        logger.debug(f"\n{messages}\n=>\n{content}")
        return content
        

    def ask(self, text: str) -> str:
        messages = [
            {"role": "system",
             "content": "You are an expert AI coding assistant."},
            {"role": "user", "content": text}
        ]
        return self.message(messages)
        

    def extract_code(self, text: str) -> str:
        # print(text)
        found = self.code_pattern.search(text)
        return found and found.group(1).strip()

    def extract_json(self, text: str) -> str:
        # print(text)
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

    def test(self, problems: list[Problem]):
        for problem in problems:
            logger.info(f"Problem {problem.name}")
            with Timer() as timer:
                solution = self.create_solution(problem.text)
            logger.info(f"Solved in {timer.elapsed:0.2f} seconds")
            problem.check(solution, verbose=1)
    
    def chat(self, problem: str):
        prompt = f"Solve next problem using python.\n###\n{problem}\n###\n"
        messages = list()
        while True:
            messages.append({"role": "user", "content": prompt})
            sol = self.extract_code(self.message(messages))
            messages.append({"role": "assistant",
                            "content": f"```python\n{sol}\n```"})
            prompt = yield sol
        


if __name__ == "__main__":
    problems = Problem.from_folder("DataSet/Tests")
    melons = problems["melons"]
    
    model = Model()
    
    chat = model.chat(melons.text)
    sol = chat.send(None)
    while True:
        print(f"\n{sol}\n")
        sol = chat.send(input())