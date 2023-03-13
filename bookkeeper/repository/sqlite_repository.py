"""
Модуль описывает репозиторий, sqlite
"""
import sqlite3
from copy import deepcopy
from itertools import count
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T

from bookkeeper.repository.sqlite_init import get_fill_insert, get_fields_names
from bookkeeper.models.category import Category


class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, sqlite
    """

    def __init__(self, data_base_name: str, cls_example: T) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

        self.cls_example = cls_example
        self.create_connection(data_base_name)

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        sql = get_fill_insert(obj)
        print(sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        obj.pk = int(cursor.lastrowid)
        print(cursor.lastrowid)
        # sql = 'select pk from '+ getattr(a, '__tablename__') + 'where'
        self.connection.commit()
        # теперь обновляем содержимое контейнера в памяти
        self.get_all()
        return obj.pk

    def get(self, pk: int) -> T | None:
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        fields, flx = get_fields_names(self.cls_example)

        if where is None:
            self._container.clear()
            sql = 'select ' + fields + ' from ' + self.cls_example.__tablename__
            print(sql)
            cursor = self.connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            rez = []
            for row in rows:
                restored_cls = deepcopy(self.cls_example)
                for idx, j_row in enumerate(row):
                    setattr(restored_cls, flx[idx], j_row)
                rez.append(restored_cls)
                self._container[restored_cls.pk] = restored_cls
                # print(i)
            return rez
        # заполняем массив в памяти из базы данных
        self.get_all()
        return [obj for obj in self._container.values()
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        sql = f'update {self.cls_example.__tablename__} set '
        _, flx = get_fields_names(self.cls_example)
        for i in flx:
            sql += f' {i}="{getattr(obj, i)}",'
        sql = sql[:-1]  # удаляем запятую
        sql += f' where pk={obj.pk}'
        print(sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        # заполняем массив в памяти из базы данных
        self.get_all()
        # self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        sql = f'delete from {self.cls_example.__tablename__} where pk="{pk}" '
        print(sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        # заполняем массив в памяти из базы данных
        self.get_all()

    def create_connection(self, db_file: str)->None:
        """ create a database connection to a SQLite database """
        # self.connection = None
        try:
            self.connection = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Exception as exception:
            print(exception)


if __name__ == '__main__':
    category = Category("")
    sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', category)
    print(*sql_cat_repo.get_all(), sep='\n')
    category = sql_cat_repo.get(1)
    sql_cat_repo.update(category)

    category = Category("")

    sql_cat_repo.delete(sql_cat_repo.add(category))
