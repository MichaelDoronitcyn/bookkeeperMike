import datetime

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.abstract_repository import T
# from dataclasses import dataclass
# from datetime import datetime
import sqlite3


# from bookkeeper.repository.sqlite_repository import SqliteRepository


def getFillInsert(a: T) -> str:
    rez = getAllNames(a)
    s = 'insert into ' + getattr(a, '__tablename__') + ' ('

    for i in rez:
        print(i, getattr(a, i))
        s += str(i) + ','
    s = s[:-1]
    s += ') values ('

    for i in rez:
        r = "0"
        if getattr(a, i) is None:
            r = '0'
        else:
            r = str(getattr(a, i))
        s += '"' + r + '",'
    s = s[:-1]
    s += ')'
    return (str(s))


def getAllNames(a: T) -> list[str]:
    rez = []
    for i in a.__annotations__:
        rez.append(i)

    rez.remove('pk')
    return (rez)


def createTable(a: T, nameOfTable: str) -> str:
    # create table if not exists dhcp (
    #     mac          text not NULL primary key,
    #     ip           text,
    #     vlan         text,
    #     interface    text
    # );

    sInit = f'create table if not exists {nameOfTable} ('
    # print(a.__dir__())
    print('....', a.__annotations__)
    startB = True
    for i in a.__dataclass_fields__:
        print(a.__dataclass_fields__[i].type)
        if not startB:
            sInit += ','
        if a.__dataclass_fields__[i].type is datetime.datetime:
            sInit += a.__dataclass_fields__[i].name + ' text'
        if a.__dataclass_fields__[i].type is str:
            sInit += a.__dataclass_fields__[i].name + ' text'
        if a.__dataclass_fields__[i].type is int:
            sInit += a.__dataclass_fields__[i].name + ' integer'
            # INTEGER PRIMARY KEY
            if a.__dataclass_fields__[i].name == 'pk':
                sInit += ' PRIMARY KEY'
        if a.__dataclass_fields__[i].type in [int | None]:
            sInit += a.__dataclass_fields__[i].name + ' integer'
        if a.__dataclass_fields__[i].type is float:
            sInit += a.__dataclass_fields__[i].name + ' real'
        if startB:
            startB = False
    sInit += ');'
    # print(sInit)
    return (sInit)


def checkAndCreate(db: str) -> None:
    conn = sqlite3.connect(db)
    c = conn.cursor()

    e = Expense(amount=100, category=1, comment='test')

    a = createTable(e, e.__tablename__)
    print(a)
    c.execute(a)

    print(e)

    e = Category("name", 0)
    a = createTable(e, e.__tablename__)
    print(a)
    c.execute(a)
    print(c)

    conn.commit()


if __name__ == '__main__':
    a = Category('aa', 0)
    print(getAllNames(a))

    print(getFillInsert(a))

    e = Expense(amount=100, category=1, comment='test')
    print(getFillInsert(e))
