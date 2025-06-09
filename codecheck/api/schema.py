from typing import Literal, Optional

from pydantic import BaseModel

from codecheck.dataset.tester import Test


class Solution(BaseModel):
    solution: str
    tests: list[Test]


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class MessagesRequest(BaseModel):
    messages: list[Message]


class ProblemRequest(BaseModel):
    problem: str


class SolutionResponse(BaseModel):
    solution: Optional[str]


class TestsResponse(BaseModel):
    tests: list[Test]
