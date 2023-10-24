import re

import requests

from models.absclasses import AbstractApi
from settings import QUANTITY_VACANCIES, MIN_SALARY


class HeadHunterApi(AbstractApi):
    """ Класс для работы с HeadHunter API """

    _url = r'https://api.hh.ru/vacancies/'
    _per_page = QUANTITY_VACANCIES
    _salary = MIN_SALARY

    def get_vacancy_by_id(self, id_: int) -> dict:
        """ Метод для получения вакансии по id """

        query_params = {
            'page': 0,
            'per_page': self._per_page,
            'employer_id': str(id_),
            'salary': self._salary,
            'only_with_salary': True,
        }

        response = requests.get(self._url, params=query_params)
        if response.status_code != 200:
            raise ConnectionError(f'HeadHunter API error, status code: {response.status_code}')

        return response.json()

    def format_data(self, row_data: dict) -> list[dict]:
        """ Метод для форматирования данных """

        result = []

        for item in row_data['items']:

            requirements = item['snippet']['responsibility']
            requirements = re.sub(r'<.*?>', '', requirements) if requirements else 'Не указано'

            vacancy = {
                'vacancy_name': item['name'],
                'vacancy_id': int(item['id']),
                'company_name': item['employer']['name'],
                'company_id': int(item['employer']['id']),
                'url': item['alternate_url'],
                'salary': item['salary']['from'] or item['salary']['to'],
                'experience': item['experience']['name'],
                'requirements': requirements,
                'city': item['area']['name'],
                'city_id': int(item['area']['id']),
            }
            result.append(vacancy)

        return result
