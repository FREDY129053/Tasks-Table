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
    "database": "tasks_table_copy",
}
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)

class AddCoauthors(QWidget):
    def __init__(self, table_id):
        super(AddCoauthors, self).__init__()
        loadUi("Users_Interfaces/add_coauthors.ui", self)
        self.setWindowTitle("Добавление соавторов")
        self.table_id = table_id
        self.add_coauthors_button.clicked.connect(self.add_coauthors)

    def add_coauthors(self):
        global is_wrong_coauthor

        coauthors = self.coauthors.text().split(', ')
        is_wrong_coauthor = True

        # Проверка на наличие введенных соавторов в бд
        if len(coauthors) == 0:
            pass
        elif len(coauthors) != 0 and is_wrong_coauthor:
            for i in coauthors:
                cursor.execute(f"SELECT * FROM users WHERE login='{i}'")
                user_info = cursor.fetchall()
                print(user_info)
                if len(user_info) == 0:
                    self.status.setText(f"Пользователь \"{i}\" не найден")
                    is_wrong_coauthor = True
                else:
                    is_wrong_coauthor = False

        if is_wrong_coauthor is False:
            for i in coauthors:
                cursor.execute(f"SELECT * FROM users WHERE login = '{i}'")
                user_id = cursor.fetchone()[0]
                print(f"Us = {user_id}")
                print(f"Tab = {self.table_id}")
                cursor.execute(f"INSERT INTO coauthors (user_id, table_id) VALUES({user_id}, {self.table_id})")
                database.commit()

            self.close()
