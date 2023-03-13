"""
Модуль описывает утилиты для организации работы с sqlite
"""
import datetime
import sqlite3
from typing import Tuple

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.abstract_repository import T
# from dataclasses import dataclass
# from datetime import datetime



# from bookkeeper.repository.sqlite_repository import SqliteRepository


def get_fill_insert(obj: T) -> str:
    """
    генерирует строку insert для sql
    """
    rez = get_all_names(obj)
    sql = 'insert into ' + getattr(obj, '__tablename__') + ' ('

    for i in rez:
        print(i, getattr(obj, i))
        sql += str(i) + ','
    sql = sql[:-1]
    sql += ') values ('

    for i in rez:
        rez_str = "0"
        if getattr(obj, i) is None:
            rez_str = '0'
        else:
            rez_str = str(getattr(obj, i))
        sql += '"' + rez_str + '",'
    sql = sql[:-1]
    sql += ')'
    return str(sql)


def get_all_names(obj: T) -> list[str]:
    """
    заполняет массив названия полей и удалет поле pk
    """
    rez = []
    for i in obj.__annotations__:
        rez.append(i)

    rez.remove('pk')
    return rez


def create_table(obj: T, name_of_table: str) -> str:
    """
    создает таблицу если она отсутсвует
    """
    # create table if not exists dhcp (
    #     mac          text not NULL primary key,
    #     ip           text,
    #     vlan         text,
    #     interface    text
    # );

    s_init = f'create table if not exists {name_of_table} ('
    # print(a.__dir__())
    print('....', obj.__annotations__)
    start_b = True
    for i in obj.__dataclass_fields__:
        print(obj.__dataclass_fields__[i].type)
        if not start_b:
            s_init += ','
        if obj.__dataclass_fields__[i].type is datetime.datetime:
            s_init += obj.__dataclass_fields__[i].name + ' text'
        if obj.__dataclass_fields__[i].type is str:
            s_init += obj.__dataclass_fields__[i].name + ' text'
        if obj.__dataclass_fields__[i].type is int:
            s_init += obj.__dataclass_fields__[i].name + ' integer'
            # INTEGER PRIMARY KEY
            if obj.__dataclass_fields__[i].name == 'pk':
                s_init += ' PRIMARY KEY'
        if obj.__dataclass_fields__[i].type in [int | None]:
            s_init += obj.__dataclass_fields__[i].name + ' integer'
        if obj.__dataclass_fields__[i].type is float:
            s_init += obj.__dataclass_fields__[i].name + ' real'
        if start_b:
            start_b = False
    s_init += ');'
    # print(s_init)
    return s_init


def check_and_create(data_base_name: str) -> None:
    """
    формирует файл для работы sqlite и создает таблицы
    """
    connection = sqlite3.connect(data_base_name)
    cursor = connection.cursor()

    obj = Expense(amount=100, category=1, comment='test')

    sql = create_table(obj, obj.__tablename__)
    print(sql)
    cursor.execute(sql)

    # print(obj)

    category = Category("name", 0)
    sql = create_table(obj, category.__tablename__)
    print(sql)
    cursor.execute(sql)
    print(cursor)

    connection.commit()

def get_fields_names( obj : T) -> Tuple[str, list[str]]:
    """
    возвращает  именя полей и список полей в классе
    """
    fields = ''
    flx = []
    for row in obj.__annotations__:
        fields += row + ','
        flx.append(row)
    fields = fields[:-1]
    return fields, flx



if __name__ == '__main__':
    category = Category('aa', 0)
    print(get_all_names(category))

    print(get_fill_insert(category))

    expenses = Expense(amount=100, category=1, comment='test')
    print(get_fill_insert(expenses))
