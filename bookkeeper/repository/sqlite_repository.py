"""
Модуль описывает репозиторий, sqlite
"""
from copy import deepcopy
from itertools import count
from typing import Any, Generic

from bookkeeper.repository.abstract_repository import AbstractRepository, T

import sqlite3
from bookkeeper.repository.sqlite_init import getFillInsert
from bookkeeper.models.category import Category

class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, sqlite
    """

    def __init__(self, dbName, clsExample:T) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

        self.clsExample = clsExample
        self.create_connection(dbName)

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        sql = getFillInsert(obj)
        print(sql)
        c = self.conn.cursor()
        c.execute(sql)
        obj.pk = c.lastrowid
        print(c.lastrowid)
        # sql = 'select pk from '+ getattr(a, '__tablename__') + 'where'
        self.conn.commit()
        #теперь обновляем содержимое контейнера в памяти
        self.get_all()
        return obj.pk

    def get(self, pk: int) -> T | None:
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        fields = ''
        flx = []
        for i in self.clsExample.__annotations__:
            fields += i + ','
            flx.append(i)
        fields=fields[:-1]
        if where is None:
            self._container.clear()
            sql =  'select '+fields+' from '+self.clsExample.__tablename__
            print(sql)
            c = self.conn.cursor()
            c.execute(sql)
            rows = c.fetchall()
            rez = []
            for i in rows:
                rrr = deepcopy( self.clsExample )
                for idx,j in enumerate(i):
                    setattr(rrr,flx[idx], j)
                rez.append(rrr)
                self._container[rrr.pk] = rrr
                # print(i)
            return rez
        # заполняем массив в памяти из базы данных
        self.get_all()
        return [obj for obj in self._container.values()
                 if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        self._container.pop(pk)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)


if __name__ == '__main__':
    e = Category("")
    sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', e)
    print(*sql_cat_repo.get_all(), sep='\n')