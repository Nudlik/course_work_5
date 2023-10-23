import re
from pprint import pprint

import requests

from models.absclasses import AbstractApi


class HeadHunterApi(AbstractApi):
    _url = r'https://api.hh.ru/vacancies/'

    def get_vacancy_by_id(self, id_: int) -> dict:
        query_params = {
            'page': 0,
            'per_page': 10,
            'employer_id': str(id_),
            'salary': 20000,
            'only_with_salary': True,
        }

        response = requests.get(self._url, params=query_params)
        if response.status_code != 200:
            raise ConnectionError(f'HeadHunter API error, status code: {response.status_code}')

        return response.json()

    def format_data(self, row_data: dict) -> list[dict]:
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
                'salary': item['salary']['from'],
                'experience': item['experience']['name'],
                'requirements': requirements,
                'city': item['area']['name'],
                'city_id': int(item['area']['id']),
            }
            result.append(vacancy)

        return result


if __name__ == '__main__':
    api = HeadHunterApi()
    res = api.get_vacancy_by_id(1740)
    pprint(res)
