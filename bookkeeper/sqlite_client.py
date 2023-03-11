"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.utils import read_tree

from bookkeeper.repository.sqlite_init import checkAndCreate
from bookkeeper.repository.sqlite_repository import SqliteRepository

# cat_repo = MemoryRepository[Category]()
# exp_repo = MemoryRepository[Expense]()

checkAndCreate('mikeExpenses.sqlite')

clsCategory = Category('')
sql_cat_repo = SqliteRepository[Category]('mikeExpenses.sqlite', clsCategory)

clsExpense = Expense(0, 1)
sql_exp_repo = SqliteRepository[Expense]('mikeExpenses.sqlite', clsExpense)
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
