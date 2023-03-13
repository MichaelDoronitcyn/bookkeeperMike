"""
класс для просмотра категорий
"""
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTreeView

from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SqliteRepository


class CategoryView(QTreeView):
    """
    виджет просмотра Категорий
    """
    def __init__(self):
        super().__init__()

        self.setModel(self.get_model())
        self.setAlternatingRowColors(True)

    def get_model(self) -> QStandardItemModel:
        """
        данные для отображения в дереве
        """
        model = QStandardItemModel()
        sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', Category(""))
        categories = sql_cat_repo.get_all()
        cdict = {}
        # populate data
        for category in categories:
            parent1 = QStandardItem(category.name)
            cdict[category.pk] = parent1

        for category in categories:
            if category.parent > 0:
                parent1 = cdict[category.parent]
                parent1.appendRow(cdict[category.pk])
            # self.setFirstColumnSpanned(i, self.rootIndex(), True)
            if category.parent == 0:
                model.appendRow(cdict[category.pk])

        return model

    def set_model(self) -> None:
        """
        установить модель
        """
        return
