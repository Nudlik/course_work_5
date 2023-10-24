from models.absclasses import AbstractView
from prettytable import PrettyTable


class View(AbstractView):
    """ Класс для отображения данных в консоль """

    def __init__(self, columns: list, data: list[tuple]):
        self.columns = columns
        self.data = data

    def show(self) -> None:
        """ Метод для отображения данных в консоль """

        if not self.data:
            print('No data to show')
            return
        table = PrettyTable()
        table.field_names = self.columns
        table.add_rows(self.data)
        print(table)
