"""
класс просмотра расходов
"""
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem

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
        self.table.setHorizontalHeaderLabels(["Дата", "Сумма", "Категория", "Комментарий"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vBox.addWidget(self.table)
        self.setLayout(self.vBox)
        self.update_table()

    def update_table(self):
        cls_expense = Expense(0, 1)
        sql_exp_repo = SqliteRepository[Expense]('mikeExpenses.sqlite', cls_expense)
        expances = sql_exp_repo.get_all()
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
        for exp in expances:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(exp.added_date))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(exp.amount)))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(exp.category)))
            self.table.setItem(row_position, 3, QTableWidgetItem(exp.comment))
