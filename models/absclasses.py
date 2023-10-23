from abc import ABC, abstractmethod


class AbstractApi(ABC):

    @abstractmethod
    def get_vacancy(self):
        pass

    @abstractmethod
    def format_data(self):
        pass


class AbstractDataBase(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass
