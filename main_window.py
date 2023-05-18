import add_table_window

import sys
import mysql

from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget, QScrollArea, QSpacerItem, QMenu
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

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("Users_Interfaces/main_window.ui", self)

        self.setWindowTitle("Main")

        self.update_as = self.findChild(QAction, 'update_act')
        self.update_as.triggered.connect(self.update_window)

        btn = self.findChild(QPushButton, 'add_table_btn')
        self.add_table_btn.clicked.connect(self.add_table)

        table_btn = self.findChild(QPushButton, 'table_name')
        scroll_area = self.findChild(QScrollArea, 'scrollArea')

        parent = scroll_area.parentWidget()
        btn.move(650, 513)
        btn.setParent(parent)

        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        cursor.execute("SELECT * FROM tables")
        tables = cursor.fetchall()
        print(tables)

        for i in range(len(tables)):
            new = QPushButton()
            new.setText(f"{tables[i][1]}")
            new.setFixedWidth(250)
            new.setFixedHeight(80)

            scroll_layout.addWidget(new, i // 2, i % 2)

            if i + 1 >= len(tables):
                scroll_layout.addWidget(empty_widget)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)


    def update_window(self):
        self.close()
        self.show()

    # заполнение таблицы данными
    def load_data(self, table):
        tasks = [{"name": "Посрать", "age": "Покупка туалетки", "address": "Срать"},
                 {"name": "Mark", "age": "18", "address": "Alabama"},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": "Обосраться"},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": "Отложить кучу"},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": ""},
                 {"name": "Посрать", "age": "Покупка туалетки", "address": "Надристать"}]
        row = 0
        table.setRowCount(len(tasks))

        for task in tasks:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(task["name"]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(task["age"]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(task["address"]))
            row += 1

    def add_table(self):
        self.main = add_table_window.AddTable()
        self.main.show()
