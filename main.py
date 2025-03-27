import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from model import Model

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def main():
    return FileResponse("static/index.html")

@app.get("/generate_problem")
def generate_problem(text: str):
    model = Model()
    solution = model.create_solution(text)
    tests = model.create_tests(text, solution)
    return {
        "solution": solution,
        "tests": tests
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
