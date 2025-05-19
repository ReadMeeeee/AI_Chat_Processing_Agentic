# AI-агент по обработке документов и чатов

Небольшой агент на Python, который:

1. Конвертирует `.docx` файлы в JSON-чаты (`process_docxs_to_json`)
2. Обрабатывает JSON-чаты через AI по API, извлекая описание проблемы, ключевые слова и пошаговое решение (`chats_process`)
3. Запускает оба цикла через одну команду (`convert_and_process_dir`)

---

## Структура проекта

```
.
├── README.md
├── .env         # Ключи для ИИ по API
├── run.py       # Точка входа
├── solution/
│   ├── config/
│   │   ├── config.py                       # Пути к директориям, загрузка .env, инициализация AIModelAPI
│   │   ├── functions_instructions.json     # Инструкции по обработке основного запроса (function_calling prompt)
│   │   ├── functions_instructions_old.json # Старая (рабочая, недоработанная) версия functions_instructions.json
│   │   ├── task_instructions.json          # Инструкция по обработке чата
│   │   └── __init__.py
│   ├── docx_converter/
│   │   ├── pipeline_docx_to_json.py  # Функции для подготовки текста в порядке пайплайна
│   │   ├── models.py                 # Модели (pydantic-классы) для подготовки текста
│   │   ├── cleaner.py                # Функции очистки текста от мусора
│   │   ├── docx_processing.py        # Объединение пайплайна для файла или директории .docx
│   │   └── __init__.py
│   ├── chat_handler/
│   │   ├── models.py             # Модели (pydantic-классы) для подготовки запросов (запрос, AI API)
│   │   ├── chat_processing.py    # Функции обработки файла чата или директории .json
│   │   └── __init__.py
│   ├── json_loaders/
│   │   ├── models.py             # Модели (pydantic-классы) для извлчения и последующий работы с инструкциями
│   │   ├── my_utils.py           # load_instruction_solution, load_instruction_function_calling
│   │   ├── task_loader.py        # Загрузчик задания из .json в переменную
│   │   ├── json_data_loader.py   # Загрузчик инструкций
│   │   └── __init__.py
│   └── convert_and_process/
│       ├── convert_and_process_dir.py  # Функции подготовки .docx и обработки их по задаче (файл/ директория)
│       └── __init__.py
├── __init__.py
└── requirements.txt
```

---

## Основной цикл functiun_callingа на коленке:

1. `run.py` → `run_function_agent()`:

   * Загружает описание функций из JSON
   * Формирует prompt для LLM
   * Парсит ответ; если LLM вернул `function_call`, вызывает одну из локальных функций:
- `process_docxs_to_json`   → многопроцессная конвертация `.docx` в JSON
- `chats_process`           → многопроцессная отправка чатов в LLM и запись решения
- `convert_and_process_dir` → объединение обоих шагов

---

## Примечания

* Все пути к директориям (`input_data`, `to_process`, `solutions`) и файл инструкций (`task_instructions.json`, `functions_instructions.json`) задаются в `solution/config/config.py`.
* Если LLM возвращает некорректный JSON, скрипт выводит сырой ответ.
* Используется Pydantic v2 для валидации JSON-инструкций и API-моделей.
* Внесены другие мелкие оптимизации в сравнении с предыдущими проектами (`Practice`, `Practice_unified_structure`).
---
