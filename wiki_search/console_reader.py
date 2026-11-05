"""Считывание пользовательского ввода с консоли."""

from collections.abc import Callable

from wiki_search.errors import ExitRequested


class ConsoleReader:
    """Считывает поисковый запрос и номер выбранной статьи."""

    EXIT_COMMAND = ":q"
    BACK_CHOICE = 0

    def __init__(self, read_line: Callable[[str], str] = input) -> None:
        self._read_line = read_line

    def read_query(self) -> str:
        """Возвращает запрос без крайних пробелов (может быть пустым)."""
        return self._read(
            f"\nВведите запрос ({self.EXIT_COMMAND} - выход): "
        )

    def read_choice(self, results_count: int) -> int | None:
        """Возвращает номер от 0 до results_count или None, если он неверен."""
        text = self._read(
            f"Номер статьи (1-{results_count}), "
            f"{self.BACK_CHOICE} - новый поиск, "
            f"{self.EXIT_COMMAND} - выход: "
        )
        return self._parse_choice(text, results_count)

    def _read(self, prompt: str) -> str:
        try:
            text = self._read_line(prompt).strip()
        except (EOFError, RuntimeError) as error:
            # RuntimeError: у процесса нет stdin или stdout.
            raise ExitRequested from error
        if text.lower() == self.EXIT_COMMAND:
            raise ExitRequested
        return text

    @staticmethod
    def _parse_choice(text: str, results_count: int) -> int | None:
        if not text.isdecimal():
            return None
        try:
            choice = int(text)
        except ValueError:  # Python ограничивает длину числа в строке.
            return None
        return choice if 0 <= choice <= results_count else None
