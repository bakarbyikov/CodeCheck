import uvicorn
from fastapi import FastAPI

from model import Model
from schema import ChatResponse, Message, SolutionResponse, TestsResponse

app = FastAPI()


@app.post("/chat")
def chat(messages: list[Message]) -> ChatResponse:
    solution = Model().chat(messages)
    return ChatResponse(solution=solution)


@app.post("/create_solution")
def create_solution(problem: str) -> SolutionResponse:
    solution = Model().create_solution(problem)
    return SolutionResponse(solution=solution)


@app.post("/create_tests")
def create_tests(problem: str) -> TestsResponse:
    return Model().create_tests(problem)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
