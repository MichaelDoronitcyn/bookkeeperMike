import datetime

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
import dataclasses
from datetime import datetime
import sqlite3

# from bookkeeper.repository.sqlite_repository import SqliteRepository



def getFillInsert( a ):
    rez=getAllNames(a)
    s = 'insert into ' + getattr(a, '__tablename__') + ' ('

    for i in rez:
        print(i, getattr(a, i))
        s += i + ','
    s = s[:-1]
    s += ') values ('

    for i in rez:
        r = "0"
        if getattr(a, i) is None:
            r='0'
        else:
            r = str(getattr(a, i))
        s += '"' + r + '",'
    s = s[:-1]
    s += ')'
    return(s)
def getAllNames( a ):
    rez=[]
    for i in a.__dataclass_fields__:
        rez.append( a.__dataclass_fields__[i].name)

    rez.remove('pk')
    return(rez)
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
    c.execute('drop table ' + e.__tablename__)
    conn.commit()


    a = createTable(e, e.__tablename__)
    c.execute(a)
    print(a)
    print(e)

    e = Category("name",0)
    a = createTable(e, e.__tablename__)
    print(a)
    c.execute(a)
    print(c)

    conn.commit()

if __name__ == '__main__':

    a = Category('aa',0)
    print(getAllNames(a))

    print( getFillInsert(a) )

    e = Expense(amount=100, category=1, comment='test')
    print(getFillInsert(e))