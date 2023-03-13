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
        self.vBox = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Дата", "Сумма", "Категория", "Комментарий"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vBox.addWidget(self.table)
        self.setLayout(self.vBox)
        self.update_table()

    def update_table(self):
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
                               QTableWidgetItem(exp.added_date.__str__()))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(exp.amount)))
            name = sql_cat_repo.get(exp.category).name
            self.table.setItem(row_position, 2, QTableWidgetItem(name))
            self.table.setItem(row_position, 3, QTableWidgetItem(exp.comment))
