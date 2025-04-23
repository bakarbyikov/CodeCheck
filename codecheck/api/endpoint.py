from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI

from ..model.model import Model
from .schema import (MessagesRequest, ProblemRequest,
                    SolutionResponse, TestsResponse)

app = FastAPI()

origins = [
    "https://olegpepeg.ru:8081",
    "http://olegpepeg.ru:8081",
    "https://olegpepeg.ru:8080",
    "http://olegpepeg.ru:8080",
    
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


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main
