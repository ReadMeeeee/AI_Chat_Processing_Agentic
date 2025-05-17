from json import load
from os import path
from solution.json_loaders.models import InstructionSolution, InstructionBlockSolution, InstructionOfFunctions


def is_file_is_correct(path_to_file: str, file_format: str, is_file: bool = True, is_correct: bool = True) -> None:
    if is_file and not path.exists(path_to_file):
        raise FileNotFoundError(f"Файл не найден: {path_to_file}")

    if is_correct and not file_format.startswith("."):
        raise ValueError(f"Аргумент 'file_format' должен начинаться с точки. Получено: \"{file_format}\"")

    shaped_path = path.splitext(path.basename(path_to_file))
    format_of_file = shaped_path[1]

    if is_correct and (format_of_file != file_format):
        raise ValueError(f"Ожидаемый формат файла - \"{file_format}\", получен - {format_of_file}")


def load_instruction_solution(json_instruction_path: str) -> InstructionBlockSolution:
    """
    Функция создает блок инструкций InstructionBlock из json-файла

    :param json_instruction_path: Путь к json-файлу инструкций по обработке диалога с ТП

    :return: Блок инструкций для последующей обработки в запросе
    """
    is_file_is_correct(json_instruction_path, ".json")
    with open(json_instruction_path, "r", encoding="utf-8") as f:
        data = load(f)


    def _is_subset_of(keys: set[str], data_position: dict) -> None:
        if not keys.issubset(data_position):
            raise KeyError(f"Инструкции не содержат необходимые ключи: {keys - set(data_position)}")


    paragraph_keys = {"role", "introduction", "context", "instructions", "output_format"}
    instruction_keys = {"description", "keywords", "solution"}
    for_instruction_keys = {"instruction", "example", "response_format"}

    _is_subset_of(paragraph_keys, data)
    _is_subset_of(instruction_keys, data['instructions'])
    _is_subset_of(for_instruction_keys, data['output_format'])
    for item in data['instructions']:
        _is_subset_of(for_instruction_keys, data['instructions'][item])


    def _make_instruction(data_section: dict[str, dict], key_of_section: str) -> str:
        subdata = data_section[key_of_section]
        instruction = InstructionSolution(
            instruction=subdata.get("instruction", ""),
            example=subdata.get("example", ""),
            response_format=subdata.get("response_format", ""),
        )
        return instruction.unit_it()


    instructions = ""
    for key in instruction_keys:
        instruct = _make_instruction(data["instructions"], key)
        instructions += f"{instruct}\n"

    format_instruction = _make_instruction({"output_format": data["output_format"]}, "output_format")

    return InstructionBlockSolution(
        role=data["role"],
        introduction=data["introduction"],
        instructions=instructions,
        context="\n".join(data["context"]) if isinstance(data["context"], list) else data["context"],
        format=format_instruction
    )


def load_instruction_function_calling(json_instruction_path: str) -> InstructionOfFunctions:
    """
    Загружает json-файл описания функций и возвращает текстовый блок для system prompt.

    :param json_instruction_path: Путь к файлу .json

    :return: Объект InstructionOfFunctions
    """
    is_file_is_correct(json_instruction_path, ".json")

    with open(json_instruction_path, "r", encoding="utf-8") as f:
        data = load(f)

    if "role" not in data or "arguments" not in data:
        raise KeyError("Ожидаются ключи 'role' и 'arguments' в JSON-файле.")

    role_text = data["role"]
    function_entries = data["arguments"]
    functions: list[FunctionData] = []

    for function_data in function_entries:
        if not function_data.get("name"):
            continue  # пропускаем пустые заглушки

        param_objs = [
            ParameterInfo(**p)
            for p in function_data.get("parameters", [])
            if p.get("argument_name")
        ]

        function_obj = FunctionData(
            name=function_data["name"],
            description=function_data.get("description", ""),
            parameters=param_objs,
            returns=function_data.get("returns")
        )
        functions.append(function_obj)

    # Сборка текстов
    all_functions_text = "\n\n".join(f.unit_it() for f in functions)
    instruction_intro = "Ты можешь использовать следующие функции для обработки и анализа данных:"

    return InstructionOfFunctions(
        role=role_text,
        instructions=instruction_intro,
        functions=all_functions_text
    )


def main():
    from solution.config import path_to_instruct_json


    instructs = load_instruction_solution(path_to_instruct_json)
    instructions = f"{instructs.introduction}\n\n{instructs.instructions}\n"
    print(f"role:         {instructs.role}\n\n"
          f"instructions: {instructions}\n\n"
          f"context:      {instructs.context}\n\n"
          f"format:       {instructs.format}\n\n"  )

    return None


if __name__ == "__main__":
    main()

