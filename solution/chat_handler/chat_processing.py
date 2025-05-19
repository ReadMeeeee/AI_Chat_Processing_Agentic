from os import path, makedirs, listdir
from json import loads, JSONDecodeError, dump
from concurrent.futures import ProcessPoolExecutor, as_completed

from solution.chat_handler.models import AIModelAPI, LLMRequest, ProblemWithSolution
from solution.json_loaders import load_task, load_instruction_solution


def chat_process(
        model: AIModelAPI,
        path_to_task: str,
        path_to_instruct_json: str,
        output_dir: str
) -> None:

    company_name, chat_text = load_task(path_to_task)
    instructions = load_instruction_solution(path_to_instruct_json)
    req = LLMRequest(instructions=instructions, task=chat_text)

    try:
        result_text = model.get_response(req)
    except Exception as e:
        raise RuntimeError(f"Ошибка при обращении к ИИ: {e}")

    try:
        result_dict = loads(result_text)
    except JSONDecodeError as e:
        raise ValueError(f"Ответ ИИ не является корректным JSON: {e}\nОтвет: {result_text}")

    output_file_path = path.join(output_dir, f"{company_name}.json")
    if not path.exists(output_dir):
        makedirs(output_dir)

    sol = ProblemWithSolution(
        name=company_name,
        description=result_dict.get("description", ""),
        keywords=result_dict.get("keywords", []),
        solution=result_dict.get("solution", "")
    )

    with open(output_file_path, "w", encoding="utf-8") as f:
        dump(sol.unit_it(), f, ensure_ascii=False, indent=4)


def chats_process(
        model: AIModelAPI,
        path_to_instruct_json: str,
        input_dir: str,
        output_dir: str,
        threads: int = 1
) -> None:
    files = listdir(input_dir)

    if threads <= 1:
        for filename in files:
            chat_process(
                model=model,
                path_to_instruct_json=path_to_instruct_json,
                path_to_task=path.join(input_dir, filename),
                output_dir=output_dir
            )
        return

    with ProcessPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(chat_process, model=model, path_to_task=path.join(input_dir, filename),
                                   path_to_instruct_json=path_to_instruct_json,
                                   output_dir=output_dir): filename for filename in files}

        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Ошибка при обработке {file}: {e}")
