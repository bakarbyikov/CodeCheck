from llama_cpp import Llama

class Model:
    def __init__(self):
        self.llm = Llama.from_pretrained(
            repo_id="QuantFactory/Nxcode-CQ-7B-orpo-GGUF",
            filename="Nxcode-CQ-7B-orpo.Q8_0.gguf",
            verbose=False,
            n_gpu_layers=-1,
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
        
    def create_solution(self, problem: str) -> str:
        return self.ask(f"Solve next problem using python.\n###\n{problem}\n###\n")
    
    def create_tests(self, problem: str, code: str) -> str:
        prompt = 'List some testcases to fully test entire code using JSON schema:\n Testcase = {"input": str, "expected": str}\nReturn: List[Testcase]'
        return self.ask(f"{prompt}\n###\n{problem}\n###\n{code}\n###")

if __name__ == "__main__":
    model = Model()
    model.create_solution()