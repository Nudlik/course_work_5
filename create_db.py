import psycopg2

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


def class_log(st):
    def inner(cls):
        methods = {k: v for k, v in cls.__dict__.items() if callable(v) and not k.startswith(st)}
        for k, v in methods.items():
            setattr(cls, k, connect(v))
        return cls

    return inner


@class_log('_')
class DbCreator:

    def __init__(self, database_name: str, database_params: dict) -> None:
        self.db_name = database_name
        self.db_params = database_params

    def _create_database(self) -> None:
        params = self.db_params.copy()
        params['database'] = 'postgres'

        conn = psycopg2.connect(**params)
        conn.autocommit = True

        cur = conn.cursor()
        query = f'''
        CREATE DATABASE {self.db_name}
        WITH
        OWNER = postgres
        ENCODING = 'UTF8'
        LC_COLLATE = 'Russian_Russia.1251'
        LC_CTYPE = 'Russian_Russia.1251'
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1
        IS_TEMPLATE = False;
        '''
        cur.execute(query)

        cur.close()
        conn.close()

    @staticmethod
    def create_table_companies() -> str:
        query = '''
        CREATE TABLE IF NOT EXISTS public.companies
        (
            company_id integer NOT NULL,
            name character varying(50) COLLATE pg_catalog."default" NOT NULL,
            CONSTRAINT companies_pkey PRIMARY KEY (company_id)
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.companies
            OWNER to postgres;
        '''
        return query

    @staticmethod
    def create_table_vacancies() -> str:
        query = '''
        CREATE TABLE IF NOT EXISTS public.vacancies
        (
            vacancy_id integer NOT NULL,
            company_id integer NOT NULL,
            experience character varying(30) COLLATE pg_catalog."default" NOT NULL,
            requirements text COLLATE pg_catalog."default" NOT NULL,
            salary integer NOT NULL,
            url character varying(100) COLLATE pg_catalog."default" NOT NULL,
            vacancy_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
            city_id integer NOT NULL,
            CONSTRAINT vacancies_pkey PRIMARY KEY (vacancy_id),
            CONSTRAINT cities_pk FOREIGN KEY (city_id)
                REFERENCES public.cities (city_id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            CONSTRAINT companies_pk FOREIGN KEY (company_id)
                REFERENCES public.companies (company_id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.vacancies
            OWNER to postgres;
        '''
        return query

    @staticmethod
    def create_table_cities() -> str:
        query = '''
        CREATE TABLE IF NOT EXISTS public.cities
        (
            city_id integer NOT NULL,
            name character varying(50) COLLATE pg_catalog."default" NOT NULL,
            CONSTRAINT cities_pkey PRIMARY KEY (city_id)
        )
        
        TABLESPACE pg_default;
        
        ALTER TABLE IF EXISTS public.cities
            OWNER to postgres;
        '''
        return query


def main():
    try:
        db = DbCreator('headhunter', DB_PARAMS)
        db._create_database()
        db.create_table_companies()
        db.create_table_cities()
        db.create_table_vacancies()
    except Exception as e:
        print(e)
    else:
        print('Database created')


if __name__ == '__main__':
    main()
