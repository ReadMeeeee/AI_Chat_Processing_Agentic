from pydantic import BaseModel
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionMessageParam,
)
from solution.json_loaders import InstructionBlockSolution, InstructionBlockFunctions


class LLMRequest(BaseModel):
    instructions: InstructionBlockSolution | InstructionBlockFunctions
    task: str


    def to_prompt(self) -> list[ChatCompletionMessageParam]:
        data = self.instructions
        pre_prompt = data.unit_it()
        content = pre_prompt.instructions + self.task

        prompt: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(role="system", content=pre_prompt.role),
            ChatCompletionUserMessageParam(role="user", content=content)
        ]

        return prompt


class ProblemWithSolution(BaseModel):
    description: str
    keywords: list[str]
    solution: str
    name: str = "untitled"
    numbers: list[str] = []


    def unit_it(self) -> dict:
        s = {
            "company": self.name,
            "description": self.description,
            "keywords": self.keywords,
            "solution": self.solution
        }
        return s


class AIModelAPI:
    def __init__(self, api: str, url: str, model_name: str):
        self.api = api
        self.url = url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api, base_url=self.url)

    def get_response(self, request: LLMRequest, temperature: float = 0.1) -> str | None:
        prompt = request.to_prompt()
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt,
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
