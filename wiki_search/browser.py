"""Открытие страниц в браузере."""

import webbrowser

from wiki_search.errors import BrowserError


class BrowserOpener:
    """Открывает ссылку в браузере по умолчанию."""

    def open(self, url: str) -> None:
        """Открывает ссылку; при неудаче выбрасывает BrowserError."""
        try:
            opened = webbrowser.open(url)
        except (webbrowser.Error, OSError) as error:
            raise BrowserError(self._failure_message(url)) from error
        if not opened:
            raise BrowserError(self._failure_message(url))

    @staticmethod
    def _failure_message(url: str) -> str:
        return f"не удалось открыть браузер. Ссылка на статью: {url}"
