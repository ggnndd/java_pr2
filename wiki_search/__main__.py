"""Точка входа: python -m wiki_search."""

import io
import sys

from wiki_search.api_client import WikipediaClient
from wiki_search.app import WikipediaSearchApp
from wiki_search.browser import BrowserOpener
from wiki_search.console_printer import ConsolePrinter
from wiki_search.console_reader import ConsoleReader
from wiki_search.response_parser import SearchResponseParser


def configure_console() -> None:
    """Не даёт символам вне кодировки консоли завершить программу."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        # Потока может не быть (None), либо он может быть нестандартным (IDLE).
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(errors="replace")


def main() -> None:
    """Собирает объекты программы и запускает её."""
    configure_console()
    WikipediaSearchApp(
        reader=ConsoleReader(),
        client=WikipediaClient(),
        parser=SearchResponseParser(),
        printer=ConsolePrinter(),
        browser=BrowserOpener(),
    ).run()


if __name__ == "__main__":
    main()
