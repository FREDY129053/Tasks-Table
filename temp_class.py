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


class TempClass(QWidget):
    def __init__(self, name):
        super(TempClass, self).__init__()
        loadUi("Users_Interfaces/add_coauthors.ui", self)
        global window, index_table, name_curr
        name_curr = name
        window = foreach_table_window.window_for_action()
        index_table = foreach_table_window.current_id()

        if window == 1:
            self.setWindowTitle("Переименовать запись")
        elif window == 2:
            self.setWindowTitle("Изменить описание")
        elif window == 3:
            self.setWindowTitle("Изменить автора")

        self.add_coauthors_button.clicked.connect(self.add_coauthors)


    def add_coauthors(self):
        global is_wrong_coauthor
        db_config = {
            "user": "me",
            "password": "password",
            "host": "193.124.118.138",
            "database": "task_table",
        }
        database = mysql.connector.connect(**db_config)
        cursor = database.cursor(buffered=True)

        coauthors = self.coauthors.text()
        print(window, coauthors, index_table, name_curr)

        # Проверка на наличие введенных соавторов в бд
        if len(coauthors) == 0:
            self.status.setText("Поле пустое!")
        else:
            if window == 1:
                cursor.execute(f"UPDATE columns SET name = '{coauthors}' WHERE table_id = {index_table} AND name = '{name_curr}'")
                database.commit()
            elif window == 2:
                cursor.execute(
                    f"UPDATE columns SET text = '{coauthors}' WHERE table_id = {index_table} AND name = '{name_curr}'")
                database.commit()
            elif window == 3:
                cursor.execute(
                    f"UPDATE columns SET author = '{coauthors}' WHERE table_id = {index_table} AND name = '{name_curr}'")
                database.commit()

        self.close()
