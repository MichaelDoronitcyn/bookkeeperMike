"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    pass


@dataclass(slots=True)
class Expense(Base):
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    __tablename__="expanseTable"

    amount: int
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

