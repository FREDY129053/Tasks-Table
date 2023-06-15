import sys
import mysql
import other_classes

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
import foreach_table_window
#

from log_in_window import *
from sign_up_window import *
from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QFileDialog
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
            "database": "tasks_table_copy",
        }
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)

class AddColumn(QWidget):
    def __init__(self, table_id):
        super(AddColumn, self).__init__()
        loadUi("Users_Interfaces/REDACTOR_ZAPIS_TEST.ui", self)
        global name_table
        name_table = foreach_table_window.curr()
        self.table_id = table_id
        self.setWindowTitle("Добавить столбец")

        self.add_column_btn.clicked.connect(self.add_column)

    def add_column(self):
        name_column = self.name_adding.text()

        cursor.execute(f"INSERT INTO columns (board_id, name) VALUES({self.table_id}, '{name_column}')")
        database.commit()

        self.close()