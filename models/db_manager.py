import psycopg2

from models.absclasses import AbstractDataBase
from models.view import View
from settings import DB_PARAMS, DATABASE_CLEAR, DATABASE_DROP


# функция декоратор
def connect(func):
    def inner(self, *args, **kwargs):
        conn = psycopg2.connect(**DB_PARAMS)
        try:
            with conn:
                with conn.cursor() as cur:
                    query = func(*args, **kwargs)
                    cur.execute(query)

                    # вывод данных в консоль
                    if cur.description:
                        columns = [i.name for i in cur.description]
                        data = cur.fetchall()
                        viev = View(columns, data)
                        viev.show()

        except Exception as e:
            raise e
        finally:
            conn.close()

    return inner


# Декоратор для обертки калбл методов класса функцией connect
def class_dec_func(st: str):
    def inner(cls):
        methods = {k: v for k, v in cls.__dict__.items() if callable(v) and k.startswith(st)}
        for k, v in methods.items():
            setattr(cls, k, connect(v))
        return cls

    return inner


@class_dec_func('get_')
class DBManager(AbstractDataBase):
    """ Класс для работы с БД """

    db_clear = DATABASE_CLEAR
    db_drop = DATABASE_DROP

    def __init__(self, database_name: str, database_params: dict) -> None:
        self.db_name = database_name
        self.db_params = database_params

    def __del__(self):
        if self.db_clear:
            self.get_func_clear_db()
        elif self.db_drop:
            try:
                self.__drop_db()
            except Exception as e:
                print('База удалена, но возникла ошибка:', e)
            else:
                print('База удалена, без ошибок')
        else:
            del self

    @staticmethod
    def get_func_clear_db() -> str:
        """ Метод для очистки БД """

        query = '''
        TRUNCATE vacancies CASCADE;
        TRUNCATE cities CASCADE;
        TRUNCATE companies CASCADE;
        '''
        return query

    def __drop_db(self) -> None:
        """ Метод для удаления БД """

        params = self.db_params.copy()
        params['database'] = 'postgres'

        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{self.db_name}';")
        cur.execute(f'DROP DATABASE IF EXISTS {self.db_name}')

        cur.close()
        conn.close()

    def insert_data_to_db(self, data: dict) -> None:
        """ Метод для добавления данных в БД """

        city_id, city_name = data['city_id'], data['city']
        company_id, company_name = data['company_id'], data['company_name']
        vacancy_id, vacancy_name = data['vacancy_id'], data['vacancy_name']
        experience, requirements = data['experience'], data['requirements']
        salary, url = data['salary'], data['url']

        conn = psycopg2.connect(**self.db_params)
        try:
            with conn:
                with conn.cursor() as cur:

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
                    cur.execute(query, (vacancy_id,
                                        company_id,
                                        experience,
                                        requirements,
                                        salary,
                                        url,
                                        vacancy_name,
                                        city_id))
        except Exception as e:
            raise e
        else:
            print('data inserted to db')
        finally:
            conn.close()

    @staticmethod
    def get_companies_and_vacancies_count() -> str:
        """ Метод для получения кол-ва компаний и вакансий """

        query = '''
        SELECT name as "Название компании", COUNT(*) as "Кол-во вакансий"
        FROM companies c
        JOIN vacancies v USING(company_id)
        GROUP BY name
        '''
        return query

    @staticmethod
    def get_all_vacancies() -> str:
        """ Метод для получения всех вакансий """

        query = '''
        SELECT 
            c.name as "Название компании"
            , v.vacancy_name as "Название Вакансии"
            , v.salary as "ЗП"
            , v.experience as "Опыт"
            , v.url "Ссылка"
            , v.requirements as "Требования"
        FROM companies c
        JOIN vacancies v USING(company_id)
        '''
        return query

    @staticmethod
    def get_avg_salary() -> str:
        """ Метод для получения средней зарплаты """

        query = '''
        SELECT ROUND(AVG(salary), 2) as "Средняя ЗП"
        FROM vacancies
        '''
        return query

    @staticmethod
    def get_vacancies_with_higher_salary() -> str:
        """ Метод для получения вакансий с зарплатой выше средней """

        query = '''
        SELECT 
            c.name as "Название компании"
            , v.vacancy_name as "Название Вакансии"
            , v.salary as "ЗП"
            , v.experience as "Опыт"
            , v.url "Ссылка"
            , v.requirements as "Требования"
        FROM companies c
        JOIN vacancies v USING(company_id)
        WHERE v.salary >= (SELECT AVG(salary) FROM vacancies)
        '''
        return query

    @staticmethod
    def get_vacancies_with_keyword(word: str) -> str:
        """ Метод для поиска вакансий по ключевому слову """

        query = f'''
        SELECT 
            c.name as "Название компании"
            , v.vacancy_name as "Название Вакансии"
            , v.salary as "ЗП"
            , v.experience as "Опыт"
            , v.url "Ссылка"
            , v.requirements as "Требования"
        FROM companies c
        JOIN vacancies v USING(company_id)
        WHERE v.vacancy_name LIKE '%{word}%'
        '''
        return query
