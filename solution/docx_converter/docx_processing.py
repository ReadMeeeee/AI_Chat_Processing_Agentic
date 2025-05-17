from os import makedirs, listdir
from concurrent.futures import ProcessPoolExecutor, as_completed
from pipeline_docx_to_json import (load_docx_from_project,
                                                           convert_from_docx,
                                                           format_chat,
                                                           write_chat_to_json
                                                           )


# Вот для этой функции можно сделать распараллеливание путем запуска нескольких интерпретаторов
def process_docx_to_json(file_path: str, output_dir: str = "to_process") -> None:
    """
    Обрабатывает docx-файл в json-файл в каталоге output_dir.
    Использует цепочку: load - convert - format - write.

    :param file_path: Путь к файлу для обработки
    :param output_dir: Путь к директории хранения результатов. По умолчанию /to_process
    """

    makedirs(output_dir, exist_ok=True)

    try:
        docx_data = load_docx_from_project(file_path)
        chat = convert_from_docx(docx_data)
        formatted_chat = format_chat(chat)
        write_chat_to_json(formatted_chat, output_dir)

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}\n{100 * '-'}")


def process_docxs_to_json(input_dir: str, output_dir: str = "to_process", threads: int = 1) -> None:
    """
    Обрабатывает в директории docx-файлы в json-файлы в каталог output_dir.
    Использует цепочку: load - convert - format - write.

    :param input_dir: Путь к директории с .docx для обработки
    :param output_dir: Путь к директории хранения результатов. По умолчанию /to_process
    :param threads: Количества потоков для обработки. По умолчанию 1
    """

    files = listdir(input_dir)

    if threads <= 1:
        for filename in files:
            process_docx_to_json(f"{input_dir}\\{filename}", output_dir=output_dir)
        return

    with ProcessPoolExecutor(max_workers=threads) as executor:                                # Использование файла по циклу файла из файлов
        futures = {executor.submit(process_docx_to_json, f"{input_dir}\\{filename}", output_dir): filename for filename in files}
                # Для каждой задачи 'process_docx' есть свой файл 'filename'
        for future in as_completed(futures):
        # Для каждого ожидаемого объекта - подождать объект и попробовать извлечь результат
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Ошибка при обработке {file}: {e}")



def main():
    from solution.config import path_to_input_data, path_to_process


    # Из-за накладных расходов на подготовку пула потоков - 
    # при небольшом объеме входных данных для обработки лучше не использовать многопоток
    process_docxs_to_json(path_to_input_data, path_to_process)



if __name__ == "__main__":
    main()

