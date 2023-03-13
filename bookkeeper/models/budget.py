"""
Описан класс, представляющий ,бюджет
"""

from dataclasses import dataclass


@dataclass
class Budget:
    """

    pk - id записи в базе данных
    """

    __tablename__ = "budgetTable"

    amount: int

    pk: int = 0
