# Поиск по Википедии

Консольная программа: считывает поисковый запрос, выводит результаты поиска
по русской Википедии и открывает выбранную статью в браузере.

## Запуск

Нужен Python 3.10 или новее. Сторонние библиотеки не требуются.

```
python main.py
```

Введите запрос (до 300 символов), затем номер статьи из списка. `0` начинает
новый поиск, `:q` или Ctrl+C завершают программу.


## Структура

| Класс | Файл | Ответственность |
| --- | --- | --- |
| `ConsoleReader` | `wiki_search/console_reader.py` | ввод данных |
| `WikipediaClient` | `wiki_search/api_client.py` | обращение к API, ссылки на статьи |
| `SearchResponseParser` | `wiki_search/response_parser.py` | разбор ответа |
| `ConsolePrinter` | `wiki_search/console_printer.py` | вывод результатов и сообщений |
| `BrowserOpener` | `wiki_search/browser.py` | открытие статьи в браузере |
| `WikipediaSearchApp` | `wiki_search/app.py` | сценарий работы программы |
| `SearchResult` | `wiki_search/models.py` | данные одной статьи |

Исключения описаны в `wiki_search/errors.py`.
