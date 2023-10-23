import psycopg2

from models.absclasses import AbstractDataBase
from settings import DB_PARAMS


def connect(func):
    def inner(*args, **kwargs):
        conn = psycopg2.connect(**DB_PARAMS)
        try:
            with conn:
                with conn.cursor() as cur:
                    query = func()
                    cur.execute(query)
        except Exception as e:
            raise e
        finally:
            conn.close()

    return inner


def class_log(st: str):
    def inner(cls):
        methods = {k: v for k, v in cls.__dict__.items() if callable(v) and k.startswith(st)}
        for k, v in methods.items():
            setattr(cls, k, connect(v))
        return cls

    return inner


@class_log('get_')
class DBManager(AbstractDataBase):

    def __init__(self, database_name: str, database_params: dict) -> None:
        self.db_name = database_name
        self.db_params = database_params

    def insert_data_to_db(self, data: dict):
        conn = psycopg2.connect(**self.db_params)

        city_id, city_name = data['city_id'], data['city']
        company_id, company_name = data['company_id'], data['company_name']
        vacancy_id, vacancy_name = data['vacancy_id'], data['vacancy_name']
        experience, requirements = data['experience'], data['requirements']
        salary, url = data['salary'], data['url']

        cur = conn.cursor()
        query = 'INSERT INTO cities (city_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING'
        cur.execute(query, (city_id, city_name))

        query = 'INSERT INTO companies (company_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING'
        cur.execute(query, (company_id, company_name))

        query = '''
        INSERT INTO vacancies 
        (
            vacancy_id, 
            company_id, 
            experience, 
            requirements, 
            salary, 
            url, 
            vacancy_name, 
            city_id
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        '''
        cur.execute(query, (vacancy_id, company_id, experience, requirements, salary, url, vacancy_name, city_id))
        conn.commit()

        cur.close()
        conn.close()
        print('inserted')

    def get_companies_and_vacancies_count(self):
        query = '''
        
        '''
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
