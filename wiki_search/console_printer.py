"""Вывод результатов и сообщений в консоль."""

from collections.abc import Sequence

from wiki_search.models import SearchResult


class ConsolePrinter:
    """Отвечает за всё, что программа показывает пользователю."""

    def show_welcome(self) -> None:
        """Выводит приветствие."""
        print("Поиск по русской Википедии")

    def show_goodbye(self) -> None:
        """Выводит прощание."""
        print("\nДо свидания!")

    def show_message(self, message: str) -> None:
        """Выводит сообщение."""
        print(message)

    def show_error(self, message: str) -> None:
        """Выводит сообщение об ошибке."""
        print(f"Ошибка: {message}")

    def show_results(self, results: Sequence[SearchResult]) -> None:
        """Выводит пронумерованный список статей."""
        print(f"\nПоказано статей: {len(results)}\n")
        for number, result in enumerate(results, start=1):
            print(f"{number}. {result.title}")
            if result.snippet:
                print(f"   {result.snippet}")
