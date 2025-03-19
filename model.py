import re

from llama_cpp import Llama


class Model:
    code_pattern = re.compile("```python(.*)```", re.DOTALL)
    json_pattern = re.compile("```json(.*)```", re.DOTALL)

    def __init__(self):
        self.llm = Llama.from_pretrained(
            repo_id="QuantFactory/Nxcode-CQ-7B-orpo-GGUF",
            filename="Nxcode-CQ-7B-orpo.Q8_0.gguf",
            verbose=False,
            n_gpu_layers=-1,
            n_threads=16,
            n_ctx = 1<<9,
        )
        
    
    def ask(self, text: str) -> str:
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", 
                 "content": "You are an expert AI coding assistant."},
                {"role": "user", "content": text}
            ],
        )
        return response["choices"][0]["message"]["content"]
    
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

if __name__ == "__main__":
    model = Model()
    model.create_solution()