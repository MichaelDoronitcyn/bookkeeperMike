import sys
from PyQt6.QtGui import QIcon, QStandardItem

from PyQt6.QtCore import (QDate, QDateTime, QSortFilterProxyModel, Qt,
                          QTime)
from PyQt6.QtGui import QStandardItemModel

from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QFormLayout, QPushButton, QDialog, QDialogButtonBox, QAbstractItemView)

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.budgetview import BudgetView
from bookkeeper.view.categoryview import CategoryView
from bookkeeper.view.expansesview import ExpansesView


class MainApplication(QWidget):
    FROM, SUBJECT, DATE = range(3)

    def __init__(self):
        super().__init__()

        self.expanses_view: ExpansesView = None
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
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.dataGroupBox = QGroupBox("Последние расходы")
        # self.dataView = CategoryView()  # QTreeView()

        data_layout = QVBoxLayout()
        # dataLayout.addWidget(self.dataView)
        self.expanses_view = ExpansesView()
        data_layout.addWidget(self.expanses_view)
        data_layout.addWidget(BudgetView())
        self.dataGroupBox.setLayout(data_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.dataGroupBox)
        main_layout.addWidget(self.get_insert_wd())

        self.setLayout(main_layout)

        self.show()

    def get_insert_wd(self)->QWidget:
        wid = QWidget()
        form=QFormLayout()


        form.addRow("Расходы", self.expanses )
        form.addRow("Комментарий", self.comment)
        form.addRow( self.but_category )
        form.addRow("Категория", self.category)
        form.addRow(self.but_new)
        wid.setLayout(form)
        return wid

    def button_clicked(self, s):
        print("click", s)

        dlg = CustomDialog()
        if dlg.exec():
            print("in")
            for ix in dlg.tree.selectedIndexes():
                text = ix.data()  # or ix.data()
            print(text)
            self.category.setText(text)
        else:
            print("Cancel!")

    def button_new(self):
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
    def __init__(self):
        super().__init__()

        self.setWindowTitle("выбор категории")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.tree = CategoryView()
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.layout.addWidget( self.tree )
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)