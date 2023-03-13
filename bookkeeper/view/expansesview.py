"""
класс просмотра расходов
"""
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHeaderView


class ExpansesView(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.vBox = QVBoxLayout()

        self.init_ui()


    def init_ui(self):

        self.table.setRowCount(5)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Дата", "Сумма", "Категория", "Комментарий"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vBox.addWidget(self.table)
        self.setLayout(self.vBox)
