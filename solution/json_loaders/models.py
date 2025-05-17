from pydantic import BaseModel


class InstructionSolution(BaseModel):
    instruction: str
    example: str = ""
    response_format: str = ""


    def unit_it(self) -> str:
        s = (f"{self.instruction}\n"
             f"Пример для выполнения задачи:\n{self.example}\n"
             f"Формат вывода для поля:\n{self.response_format}\n")

        return s


class InstructionBlockSolution(BaseModel):
    role: str
    introduction: str
    instructions: list[InstructionSolution]
    context: str | None
    format: str | None


    def unit_it(self) -> tuple[str, str]:
        instructions = self.introduction + "\n" + "\n".join(instruction.unit_it() for instruction in self.instructions)
        s = (f"Инструкция для задачи:{instructions}\n"
             f"Контекст для задачи:\n{self.context or 'данные не найдены'}\n"
             f"Формат вывода:\n{self.format or 'данные не найдены'}\n")

        return self.role, s


class ParameterInfo(BaseModel):
    argument_name: str
    typeof: str
    description: str


    def unit_it(self) -> str:
        s = (f"Аргумент функции: {self.argument_name}\n"
             f"Тип аргумента:\n{self.typeof}\n"
             f"Описание аргумента:\n{self.description}\n")

        return s


class FunctionData(BaseModel):
    name: str
    description: str
    parameters: list[ParameterInfo]
    returns: str | None = None


    def unit_it(self) -> str:
        params = "\n".join(param.unit_it() for param in self.parameters)
        s = (
            f"Название функции: {self.name}\n"
            f"Описание функции: {self.description}\n"
            f"Параметры функции:\n{params}"
        )
        if self.returns:
            s += f"\nФункция возвращает: {self.returns}"

        return s


class InstructionOfFunctions(BaseModel):
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
