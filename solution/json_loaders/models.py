from pydantic import BaseModel


class InstructionSolution(BaseModel):
    field_name: str
    instruction: str
    example: str = ""
    response_format: str = ""


    def unit_it(self) -> str:
        s = (
             f"{self.instruction}\n"
             f"Пример для выполнения задачи:\n{self.example}\n"
             f"Формат вывода:\n{self.response_format}\n"
        )

        return s


class InstructionBlockSolution(BaseModel):
    role: str
    introduction: str
    instructions: dict[str, InstructionSolution] | None = None
    context: str | list[str] | None = None
    output_format: InstructionSolution | None = None


    def unit_it(self) -> tuple[str, str]:
        instructions = self.introduction + "\n" + "\n".join(
            instruction.unit_it() for instruction in self.instructions.values()
        ) if self.instructions else ""

        context = "\n".join(self.context) if isinstance(self.context, list) else (self.context or "данные не найдены")

        s = (
            f"Инструкция для задачи:\n{instructions}\n"
            f"Контекст для задачи:\n{context or 'данные не найдены'}\n"
            f"Формат вывода:\n{self.output_format.unit_it() if self.output_format else 'данные не найдены'}\n"
        )
        return self.role, s


class ParameterInfo(BaseModel):
    argument_name: str
    typeof: str
    description: str


    def unit_it(self) -> str:
        s = (
            f"  Аргумент функции: {self.argument_name}\n"
            f"  Тип аргумента: {self.typeof}\n"
            f"  Описание аргумента: {self.description}\n"
        )

        return s


class FunctionData(BaseModel):
    name: str
    description: str
    parameters: list[ParameterInfo]
    returns: str | None = None


    def unit_it(self) -> str:
        params = "\n".join(param.unit_it() for param in self.parameters)
        s = (
            f" Название функции: {self.name}\n"
            f" Описание функции: {self.description}\n"
            f" Параметры функции:\n{params}"
        )
        if self.returns:
            s += f"\n Функция возвращает: {self.returns}"

        return s


class InstructionBlockFunctions(BaseModel):
    role: str
    instructions: str
    functions: list[FunctionData]


    def unit_it(self) -> tuple[str, str]:
        functions = "\n".join(func.unit_it() for func in self.functions)
        s = (
            f"Инструкции для 'function calling':\n{self.instructions}\n"
            f"Описание функций:\n{functions}\n"
        )

        return self.role, s
