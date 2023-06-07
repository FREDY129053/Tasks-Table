import sys
import mysql

import foreach_table_window
import other_classes

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
#

from log_in_window import *
from sign_up_window import *
from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget
                             )
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import QCoreApplication
from mysql.connector import connect

db_config = {
    "user": "me",
    "password": "password",
    "host": "193.124.118.138",
    "database": "task_table",
}
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)


class AddNote(QWidget):
    def __init__(self):
        super(AddNote, self).__init__()
        loadUi("Users_Interfaces/TEST.ui", self)
        self.setWindowTitle("Добавление записи")

        self.add_zapis.clicked.connect(self.add_note)

    def add_note(self):
        table_id = int(foreach_table_window.current_id())
        name = self.name.text()
        description = self.text.text()
        author = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()

        cursor.execute(
            f"INSERT INTO columns (table_id, author, name, text, column_id) VALUES({table_id}, '{author.username}', '{name}', '{description}', 1)")
        database.commit()
        self.close()
