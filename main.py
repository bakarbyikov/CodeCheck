import uvicorn
from fastapi import FastAPI

from model import Model
from schema import (MessagesRequest, ProblemRequest,
                    SolutionResponse, TestsResponse)

app = FastAPI()


@app.post("/chat")
def chat(request: MessagesRequest):
    solution = Model().chat(request.messages)
    return SolutionResponse(solution=solution)


@app.post("/create_solution")
def create_solution(request: ProblemRequest):
    solution = Model().create_solution(request.problem)
    return SolutionResponse(solution=solution)


@app.post("/create_tests")
def create_tests(request: ProblemRequest):
    tests = Model().create_tests(request.problem)
    return TestsResponse(tests=tests)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
