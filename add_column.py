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
            "database": "task_table",
        }
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)

class AddColumn(QWidget):
    def __init__(self):
        super(AddColumn, self).__init__()
        loadUi("Users_Interfaces/REDACTOR_ZAPIS_TEST.ui", self)
        global name_table
        name_table = foreach_table_window.curr()

        self.setWindowTitle("Добавить столбец")

        self.add_column_btn.clicked.connect(self.add_column)

    def add_column(self):
        name_column = self.name_adding.text()

        print(name_column)
        cursor.execute(f"SELECT columns_name FROM tables WHERE table_name = '{foreach_table_window.curr()}'")
        curr_name_db = cursor.fetchone()[0]
        curr_name = "" if curr_name_db is None else curr_name_db
        print(f"As = {curr_name}")
        if curr_name == "":
            add_to_table = name_column + ','
        else:
            add_to_table = curr_name + ','+ name_column
        print(add_to_table)
        print(foreach_table_window.curr())

        cursor.execute(f"UPDATE tables SET columns_name = '{add_to_table}' WHERE table_name = '{foreach_table_window.curr()}'")
        cursor.execute(f"UPDATE tables SET size_of_table = size_of_table + 1 WHERE table_name = '{foreach_table_window.curr()}'")
        database.commit()

        self.close()