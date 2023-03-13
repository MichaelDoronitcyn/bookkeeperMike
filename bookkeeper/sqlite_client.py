"""
Простой тестовый скрипт для терминала
"""
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.utils import read_tree

from bookkeeper.repository.sqlite_init import check_and_create
from bookkeeper.repository.sqlite_repository import SqliteRepository

check_and_create('mikeExpenses.sqlite')
sql_bud_repo = SqliteRepository[Budget]('mikeExpenses.sqlite', Budget(0))
sql_bud_repo.get_all()
sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', Category(''))
sql_exp_repo = SqliteRepository[Expense]('mikeExpenses.sqlite', Expense(0, 1))
#
cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

# создаем список категорий если только пустая база данных
if len(sql_cat_repo.get_all()) == 0:
    Category.create_from_tree(read_tree(cats), sql_cat_repo)

# Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*sql_cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*sql_exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = sql_cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        sql_exp_repo.add(exp)
        print(exp)
