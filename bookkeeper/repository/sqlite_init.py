import datetime

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
import dataclasses
from datetime import datetime
import sqlite3

from bookkeeper.repository.sqlite_repository import SqliteRepository



def createTable( a, nameOfTable:str ):


    # create table if not exists dhcp (
    #     mac          text not NULL primary key,
    #     ip           text,
    #     vlan         text,
    #     interface    text
    # );


    sInit = f'create table if not exists {nameOfTable} ('
    #print(a.__dir__())
    print(a.__dataclass_fields__)
    startB = True;
    for i in a.__dataclass_fields__:
        print(a.__dataclass_fields__[i].type)
        if not startB :
            sInit +=','
        if a.__dataclass_fields__[i].type is datetime:
            sInit += a.__dataclass_fields__[i].name + ' text'
        if a.__dataclass_fields__[i].type is str:
            sInit += a.__dataclass_fields__[i].name + ' text'
        if a.__dataclass_fields__[i].type is int:
            sInit += a.__dataclass_fields__[i].name + ' integer'
            # INTEGER PRIMARY KEY
            if a.__dataclass_fields__[i].name == 'pk':
                sInit += ' PRIMARY KEY'
        if a.__dataclass_fields__[i].type in [ int | None]:
            sInit += a.__dataclass_fields__[i].name + ' integer'
        if a.__dataclass_fields__[i].type is float:
            sInit += a.__dataclass_fields__[i].name + ' real'
        if startB:
            startB = False
    sInit += ');'
    # print(sInit)
    return (sInit)


def checkAndCreate( db ):
    conn = sqlite3.connect('mikeExpenses.sqlite')
    c = conn.cursor()

    e = Expense(amount=100, category=1, comment='test' )
    a = createTable(e, e.__tablename__)
    c.execute(a)
    print(a)
    print(e)

    e = Category("name",0)
    a = createTable(e, e.__tablename__)
    print(a)
    c.execute(a)
    print(e)

    conn.commit()