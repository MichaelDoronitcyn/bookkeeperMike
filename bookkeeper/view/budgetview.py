"""
класс просмотра бюджета
"""
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem


class BudgetView(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.vBox = QVBoxLayout()

        self.init_ui()


    def init_ui(self):

        self.table.setRowCount(3)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["", "Сумма", "Бюджет"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vBox.addWidget(self.table)
        self.setLayout(self.vBox)
        self.table.setItem(0, 0, QTableWidgetItem("День"))
        self.table.setItem(0, 2, QTableWidgetItem("1000"))
        self.table.setItem(1, 0, QTableWidgetItem("Неделя"))
        self.table.setItem(1, 2, QTableWidgetItem("7000"))
        self.table.setItem(2, 0, QTableWidgetItem("Месяц"))
        self.table.setItem(2, 2, QTableWidgetItem("30000"))
        self.setMaximumHeight(150)