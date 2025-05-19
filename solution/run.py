import json
from typing import Callable

from solution.docx_converter import strip_json_markdown
from solution.config import deepseek_api, chatgpt_api, path_to_func_instruct_json, path_to_input_data, path_to_process, path_to_output, path_to_task_instruct_json
from solution.chat_handler.models import AIModelAPI, LLMRequest
from solution.json_loaders import load_instruction_function_calling
from solution.docx_converter import process_docxs_to_json
from solution.chat_handler import chats_process
from solution.convert_and_process import convert_and_process_dir


# region 'Интерпретатор function calling' на коленке
# Если вдруг это пошло бы в прод - я оформил бы красивую обертку в виде класса
function_map: dict[str, Callable] = {
    "process_docxs_to_json": process_docxs_to_json,
    "chats_process": chats_process,
    "convert_and_process_dir": convert_and_process_dir
}

model_map: dict[str, AIModelAPI] = {
    "deepseek_api": deepseek_api,
    "chatgpt_api": chatgpt_api
}


def execute_function_call(function_name: str, arguments: dict) -> str:
    if function_name not in function_map:
        raise ValueError(f"Функция '{function_name}' нет")

    if "model" in arguments and isinstance(arguments["model"], str):
        m = arguments["model"]
        if m in model_map:
            arguments["model"] = model_map[m]
        else:
            raise ValueError(f"Модель '{m}' не найдена")

    print(f"Запуск функции: {function_name}\nС аргументами: {arguments}\n\n")
    function_map[function_name](**arguments)
    return f"Функция {function_name} запущена"


def run_function_agent(
    model: AIModelAPI,
    instruction_json_path: str,
    user_request: str
) -> str:
    instructions = load_instruction_function_calling(instruction_json_path)
    request = LLMRequest(instructions=instructions, task=user_request)
    raw = model.get_response(request)

    cleaned = strip_json_markdown(raw)
    try:
        parsed = json.loads(cleaned)
        if "function_call" in parsed:
            call = parsed["function_call"]
            return execute_function_call(call["name"], call["arguments"])
    except json.JSONDecodeError:
        pass

    try:
        context = {
            "deepseek_api": deepseek_api,
            "chatgpt_api": chatgpt_api,
            "path_to_input_data": path_to_input_data,
            "path_to_process": path_to_process,
            "path_to_output": path_to_output,
            "path_to_task_instruct_json": path_to_task_instruct_json
        }
        parsed = eval(cleaned, context)
        if isinstance(parsed, dict) and "function_call" in parsed:
            call = parsed["function_call"]
            return execute_function_call(call["name"], call["arguments"])
    except Exception:
        pass

    return f"Ответ ИИ (не вызвали функцию):\n{raw}"
# endregion


def main():
    model = deepseek_api  # chatgpt_api

    request_text = "Преобразуй все документы из папки input_data и обработай их через ИИ в 1 потоке"
    result = run_function_agent(
        model=model,
        instruction_json_path=path_to_func_instruct_json,
        user_request=request_text
    )
    print(result)

if __name__ == "__main__":
    main()
