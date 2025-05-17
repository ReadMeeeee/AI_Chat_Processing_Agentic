def load_task():
    pass


def upload_solution(solutions_folder: str, sol: ProblemWithSolution) -> None:
    """
    Функция создает по пути json_solution_path json-файл с решениями

    :param solutions_folder: путь для сохранения решений в формате .json
    :param sol: решение типа ProblemWithSolution
    """
    filename = sol.name.join(".json")
    full_path = path.join(solutions_folder, filename)
    is_file_is_correct(full_path, ".json", is_file = False)


    str_to_write = {
        "company": sol.name,
        "description": sol.description,
        "keywords": sol.keywords,
        "solution": sol.solution
    }

    with open(full_path, "w", encoding="utf-8") as f:
        dump(str_to_write, f, ensure_ascii=False, indent=4)
