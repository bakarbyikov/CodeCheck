import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from codecheck.dataset.tester import Result, test

from ..model.model import Model
from .schema import (MessagesRequest, ProblemRequest, Solution,
                     SolutionResponse, TestsResponse)

app = FastAPI(
    root_path="/api"
)

origins = [
    "https://olegpepeg.ru",
    "http://olegpepeg.ru",

    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(request: MessagesRequest) -> SolutionResponse:
    solution = Model().chat(request.messages)
    return SolutionResponse(solution=solution)


@app.post("/create_solution")
def create_solution(request: ProblemRequest) -> SolutionResponse:
    solution = Model().create_solution(request.problem)
    return SolutionResponse(solution=solution)


@app.post("/create_tests")
def create_tests(request: ProblemRequest) -> TestsResponse:
    tests = Model().create_tests(request.problem)
    return TestsResponse(tests=tests)


@app.post("/test_solution")
def test_solution(request: Solution) -> list[Result]:
    return test(request.solution, request.tests)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
