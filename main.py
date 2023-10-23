from pprint import pprint

from models.api_hh import HeadHunterApi
from models.db_manager import DBManager
from settings import DB_PARAMS, COMPANIES


def main():
    api = HeadHunterApi()
    db = DBManager('headhunter', DB_PARAMS)

    for id_, name in COMPANIES:
        row_data = api.get_vacancy_by_id(id_)
        format_data = api.format_data(row_data)
        # pprint(format_data)



if __name__ == '__main__':
    main()