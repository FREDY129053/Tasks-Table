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

class TempClass(QWidget):
    def __init__(self, table_id):
        super(TempClass, self).__init__()
        loadUi("Users_Interfaces/add_coauthors.ui", self)
        global window, index_table, name_curr
        self.table_id = table_id
        window = foreach_table_window.window_for_action()

        self.add_coauthors_button.setText("Внести корректировки")

        if window == 1:
            self.setWindowTitle("Переименовать запись")
            self.label.setText("Переименовать запись")
        elif window == 2:
            self.setWindowTitle("Изменить описание")
            self.label.setText("Изменить описание")
        elif window == 3:
            self.setWindowTitle("Изменить автора")
            self.label.setText("Изменить автора")

        self.add_coauthors_button.clicked.connect(self.add_coauthors)


    def add_coauthors(self):
        global is_wrong_coauthor

        ready_to_close = False

        coauthors = self.coauthors.text()

        # Проверка на наличие введенных соавторов в бд
        if len(coauthors) == 0:
            self.status.setText("Поле пустое!")
        else:
            if window == 1:
                cursor.execute(f"UPDATE tasks SET name = '{coauthors}' WHERE id = {self.table_id}")
                database.commit()
                ready_to_close = True
            elif window == 2:
                cursor.execute(
                    f"UPDATE tasks SET description = '{coauthors}' WHERE id = {self.table_id}")
                database.commit()
                ready_to_close = True
            elif window == 3:
                cursor.execute(f"SELECT id  FROM users WHERE login = '{coauthors}'")
                new_author = int(cursor.fetchone()[0])

                if new_author is None:
                    self.status.setText("Нет такого пользователя!")
                else:
                    new_author = int(new_author[0])
                    cursor.execute(
                        f"UPDATE tasks SET author_id = {new_author} WHERE id = {self.table_id}")
                    database.commit()
                    ready_to_close = True

        if ready_to_close:
            self.close()
