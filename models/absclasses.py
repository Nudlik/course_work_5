from abc import ABC, abstractmethod


class AbstractApi(ABC):

    @abstractmethod
    def get_vacancy_by_id(self, id_: int):
        pass

    @abstractmethod
    def format_data(self, row_data: dict) -> list:
        pass


class AbstractDataBase(ABC):

    @staticmethod
    @abstractmethod
    def get_companies_and_vacancies_count() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_all_vacancies() -> list:
        pass

    @staticmethod
    @abstractmethod
    def get_avg_salary() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_vacancies_with_higher_salary() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_vacancies_with_keyword(word: str) -> str:
        pass


class AbstractView(ABC):

    @abstractmethod
    def show(self) -> None:
        pass
