import sys
import mysql

import add_coauthors_window, other_classes, add_column, add_note, zapis, temp_class

# эти два класса ВАЖНЫ, иначе сломается (хз почему)
import log_in_window
import sign_up_window
#

from functools import partial
from log_in_window import *
from sign_up_window import *
from secrets import compare_digest
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QMainWindow, QGridLayout, QLabel, QStatusBar, QCheckBox, QDialog, QStackedWidget,
                             QTableWidget, QHeaderView, QTableWidgetItem, QColumnView, QTableView, QScrollArea,
                             QSpacerItem, QMenu
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
window = 0

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
        add_column_btn = self.findChild(QPushButton, 'add_columns')
        add_note_btn = self.findChild(QPushButton, 'add_text')

        add_note_btn.clicked.connect(self.add_note)

        name.setText(self.windowTitle())

        curr_user = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()
        cursor.execute(f"""SELECT coauthors_login, author_login, background, 
                           size_of_table, columns_name, id, table_type FROM tables WHERE table_name = '{self.windowTitle()}'""")

        info_from_db = cursor.fetchall()

        global ind
        coauthors, author_from_db, background_db, table_size_db, name_col, ind, type = info_from_db[0]

        table_size_db = int(table_size_db)

        ind = int(ind)
        type = "Публичная" if int(type) == 0 else "Приватная"

        author.setText(author_from_db)
        self.label_5.setText(f"{type}")

        if curr_user.username == author_from_db:
            coauthor.setStyleSheet("color: gray; font: 600 12pt 'Work Sans';")
        elif curr_user.username in coauthors:
            coauthor.setStyleSheet("color: green; font: 600 12pt 'Work Sans';")
        else:
            coauthor.setStyleSheet("color: red; font: 600 12pt 'Work Sans';")
            self.add_text.setVisible(False)
            self.add_columns.setVisible(False)
            self.add_coauthors_button.setVisible(False)

        table = self.findChild(QScrollArea, 'scrollArea')
        scroll = table.verticalScrollBar()
        scroll.setOrientation(Qt.Orientation.Horizontal)

        main_widget_of_column = QWidget()
        horizontal_columns = QHBoxLayout(main_widget_of_column)

        cursor.execute(f"SELECT size_of_table, columns_name FROM tables WHERE table_name = '{window_name}'")
        columns_from_db = cursor.fetchall()
        columns_count, temp = columns_from_db[0]
        columns_name = temp.split(',') if temp is not None else (["Новая колонка"] * int(columns_count))
        columns_name = [i for i in columns_name if i != '']

        cursor.execute(f"SELECT * FROM columns WHERE table_id = {ind}")
        notes = cursor.fetchall()
        notes = [i for i in notes]

        self.clickable_notes = []
        if len(columns_name) == 0:
            self.add_text.setVisible(False)
            horizontal_columns.addWidget(add_column_btn)
            table.setWidget(main_widget_of_column)
        else:
            for i in range(len(columns_name)):
                scroll_column = QScrollArea()
                column = QWidget()

                scroll_column.setStyleSheet("QScrollBar:vertical {"
                                            "    border: none;"
                                            "    background-color: #F0F0F0;"
                                            "    width: 5px;"
                                            "    margin: 0px 0px 0px 0px;"
                                            "}"
                                            "QScrollBar::handle:vertical {"
                                            "    background-color: #C0C0C0;"
                                            "    min-height: 20px;"
                                            "}"
                                            "QScrollBar::add-line:vertical {"
                                            "    border: none;"
                                            "    background-color: none;"
                                            "}"
                                            "QScrollBar::sub-line:vertical {"
                                            "    border: none;"
                                            "    background-color: none;"
                                            "}")

                name_of_column = QLabel(f"{columns_name[i]}")

                name_of_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
                column.setStyleSheet("border: none;")
                name_of_column.setFixedWidth(170)

                scroll_column.setFixedSize(200, 275)
                widget_for_column_elements = QVBoxLayout(column)
                widget_for_column_elements.addWidget(name_of_column)
                widget_for_column_elements.addStretch()

                if len(notes) == 0 and i == 0:
                    widget_for_column_elements.addWidget(add_note_btn)
                    widget_for_column_elements.addStretch()
                if i == int(notes[i][4]) - 1:
                    # notes_temp = [notes[i]]
                    notes_temp = notes

                    for j in range(len(notes_temp)):
                        temp_button = QPushButton()
                        temp_button.setStyleSheet("border: 1px solid #333333")
                        temp_button.setText(f"{notes_temp[j][2]}")
                        temp_button.setFixedWidth(170)
                        self.clickable_notes.append(temp_button)

                        widget_for_column_elements.addWidget(temp_button)
                        widget_for_column_elements.addStretch()

                        cont = QMenu(self)
                        show_action = QAction("Посмотреть запись", self)
                        show_action.triggered.connect(lambda checked, b=temp_button: self.show_window(b.text()))

                        rename_action = QAction("Изменить название", self)
                        rename_action.triggered.connect(lambda checked, b=temp_button: self.change_name(b.text()))

                        change_desc_action = QAction("Изменить описание", self)
                        change_desc_action.triggered.connect(self.change_desc)

                        change_author_action = QAction("Изменить автора", self)
                        change_author_action.triggered.connect(self.change_author)

                        right_action = QAction("→", self)
                        right_action.triggered.connect(self.go_right(name))

                        cont.addAction(show_action)
                        cont.addAction(rename_action)
                        cont.addAction(change_desc_action)
                        cont.addAction(change_author_action)

                        temp_button.setMenu(cont)

                    if i == 0:
                        widget_for_column_elements.addWidget(add_note_btn)
                        widget_for_column_elements.addStretch()

                scroll_column.setWidget(column)

                spacer = QSpacerItem(100, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

                horizontal_columns.addWidget(scroll_column)
                if i < 6:
                    horizontal_columns.addItem(spacer)

            horizontal_columns.addWidget(add_column_btn)
            table.setWidget(main_widget_of_column)

        for i, button in enumerate(self.clickable_notes):
            button.clicked.connect(lambda _, index=i: self.show_window(self.clickable_notes[index].text()))

        # back = QPixmap(f"{background_db}")
        # widget.setStyleSheet(f"background-image: url({back.toImage()}); background-repeat: no-repeat; background-position: left; background-attachment: fixed;")
        #
        # if (background_db == "") or (background_db is None):
        #     widget.setStyleSheet("""
        #         background-color: rgb(170, 170, 255);
        #         border-radius: 10px;
        #         border: 3px solid #3C288C;
        #         """)
        # else:
        #     widget.setStyleSheet("""
        #         QWidget {
        #         background-image: url(%s);
        #         background-repeat: no-repeat;
        #         background-position: center;
        #         background-attachment: fixed;
        #         background-size: 450px 320px;
        #         object-fit: cover;
        #         }""" % (background_db))

    def change_name(self, name):
        global window

        window = 1
        self.window_temp1 = temp_class.TempClass(name)
        self.window_temp1.show()

    def change_desc(self):
        global window

        window = 2
        self.window_temp1 = temp_class.TempClass()
        self.window_temp1.show()

    def change_author(self):
        global window

        window = 3
        self.window_temp1 = temp_class.TempClass()
        self.window_temp1.show()

    # def go_right(self, name):
    #     cursor
    #     cursor.execute(f"UPDATE columns SET column_id = column_id + 1 WHERE name = '{name}'")


    def show_window(self, title):
        self.window = zapis.EachNote(title)
        self.window.show()

    def add_column(self):
        self.col = add_column.AddColumn()
        self.col.show()

    def add_coauthors(self):
        self.coauthors = add_coauthors_window.AddCoauthors()
        self.coauthors.show()

    def add_note(self):
        self.note = add_note.AddNote()
        self.note.show()


def curr():
    return window_name

def window_for_action():
    return window

def current_id():
    return ind
