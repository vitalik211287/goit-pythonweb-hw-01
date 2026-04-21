from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


@dataclass
class Book:
    title: str
    author: str
    year: int


class LibraryInterface(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> bool:
        pass

    @abstractmethod
    def get_books(self) -> list[Book]:
        pass


class Library(LibraryInterface):
    def __init__(self) -> None:
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)
        logging.info("Книгу '%s' додано", book.title)

    def remove_book(self, title: str) -> bool:
        for book in self._books:
            if book.title.lower() == title.lower():
                self._books.remove(book)
                logging.info("Книгу '%s' видалено", title)
                return True
        logging.info("Книгу '%s' не знайдено", title)
        return False

    def get_books(self) -> list[Book]:
        return self._books.copy()


class LibraryManager:
    def __init__(self, library: LibraryInterface) -> None:
        self.library = library

    def add_book(self, title: str, author: str, year: str) -> None:
        if not year.isdigit():
            logging.info("Рік має бути числом")
            return

        book = Book(title=title, author=author, year=int(year))
        self.library.add_book(book)

    def remove_book(self, title: str) -> None:
        self.library.remove_book(title)

    def show_books(self) -> None:
        books = self.library.get_books()

        if not books:
            logging.info("Бібліотека порожня")
            return

        for book in books:
            logging.info(
                "Title: %s, Author: %s, Year: %s",
                book.title,
                book.author,
                book.year,
            )


def main() -> None:
    library: LibraryInterface = Library()
    manager = LibraryManager(library)

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                manager.add_book(title, author, year)

            case "remove":
                title = input("Enter book title to remove: ").strip()
                manager.remove_book(title)

            case "show":
                manager.show_books()

            case "exit":
                logging.info("Завершення роботи програми")
                break

            case _:
                logging.info("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
