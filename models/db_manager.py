
import psycopg2

from models.absclasses import AbstractDataBase
from settings import DB_PARAMS


class DBManager(AbstractDataBase):

    def __init__(self, database_name: str, database_params: dict) -> None:
        self.db_name = database_name
        self.db_params = database_params

    def insert_data_to_db(self):
        pass

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass


if __name__ == '__main__':
    db = DBManager('headhunter', DB_PARAMS)
