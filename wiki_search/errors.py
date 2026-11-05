"""Исключения программы."""


class ExitRequested(Exception):
    """Пользователь хочет завершить работу программы."""


class WikiSearchError(Exception):
    """Базовая ошибка; её текст можно показать пользователю."""


class NetworkError(WikiSearchError):
    """Не удалось получить ответ от сервера."""


class ApiError(WikiSearchError):
    """Сервер Википедии сообщил об ошибке в ответе."""


class ResponseFormatError(WikiSearchError):
    """Ответ сервера не удалось разобрать."""


class BrowserError(WikiSearchError):
    """Не удалось открыть страницу в браузере."""
