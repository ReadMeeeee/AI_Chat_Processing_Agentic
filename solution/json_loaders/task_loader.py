from json import load
from utils import is_file_is_correct


def load_task(path_to_task: str) -> tuple[str, str]:
    is_file_is_correct(path_to_task, '.json')
    with open(path_to_task, 'r', encoding="utf-8") as f:
        data = load(f)

    company = data['company']
    chat = data['chat']

    return company, chat


'''
def main():
    from solution.config import path_to_process
    from os import listdir


    files = listdir(path_to_process)
    print(path_to_process, '\n\n', files)

    company, chat = load_task(path_to_process + '\\' + files[0])
    print(company, '\n\n', chat)


if __name__ == '__main__':
    main()
'''
