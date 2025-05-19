from json import load
from .models import InstructionBlockSolution, InstructionBlockFunctions
from .my_utils import is_file_is_correct


def load_task(path_to_task: str) -> tuple[str, str]:
    is_file_is_correct(path_to_task, '.json')
    with open(path_to_task, 'r', encoding="utf-8") as f:
        data = load(f)

    company = data['company']
    chat = data['chat']

    return company, chat


def load_instruction_solution(json_instruction_path: str) -> InstructionBlockSolution:
    """
    Функция создает блок инструкций InstructionBlock из json-файла

    :param json_instruction_path: Путь к json-файлу инструкций по обработке диалога с ТП

    :return: Блок инструкций для последующей обработки в запросе
    """
    is_file_is_correct(json_instruction_path, ".json")
    with open(json_instruction_path, "r", encoding="utf-8") as f:
        data = load(f)

    return InstructionBlockSolution.model_validate(data)


def load_instruction_function_calling(json_instruction_path: str) -> InstructionBlockFunctions:
    """
    Функция создает блок инструкций InstructionBlockFunctions из json-файла

    :param json_instruction_path: Путь к json-файлу инструкций по обработке диалога с ТП

    :return: Блок инструкций для последующей обработки в запросе
    """
    is_file_is_correct(json_instruction_path, ".json")
    with open(json_instruction_path, "r", encoding="utf-8") as f:
        data = load(f)

    return InstructionBlockFunctions.model_validate(data)


"""
def main():
    from solution.config import path_to_task_instruct_json, path_to_func_instruct_json


    instructs_solution = load_instruction_solution(path_to_task_instruct_json)
    data_solution = instructs_solution.unit_it()
    print(f"role: {data_solution[0]}\n\n"
          f"data: {data_solution[1]}")

    instructs_function = load_instruction_function_calling(path_to_func_instruct_json)
    data_function = instructs_function.unit_it()
    print(f"role: {data_function[0]}\n\n"
          f"data: {data_function[1]}")

    return None


if __name__ == "__main__":
    main()
"""
