"""Разбор JSON-ответа API Википедии."""

import html
import json
import re
from typing import Any

from wiki_search.errors import ApiError, ResponseFormatError
from wiki_search.models import SearchResult


class SearchResponseParser:
    """Преобразует ответ сервера в список результатов поиска."""

    _HTML_TAG = re.compile(r"<[^>]+>")
    _WHITESPACE = re.compile(r"\s+")
    _FORMAT_ERROR = "сервер вернул ответ в неожиданном формате."

    def parse(self, raw_response: bytes) -> list[SearchResult]:
        """Возвращает результаты поиска из тела ответа."""
        try:
            data = json.loads(raw_response)
        except (ValueError, RecursionError) as error:
            raise ResponseFormatError(self._FORMAT_ERROR) from error

        if isinstance(data, dict) and "error" in data:
            raise ApiError(self._describe_api_error(data["error"]))

        try:
            return [self._parse_item(item) for item in data["query"]["search"]]
        except (KeyError, TypeError, ValueError) as error:
            raise ResponseFormatError(self._FORMAT_ERROR) from error

    def _parse_item(self, item: Any) -> SearchResult:
        page_id = item["pageid"]
        title = item["title"]
        # bool - подкласс int, но pageid: true не является номером статьи.
        if (
            isinstance(page_id, bool)
            or not isinstance(page_id, int)
            or not isinstance(title, str)
        ):
            raise ValueError("Некорректные поля статьи")
        return SearchResult(
            page_id=page_id,
            title=title,
            snippet=self._clean_snippet(item.get("snippet", "")),
        )

    def _clean_snippet(self, snippet: str) -> str:
        """Убирает HTML-разметку, которой API выделяет совпадения."""
        text = html.unescape(self._HTML_TAG.sub("", snippet))
        return self._WHITESPACE.sub(" ", text).strip()

    @staticmethod
    def _describe_api_error(error: Any) -> str:
        details = error.get("info") if isinstance(error, dict) else None
        return f"ответ Википедии: {details or 'причина неизвестна'}"
