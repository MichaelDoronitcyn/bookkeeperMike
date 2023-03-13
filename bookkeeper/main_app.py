"""
главное приложение
"""
import sys

from PyQt6.QtWidgets import QApplication

from bookkeeper.view.main_view import MainApplication

app = QApplication(sys.argv)
ex_app = MainApplication()
sys.exit(app.exec())
