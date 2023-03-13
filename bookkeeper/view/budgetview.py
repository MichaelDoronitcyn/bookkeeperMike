"""
класс просмотра бюджета
"""
import datetime

from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHeaderView, \
    QTableWidgetItem, QPushButton

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository


class BudgetView(QWidget):
    """
    просмотр бюджета
    """

    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.vertical_box = QVBoxLayout()
        self.but_update = QPushButton('Обновить')
        self.but_update.clicked.connect(self.update_sum)
        self.init_ui()

    def init_ui(self):
        """
         инит юи
        """
        self.table.setRowCount(3)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["", "Сумма", "Бюджет"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vertical_box.addWidget(self.table)
        self.vertical_box.addWidget(self.but_update)
        self.setLayout(self.vertical_box)
        sql_bud_repo = SqliteRepository[Budget]('mikeExpenses.sqlite', Budget(0))
        sql_bud_repo.get_all()
        self.table.setItem(0, 0, QTableWidgetItem("День"))
        bud1 = sql_bud_repo.get(1)
        bud2 = sql_bud_repo.get(2)
        bud3 = sql_bud_repo.get(3)
        self.table.setItem(0, 2, QTableWidgetItem(str(bud1.amount)))
        self.table.setItem(1, 0, QTableWidgetItem("Неделя"))
        self.table.setItem(1, 2, QTableWidgetItem(str(bud2.amount)))
        self.table.setItem(2, 0, QTableWidgetItem("Месяц"))
        self.table.setItem(2, 2, QTableWidgetItem(str(bud3.amount)))
        self.setMaximumHeight(150)
        self.update_sum()

    def update_sum(self):
        """
        обнвление и рассчет сумм
        """
        sql_exp_repo = SqliteRepository[Expense]('mikeExpenses.sqlite', Expense(0, 0))
        exps = sql_exp_repo.get_all()
        today = datetime.datetime.now()

        sum_day = 0
        sum_week = 0
        sum_month = 0
        for exp in exps:
            datetime_object = datetime.datetime.fromisoformat(str(exp.expense_date))
            days = (today - datetime_object).days
            if days == 0:
                sum_day += exp.amount
            if days < 7:
                sum_week += exp.amount
            if days < 30:
                sum_month += exp.amount
            # print( days, type(days) )

        self.table.setItem(0, 1, QTableWidgetItem(str(sum_day)))
        self.table.setItem(1, 1, QTableWidgetItem(str(sum_week)))
        self.table.setItem(2, 1, QTableWidgetItem(str(sum_month)))
