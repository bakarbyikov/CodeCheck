from typing import Literal, Optional

from pydantic import BaseModel

Solution = str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Test(BaseModel):
    input: str
    expected: str


class SolutionResponse(BaseModel):
    solution: Optional[Solution]


class TestsResponse(BaseModel):
    tests: list[Test]


class ChatResponse(SolutionResponse):
    pass
