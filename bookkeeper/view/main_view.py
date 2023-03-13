"""
создает главное окно
"""
from typing import Any

from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QGroupBox, QVBoxLayout, \
    QDialog, QDialogButtonBox, \
    QAbstractItemView, QFormLayout

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.budgetview import BudgetView
from bookkeeper.view.categoryview import CategoryView
from bookkeeper.view.expansesview import ExpansesView


class MainApplication(QWidget):
    """
     главное приложение
    """

    def __init__(self):
        super().__init__()
        self.expanses_view = Any
        self.data_group_box = Any
        self.title = 'Mike Dor'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.expanses = QLineEdit(self)
        self.expanses.setText('0')
        self.comment = QLineEdit(self)
        self.category = QLineEdit(self)
        self.category.setEnabled(False)

        self.but_category = QPushButton('Категория')
        self.but_category.clicked.connect(self.button_clicked)

        self.but_new = QPushButton('Записать')
        self.but_new.clicked.connect(self.button_new)

        self.init_ui()

    def init_ui(self):
        """
        инициализация юи
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.data_group_box = QGroupBox("Последние расходы")
        # self.dataView = CategoryView()  # QTreeView()

        data_layout = QVBoxLayout()
        # dataLayout.addWidget(self.dataView)
        self.expanses_view = ExpansesView()
        data_layout.addWidget(self.expanses_view)
        data_layout.addWidget(BudgetView())
        self.data_group_box.setLayout(data_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.data_group_box)
        main_layout.addWidget(self.get_insert_wd())

        self.setLayout(main_layout)

        self.show()

    def get_insert_wd(self) -> QWidget:
        """
        виджет кнопок управления
        """
        wid = QWidget()
        form = QFormLayout()

        form.addRow("Расходы", self.expanses)
        form.addRow("Комментарий", self.comment)
        form.addRow(self.but_category)
        form.addRow("Категория", self.category)
        form.addRow(self.but_new)
        wid.setLayout(form)
        return wid

    def button_clicked(self):
        """
        выбор названия категории
        """

        dlg = CustomDialog()
        if dlg.exec():
            text = ''
            for idx in dlg.tree.selectedIndexes():
                text = idx.data()  # or ix.data()
            self.category.setText(text)
        else:
            print("Cancel!")

    def button_new(self):
        """
        запись новых расходов
        """
        sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', Category(''))
        sql_cat_repo.get_all()
        cat = sql_cat_repo.get_all({'name': self.category.text()})[0]
        print(self.expanses.text())
        print(self.category.text())
        print(self.comment.text())
        cls_expense = Expense(int(self.expanses.text()), cat.pk)
        cls_expense.comment = self.comment.text()
        sql_exp_repo = SqliteRepository[Expense]('mikeExpenses.sqlite', cls_expense)
        sql_exp_repo.add(cls_expense)
        self.expanses_view.update_table()


class CustomDialog(QDialog):
    """
    диалог выбора категории
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("выбор категории")

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                           QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.tree = CategoryView()
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
