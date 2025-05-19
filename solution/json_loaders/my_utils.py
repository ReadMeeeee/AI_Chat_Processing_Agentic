from os import path


def is_file_is_correct(path_to_file: str, file_format: str, is_file: bool = True, is_correct: bool = True) -> None:
    if is_file and not path.exists(path_to_file):
        raise FileNotFoundError(f"Файл не найден: {path_to_file}")

    if is_correct and not file_format.startswith("."):
        raise ValueError(f"Аргумент 'file_format' должен начинаться с точки. Получено: \"{file_format}\"")

    shaped_path = path.splitext(path.basename(path_to_file))
    format_of_file = shaped_path[1]

    if is_correct and format_of_file != file_format:
        raise ValueError(f"Ожидаемый формат файла - \"{file_format}\", получен - {format_of_file}")


# С использованием классов pydantic - стала избыточной
def is_subset_of(keys: set[str], data_position: dict) -> None:
    if not keys.issubset(data_position):
        raise KeyError(f"Инструкции не содержат необходимые ключи: {keys - set(data_position)}")
