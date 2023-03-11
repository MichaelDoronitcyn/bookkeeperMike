"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.utils import read_tree
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
import dataclasses_sql

cat_repo = MemoryRepository[Category]()
exp_repo = MemoryRepository[Expense]()

# Connect to database
engine = sqlalchemy.create_engine("sqlite:///test.db")
metadata = sqlalchemy.MetaData()
#metadata
metadata.create_all(bind=engine)
# metadata.reflect()



# Insert
car = Expense(amount=100, category=1, expense_date=datetime.now(),
                added_date=datetime.now(), comment='test', pk=1)
# a = inspect(car)
Session = sessionmaker(bind=engine)
session = Session()

session.add( car )
session.commit()

# dataclasses_sql.insert(metadata, car, check_exists=True)

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
