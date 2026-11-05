"""Модели данных программы."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    """Одна статья из результатов поиска."""

    page_id: int
    title: str
    snippet: str
