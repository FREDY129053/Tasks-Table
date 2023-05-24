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


class AddCoauthors(QWidget):
    def __init__(self):
        super(AddCoauthors, self).__init__()
        loadUi("Users_Interfaces/add_coauthors.ui", self)
        self.setWindowTitle("Добавление соавторов")

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

        coauthors = self.coauthors.text().split(', ')

        # Проверка на наличие введенных соавторов в бд
        if len(coauthors) == 0:
            pass
        else:
            is_wrong_coauthor = False
            for i in coauthors:
                cursor.execute(f"SELECT * FROM users WHERE login='{i}'")
                user_info = cursor.fetchall()
                if len(user_info) == 0:
                    self.status.setText(f"Пользователь \"{i}\" не найден")
                    is_wrong_coauthor = True

        if is_wrong_coauthor is False:
            # table = other_classes.Table(table_name, author.username, self.coauthors.text(), table_type, size, columns_name)
            cursor.execute(f"SELECT coauthors_login FROM tables WHERE table_name = '{foreach_table_window.curr()}'")
            user_info = cursor.fetchall()
            user_info_str = ""
            for i in user_info:
                user_info_str = " ".join(i)
            coauthors_str = user_info_str + " " + " ".join(coauthors)
            cursor.execute(f"UPDATE tables SET coauthors_login = '{coauthors_str}' "
                           f"WHERE table_name = '{foreach_table_window.curr()}'")
            database.commit()
            self.close()
