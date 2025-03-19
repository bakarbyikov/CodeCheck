from fastapi import FastAPI

from model import Model

app = FastAPI()
model = Model()

@app.get("/generate_problem")
def generate_problem(text: str):
    solution = model.create_solution(text)
    tests = model.create_tests(text, solution)
    return {
        "solution": solution,
        "tests": tests
    }

