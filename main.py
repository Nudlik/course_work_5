from models.api_hh import HeadHunterApi
from models.db_manager import DBManager
from settings import DB_PARAMS, COMPANIES


def ask_user(db: DBManager) -> None:
    """ Функция для взаимодействия с пользователем """

    menu = {
        '1': db.get_companies_and_vacancies_count,
        '2': db.get_all_vacancies,
        '3': db.get_avg_salary,
        '4': db.get_vacancies_with_higher_salary,
        '5': db.get_vacancies_with_keyword
    }

    while True:
        print(f'Выберите пункт меню:\n'
              f'1) получает список всех компаний и количество вакансий у каждой компании.\n'
              f'2) получает список всех вакансий с указанием названия компании, названия вакансии '
              f'и зарплаты и ссылки на вакансию.\n'
              f'3) получает среднюю зарплату по вакансиям.\n'
              f'4) получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
              f'5) получает список всех вакансий, в названии которых содержатся переданные в метод слова, '
              f'например python.\n'
              f'0) выход\n')

        user_input = input()
        if user_input == "0":
            break
        elif user_input in menu:
            if user_input == '5':
                word = input('Введите ключевое слово: ')
                menu.get(user_input)(word)
            else:
                menu.get(user_input)()
        else:
            print('Пункт меню не найден\n')


def main() -> None:
    """ Основная функция """

    api = HeadHunterApi()
    db = DBManager('headhunter', DB_PARAMS)

    for id_, name in COMPANIES:
        raw_data = api.get_vacancy_by_id(id_)
        format_data = api.format_data(raw_data)
        db.insert_data_to_db(format_data, name)

    ask_user(db)


if __name__ == '__main__':
    main()
