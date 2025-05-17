from os import path
from json import loads, JSONDecodeError

from solution.models import LLMRequest, ProblemWithSolution
from solution.json_loaders import load_task, load_instruction_solution


def chat_process(
        model: AIModelAPI,
        path_to_instruct_json: str,
        path_to_task_txt: str,
) -> ProblemWithSolution:

    name = path.splitext(path.basename(path_to_task_txt))[0]
    general_task = load_task(path_to_task_txt)
    instructions = load_instruction_solution(path_to_instruct_json)
    req = LLMRequest(instruction_block=instructions, task=general_task)

    try:
        result_text = model.get_response(req)
    except Exception as e:
        raise RuntimeError(f"Ошибка при обращении к ИИ: {e}")

    try:
        result_dict = loads(result_text)
    except JSONDecodeError as e:
        raise ValueError(f"Ответ ИИ не является корректным JSON: {e}\nОтвет: {result_text}")

    return ProblemWithSolution(
        name=name,
        description=result_dict.get("description", ""),
        keywords=result_dict.get("keywords", []),
        solution=result_dict.get("solution", "")
    )


def process_all_chats(
        model: {AIModelAPI, str, str},
        path_to_input: str,
        path_to_process: str,
        path_to_instruct: str,
        path_to_output: str
) -> None:

    company_chats = process_all_docs(path_to_input, output_dir=path_to_process)

    if not company_chats:
        print("Нет данных для обработки.")
        return None

    list_of_sol: list[ProblemWithSolution] = []
    for company in company_chats:
        task_filename = f"{company.company}.txt"
        path_to_task_txt = path.join(path_to_process, task_filename)

        try:
            sol = chat_process(
                model=model,
                path_to_instruct_json=path_to_instruct,
                path_to_task_txt=path_to_task_txt,
            )
            list_of_sol.append(sol)

        except FileNotFoundError:
            print(f"Файл не найден: {path_to_task_txt}")
        except Exception as e:
            print(f"Ошибка при обработке {company.company}: {e}")

    if list_of_sol:
        upload_data(json_solution_path=path_to_output, list_of_sol=list_of_sol)
    else:
        print("Нет решений для записи.")

    return None