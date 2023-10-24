import os

# кортеж с id и названием компаний, id брать тут -> https://hh.ru/employers_list
COMPANIES = (
    (1740, 'Яндекс'),
    (5008932, 'Яндекс Практикум'),
    (1057, 'Лаборатория Касперского'),
    (5361466, '63it'),
    (3027217, '78 IT'),
    (8932785, 'Adem IT'),
    (2180, 'Ozon'),
    (10413368, 'Айти компания'),
    (84585, 'Авито'),
    (78638, 'Тинькофф'),
)

# словарь с параметрами подключения к БД
DB_PARAMS = {
    'host': 'localhost',
    'port': 5432,
    'database': 'headhunter',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD'),
}

# параметры бд для очистки/удаления БД
DATABASE_CLEAR = False
DATABASE_DROP = False

# количество выводимых вакансий c каждой компании max = 100
QUANTITY_VACANCIES = 100
MIN_SALARY = 20000
