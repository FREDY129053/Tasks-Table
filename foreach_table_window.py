import sys
import mysql

import add_coauthors_window
import other_classes
import add_column

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
#

from log_in_window import *
from sign_up_window import *
from secrets import compare_digest
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget, QHeaderView, QTableWidgetItem
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


class EachTable(QWidget):
    def __init__(self, window_title):
        super(EachTable, self).__init__()
        loadUi("Users_Interfaces/tables_widget.ui", self)
        self.setWindowTitle(window_title)
        global window_name
        window_name = self.windowTitle()
        self.add_coauthors_button.clicked.connect(self.add_coauthors)
        self.to_main.clicked.connect(self.close)

        self.add_columns.clicked.connect(self.add_column)

        name = self.findChild(QLabel, 'label_2')
        author = self.findChild(QLabel, 'author_name')
        coauthor = self.findChild(QLabel, 'label_3')

        name.setText(self.windowTitle())

        curr_user = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()
        cursor.execute(f"SELECT coauthors_login FROM tables WHERE table_name = '{self.windowTitle()}'")
        coauthors = cursor.fetchone()[0]

        cursor.execute(f"SELECT author_login FROM tables WHERE table_name = '{self.windowTitle()}'")
        author_from_db = cursor.fetchone()
        author.setText(author_from_db[0])

        if curr_user.username == author_from_db[0]:
            coauthor.setStyleSheet("color: gray; font: 600 12pt 'Work Sans';")
        elif curr_user.username in coauthors:
            coauthor.setStyleSheet("color: green; font: 600 12pt 'Work Sans';")
        else:
            coauthor.setStyleSheet("color: red; font: 600 12pt 'Work Sans';")
            self.add_text.setVisible(False)
            self.add_columns.setVisible(False)
            self.add_coauthors_button.setVisible(False)

        # self.add_column_btn.clicked.connect(self.add_column)

        table = self.findChild(QTableWidget, 'tableWidget')

        cursor.execute(f"SELECT background FROM tables WHERE table_name = '{self.windowTitle()}'")
        background_db = cursor.fetchone()[0]

        if (background_db == "") or (background_db is None):
            table.setStyleSheet("""
                background-color: rgb(170, 170, 255);
                border-radius: 10px;
                border: 3px solid #3C288C;
                """)
        else:
            table.setStyleSheet("""
                QTableWidget {
                background-image: url(%s);
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: 450px 320px;
                object-fit: cover;
                }""" % (background_db))

        cursor.execute(f"SELECT size_of_table FROM tables WHERE table_name = '{self.windowTitle()}'")
        table_size_db = int(cursor.fetchone()[0])
        table_size = 0 if table_size_db == 0 else table_size_db

        cursor.execute(f"SELECT columns_name FROM tables WHERE table_name = '{self.windowTitle()}'")
        name_col = cursor.fetchone()[0]

        cursor.execute(f"SELECT id FROM tables WHERE table_name = '{self.windowTitle()}'")
        id = int(cursor.fetchone()[0])

        cursor.execute(f"SELECT COUNT(*) FROM columns WHERE table_id = {id}")
        rows_db = cursor.fetchone()[0]
        rows = 1 if rows_db == 0 else rows_db

        print(name_col)
        if name_col is None:
            name_col = ["Новая колонка"] * table_size
        else:
            name_col = [i.strip() for i in name_col.split(",")]

        table.setColumnCount(table_size)
        table.setRowCount(rows)

        if rows == 1:
            table.setCellWidget(0, 0, self.add_text)

        for i, column_name in enumerate(name_col):
            print(f"GG {column_name}")
            item = QTableWidgetItem(column_name)
            table.setHorizontalHeaderItem(i, item)
            table.setColumnWidth(i, 150)


        # for i, name in enumerate(name_col):
        #     print(name)
        #     item = QTableWidgetItem(name)
        #     table.setHorizontalHeaderItem(i, item)
        #     table.setColumnWidth(i, 150)


    def add_column(self):
        self.col = add_column.AddColumn()
        self.col.show()

    def add_coauthors(self):
        self.coauthors = add_coauthors_window.AddCoauthors()
        self.coauthors.show()


def curr():
    return window_name
