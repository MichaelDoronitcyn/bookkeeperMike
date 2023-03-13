"""
класс просмотра расходов
"""
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, \
    QHeaderView, QTableWidgetItem

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository


class ExpansesView(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.vertical_box = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
        """
        инит юи
        """
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Дата", "Сумма", "Категория", "Комментарий"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vertical_box.addWidget(self.table)
        self.setLayout(self.vertical_box)
        self.update_table()

    def update_table(self):
        """
        обновление данных
        """
        sql_exp_repo = SqliteRepository[Expense]('mikeExpenses.sqlite', Expense(0, 1))
        sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', Category(''))
        sql_cat_repo.get_all()
        expances = sql_exp_repo.get_all()
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
        row_position = 0
        for exp in expances:
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0,
                               QTableWidgetItem(str(exp.added_date)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(exp.amount)))
            name = sql_cat_repo.get(exp.category).name
            self.table.setItem(row_position, 2, QTableWidgetItem(name))
            self.table.setItem(row_position, 3, QTableWidgetItem(exp.comment))
