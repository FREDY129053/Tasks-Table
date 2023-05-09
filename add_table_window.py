import sys
import mysql

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


class AddTable(QWidget):
    def __init__(self):
        super(AddTable, self).__init__()
        loadUi("Users_Interfaces/add_table.ui", self)
        self.setWindowTitle("Новая доска")

        self.add_table_btn.clicked.connect(self.add_table)

    def add_table(self):
        db_config = {
            "user": "me",
            "password": "password",
            "host": "193.124.118.138",
            "database": "task_table",
        }
        database = mysql.connector.connect(**db_config)
        cursor = database.cursor(buffered=True)

        table_name = self.table_name.text()
        coauthors = self.coauthors.text().split(', ')


        # Проверка на наличие введенных соавторов в бд
        is_wrong_coauthor = False
        for i in coauthors:
            cursor.execute(f"SELECT * FROM users WHERE login='{i}'")
            user_info = cursor.fetchall()
            if len(user_info) == 0:
                self.status.setText(f"Пользователь \"{i}\" не найден")
                is_wrong_coauthor = True

        if len(table_name) == 0:
            self.status.setText("Введите название доски")
        elif is_wrong_coauthor == False:
            # тип таблицы
            kind = "public" if str(self.table_type.checkState()) == str(Qt.CheckState.Unchecked) else "private"
            print(table_name)
            print(coauthors)
            print(kind)
            self.close()
