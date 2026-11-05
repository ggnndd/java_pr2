"""Обращение к API Википедии."""

import http.client
import urllib.error
import urllib.parse
import urllib.request

from wiki_search.errors import NetworkError


class WikipediaClient:
    """Выполняет поисковые запросы и формирует ссылки на статьи."""

    DEFAULT_BASE_URL = "https://ru.wikipedia.org/w"
    DEFAULT_TIMEOUT_SECONDS = 10.0
    MAX_QUERY_LENGTH = 300  # Ограничение поиска Википедии.
    _HTTP_TOO_MANY_REQUESTS = 429
    # Википедия отклоняет запросы без осмысленного User-Agent.
    USER_AGENT = "WikiSearchConsole/1.0 (educational project)"

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout

    def search(self, query: str) -> bytes:
        """Возвращает необработанный JSON-ответ на поисковый запрос."""
        request = urllib.request.Request(
            self._build_search_url(query),
            headers={"User-Agent": self.USER_AGENT},
        )
        try:
            with urllib.request.urlopen(
                request, timeout=self._timeout
            ) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            error.close()
            raise NetworkError(
                self._describe_http_error(error.code)
            ) from error
        except (OSError, http.client.HTTPException) as error:
            raise NetworkError(
                "не удалось связаться с Википедией. "
                "Проверьте подключение к интернету."
            ) from error

    def article_url(self, page_id: int) -> str:
        """Возвращает ссылку на статью по её pageid."""
        return f"{self._base_url}/index.php?curid={page_id}"

    def _build_search_url(self, query: str) -> str:
        parameters = {
            "action": "query",
            "list": "search",
            "utf8": "",
            "format": "json",
            "srsearch": query,
        }
        # urlencode выполняет percent-encoding, как URLEncoder в Java.
        encoded = urllib.parse.urlencode(
            parameters, encoding="utf-8", errors="replace"
        )
        return f"{self._base_url}/api.php?{encoded}"

    @classmethod
    def _describe_http_error(cls, code: int) -> str:
        if code == cls._HTTP_TOO_MANY_REQUESTS:
            return "слишком много запросов. Подождите минуту и повторите."
        return f"сервер вернул код HTTP {code}."
