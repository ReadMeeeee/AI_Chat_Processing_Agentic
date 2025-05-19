from solution.docx_converter import process_docxs_to_json
from solution.chat_handler.models import AIModelAPI
from solution.chat_handler import chats_process

from solution.config import path_to_input_data, path_to_process, path_to_output, path_to_task_instruct_json


def convert_and_process_dir(
        model: AIModelAPI,
        path_to_instructs: str = path_to_task_instruct_json,
        input_dir: str = path_to_input_data,
        to_process_dir = path_to_process,
        output_dir: str = path_to_output,
        threads: int = 1
        ) -> None:

    process_docxs_to_json(input_dir=input_dir, output_dir=to_process_dir,
                          threads=threads
                          )
    chats_process(model=model,
                  path_to_instruct_json=path_to_instructs,
                  input_dir=to_process_dir, output_dir=output_dir,
                  threads=threads
                  )
