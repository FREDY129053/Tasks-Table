import add_table_window

import sys
import mysql

from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget, QScrollArea, QSpacerItem, QMenu, QTableWidgetItem
                             )
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtCore import QCoreApplication
from mysql.connector import connect

import foreach_table_window

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

        self.update_as = self.findChild(QAction, 'update_act_2')
        self.update_as.triggered.connect(self.update_window)

        btn = self.findChild(QPushButton, 'add_table_btn')
        self.add_table_btn.clicked.connect(self.add_table)

        self.scroll_area = self.findChild(QScrollArea, 'scrollArea')

        parent = self.scroll_area.parentWidget()
        btn.move(650, 460)
        btn.setParent(parent)

        # def add_tables_buttons(self):
        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        cursor.execute("SELECT * FROM tables")
        tables = cursor.fetchall()
        # print(tables)

        self.buttons = []
        for i in range(len(tables)):
            new = QPushButton()

            new.setStyleSheet("""
            background-color: rgb(255, 255, 255);
            border-radius: 10px;
            border-width: 2px 2px 2px 2px;
            border-style: solid;
            border-color: #6757A5;
            font: 600 13px "Work Sans";
            """)

            # print(tables[i][1])
            new.setText(f"{tables[i][1]}")
            new.setObjectName(f"{tables[i][1]}")
            new.setFixedWidth(250)
            new.setFixedHeight(80)
            self.buttons.append(new)

            scroll_layout.addWidget(new, i // 2, i % 2)

            if i + 1 >= len(tables):
                scroll_layout.addWidget(empty_widget)

            scroll_widget.setLayout(scroll_layout)
            self.scroll_area.setWidget(scroll_widget)

        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, index=i: self.show_window(self.buttons[index]))

    def update_window(self):
        self.scroll_area.takeWidget()

        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        cursor.execute("SELECT * FROM tables")
        tables = cursor.fetchall()
        # print(tables)

        self.buttons = []
        for i in range(len(tables)):
            new = QPushButton()

            new.setStyleSheet("""
                    background-color: rgb(255, 255, 255);
                    border-radius: 10px;
                    border-width: 2px 2px 2px 2px;
                    border-style: solid;
                    border-color: #6757A5;
                    font: 600 13px "Work Sans";
                    """)

            # print(tables[i][1])
            new.setText(f"{tables[i][1]}")
            new.setObjectName(f"{tables[i][1]}")
            new.setFixedWidth(250)
            new.setFixedHeight(80)
            self.buttons.append(new)

            scroll_layout.addWidget(new, i // 2, i % 2)

            if i + 1 >= len(tables):
                scroll_layout.addWidget(empty_widget)

            scroll_widget.setLayout(scroll_layout)
            self.scroll_area.setWidget(scroll_widget)

        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, index=i: self.show_window(self.buttons[index]))

    def show_window(self, title):
        # self.new_window = foreach_table_window.EachTable()
        self.new_window = QWidget()
        self.new_window.setFixedSize(617, 440)
        self.new_window.setWindowTitle(f"{title.sender().objectName()}")

        layout = QVBoxLayout()

        # кнопка добавления столбца
        add_column_btn = QPushButton()
        add_column_btn.setFixedSize(120, 25)
        add_column_btn.setText("+ Добавить столбец")
        add_column_btn.clicked.connect(self.add_column)

        layout.addWidget(add_column_btn)
        add_column_btn.move(0, 0)

        # добавление таблицы
        table = QTableWidget()
        table.setFixedSize(590, 370)

        cursor.execute(f"SELECT size_of_table FROM tables WHERE table_name = '{self.new_window.windowTitle()}'")
        count_of_columns = cursor.fetchone()[0]
        print(count_of_columns)

        for i in range(count_of_columns):
            table.insertColumn(i)
            header_item = QTableWidgetItem(f"Новый столбец {i + 1}")
            table.setHorizontalHeaderLabels(i, header_item)
        table.setColumnCount(count_of_columns)


        layout.addWidget(table)
        self.new_window.setLayout(layout)
        table.move(15, 80)

        self.new_window.show()

    def add_column(self):
        cursor.execute(f"UPDATE tables SET size_of_table = size_of_table + 1 WHERE table_name = '{self.windowTitle()}'")
        database.commit()

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
