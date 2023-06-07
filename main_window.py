import add_table_window

import sys
import mysql
import sign_up_window, log_in_window

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

        global current_window

        self.setWindowTitle("Main")

        # стиль меню
        my_menu = self.findChild(QMenu, 'menu')
        my_menu_style = "QMenu::item:selected { background-color: #6757A5; color: #FFFFFF; }"
        my_menu.setStyleSheet(my_menu_style)
        my_menu.setMouseTracking(True)

        my_menu2 = self.findChild(QMenu, 'menu_2')
        my_menu_style2 = "QMenu::item:selected { background-color: #6757A5; color: #FFFFFF; }"
        my_menu2.setStyleSheet(my_menu_style2)
        my_menu2.setMouseTracking(True)
        #

        self.my_desks = self.findChild(QAction, 'my_desks')
        self.my_desks.triggered.connect(self.show_my_desks)

        self.my_private_desks = self.findChild(QAction, 'my_private_desks')
        self.my_private_desks.triggered.connect(self.show_my_private_desks)

        self.me_coauthor = self.findChild(QAction, 'me_coauthor')
        self.me_coauthor.triggered.connect(self.show_where_me_coauthor)

        self.public_desks = self.findChild(QAction, 'public_desks')
        self.public_desks.triggered.connect(self.update_window)

        self.update_as = self.findChild(QAction, 'update_act_2')

        self.pushButton.clicked.connect(self.update_window)

        btn = self.findChild(QPushButton, 'add_table_btn')
        self.add_table_btn.clicked.connect(self.add_table)

        self.scroll_area = self.findChild(QScrollArea, 'scrollArea')

        parent = self.scroll_area.parentWidget()
        btn.move(650, 460)
        btn.setParent(parent)

        # def add_tables_buttons(self):
        scroll_layout = QGridLayout()

        self.label.setText("Публичные доски")

        scroll_widget = QWidget()

        scroll_widget.setLayout(scroll_layout)
        self.scroll_area.setWidget(scroll_widget)

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        cursor.execute("SELECT * FROM tables WHERE table_type = 0")
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
        self.pushButton.clicked.connect(self.update_window)

        self.label.setText("Публичные доски")

        self.scroll_area.takeWidget()

        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        cursor.execute("SELECT * FROM tables WHERE table_type = 0")
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

    def show_my_desks(self):
        self.pushButton.clicked.connect(self.show_my_desks)

        self.label.setText("Мои доски")

        self.scroll_area.takeWidget()

        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        author = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()
        cursor.execute(f"SELECT * FROM tables WHERE author_login = '{author.username}'")
        tables = cursor.fetchall()

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

    def show_my_private_desks(self):
        self.pushButton.clicked.connect(self.show_my_private_desks)

        self.label.setText("Мои приватные доски")

        self.scroll_area.takeWidget()

        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        author = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()
        cursor.execute(f"SELECT * FROM tables WHERE author_login = '{author.username}' AND table_type = 1")
        tables = cursor.fetchall()

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

    def show_where_me_coauthor(self):
        self.pushButton.clicked.connect(self.show_where_me_coauthor)

        self.label.setText("Доски, где я соавтор")

        self.scroll_area.takeWidget()

        scroll_layout = QGridLayout()
        scroll_widget = QWidget()

        # виджет-пустышка для добавления в конец, чтобы место занимал
        empty_widget = QLabel()
        empty_widget.setFixedSize(100, 10)

        database.commit()
        author = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()
        cursor.execute(f"SELECT * FROM tables WHERE coauthors_login LIKE '%{author.username}%'")
        tables = cursor.fetchall()

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
        self.new_window = QWidget()

        self.new_window.setWindowTitle(f"{title.sender().objectName()}")
        self.window = foreach_table_window.EachTable(self.new_window.windowTitle())

        self.window.show()

    def add_table(self):
        self.main = add_table_window.AddTable()
        self.main.show()
