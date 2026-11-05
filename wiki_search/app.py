"""Сценарий работы программы."""

from wiki_search.api_client import WikipediaClient
from wiki_search.browser import BrowserOpener
from wiki_search.console_printer import ConsolePrinter
from wiki_search.console_reader import ConsoleReader
from wiki_search.errors import ExitRequested, WikiSearchError
from wiki_search.models import SearchResult
from wiki_search.response_parser import SearchResponseParser


class WikipediaSearchApp:
    """Связывает ввод, запрос к API, разбор ответа, вывод и браузер."""

    def __init__(
        self,
        reader: ConsoleReader,
        client: WikipediaClient,
        parser: SearchResponseParser,
        printer: ConsolePrinter,
        browser: BrowserOpener,
    ) -> None:
        self._reader = reader
        self._client = client
        self._parser = parser
        self._printer = printer
        self._browser = browser

    def run(self) -> None:
        """Обрабатывает запросы, пока пользователь не завершит работу."""
        self._printer.show_welcome()
        try:
            while True:
                self._process_query()
        except (ExitRequested, KeyboardInterrupt):
            self._printer.show_goodbye()

    def _process_query(self) -> None:
        query = self._reader.read_query()
        if not query:
            self._printer.show_error("запрос не может быть пустым.")
            return
        if len(query) > WikipediaClient.MAX_QUERY_LENGTH:
            self._printer.show_error(
                "запрос не может быть длиннее "
                f"{WikipediaClient.MAX_QUERY_LENGTH} символов."
            )
            return
        try:
            results = self._parser.parse(self._client.search(query))
            if not results:
                self._printer.show_message("По запросу ничего не найдено.")
                return
            self._printer.show_results(results)
            selected = self._ask_for_article(results)
            if selected is not None:
                url = self._client.article_url(selected.page_id)
                self._browser.open(url)
                self._printer.show_message(f"Открываю «{selected.title}».")
        except WikiSearchError as error:
            self._printer.show_error(str(error))

    def _ask_for_article(
        self, results: list[SearchResult]
    ) -> SearchResult | None:
        """Спрашивает номер, пока он не окажется корректным."""
        while True:
            choice = self._reader.read_choice(len(results))
            if choice is None:
                self._printer.show_error("введите номер из списка.")
            elif choice == ConsoleReader.BACK_CHOICE:
                return None
            else:
                return results[choice - 1]
