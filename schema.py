from typing import Literal, Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Test(BaseModel):
    input: str
    expected: str


class MessagesRequest(BaseModel):
    messages: list[Message]


class ProblemRequest(BaseModel):
    problem: str


class SolutionResponse(BaseModel):
    solution: Optional[str]


class TestsResponse(BaseModel):
    tests: list[Test]
