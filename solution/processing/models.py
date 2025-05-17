from pydantic import BaseModel
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionMessageParam,
)
from solution.json_loaders.models import (InstructionBlockSolution,
                                          ParameterInfo, FunctionData, InstructionOfFunctions)


class LLMRequest(BaseModel):
    instructions: InstructionBlockSolution | InstructionOfFunctions
    task: str


    def to_prompt(self) -> list[ChatCompletionMessageParam]:
        prompt: list[ChatCompletionMessageParam] = []

        if type(self.instructions) is InstructionOfFunctions:

            content = (
                f"Инструкции:\n{self.instructions.instructions}\n\n"
                f"Функции:\n{self.instructions.functions}\n\n"
                f"Входные данные:\n{self.task}"
            )

            prompt: list[ChatCompletionMessageParam] = [
                ChatCompletionSystemMessageParam(role="system", content=self.role),
                ChatCompletionUserMessageParam(role="user", content=content)
            ]


        else:
            instruct = self.Instructions.Introduction + self.instructions.instructions
            content = (
                f"Инструкции:\n{instruct}\n\n"
                f"Контекст:\n{self.instructions.context}\n\n"
                f"Формат вывода:\n{self.instructions.format}\n\n"
                f"Входные данные:\n{self.task}"
            )

            prompt: list[ChatCompletionMessageParam] = [
                ChatCompletionSystemMessageParam(role="system", content=self.role),
                ChatCompletionUserMessageParam(role="user", content=content)
            ]

        return prompt


class ProblemWithSolution(BaseModel):
    description: str
    keywords: list[str]
    solution: str
    name: str = "untitled"
    numbers: list[str] = None


class AIModelAPI:
    def __init__(self, api: str, url: str, model_name: str):
        self.api = api
        self.url = url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api, base_url=self.url)

    def get_response(self, request: LLMRequest,
                     temperature: float = 0.1):
        prompt = request.to_prompt()
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt,
            temperature=temperature
        )
        return response.choices[0].message.content