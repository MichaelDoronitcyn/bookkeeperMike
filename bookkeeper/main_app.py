import sys

from PyQt6.QtWidgets import QApplication

from bookkeeper.view.main_view import MainApplication

app = QApplication(sys.argv)
ex = MainApplication()
sys.exit(app.exec())
