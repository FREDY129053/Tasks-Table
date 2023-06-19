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
    "database": "tasks_table_copy",
}
database = mysql.connector.connect(**db_config)
cursor = database.cursor(buffered=True)
window = 0


class EachTable(QWidget):
    def __init__(self, window_titl, table_i):
        super(EachTable, self).__init__()
        loadUi("Users_Interfaces/tables_widget.ui", self)
        global window_title, table_id
        window_title = window_titl
        table_id = table_i

        update = self.findChild(QPushButton, 'pushButton')
        update.clicked.connect(lambda checked, b=566565: self.right(b, 1))

        self.setWindowTitle(window_title)
        global window_name
        window_name = self.windowTitle()
        self.board_id = int(table_id)
        # self.add_coauthors_button.clicked.connect(self.add_coauthors(self.board_id))
        self.add_coauthors_button.clicked.connect(lambda checked, b=self.board_id: self.add_coauthors(b))
        self.to_main.clicked.connect(self.close)

        self.add_columns.clicked.connect(lambda checked, b=self.board_id: self.add_column(b))

        name = self.findChild(QLabel, 'label_2')
        author = self.findChild(QLabel, 'author_name')
        coauthor = self.findChild(QLabel, 'label_3')
        add_column_btn = self.findChild(QPushButton, 'add_columns')
        add_note_btn = self.findChild(QPushButton, 'add_text')

        # Сделать выбор из таблицы по id таблицы и добавлять в первую колонку таблицы
        cursor.execute(f"SELECT id FROM columns WHERE board_id = {table_id}")
        columns_ids = cursor.fetchall()
        columns_ids = [0] if len(columns_ids) == 0 else [int(i) for i in columns_ids[0]]
        add_note_btn.clicked.connect(lambda checked, b=columns_ids[0]: self.add_note(b))

        name.setText(self.windowTitle())

        curr_user = sign_up_window.curr() if sign_up_window.curr() is not None else log_in_window.curr()

        # тип доски на экране
        cursor.execute(f"SELECT status FROM board WHERE id = {self.board_id}")
        type = cursor.fetchone()[0]
        curr_type = "Приватная" if int(type) == 1 else "Публичная"
        self.label_5.setText(curr_type)

        cursor.execute(f"SELECT id FROM columns WHERE board_id = {table_id}")
        self.columns_ids = cursor.fetchall()
        self.columns_ids = [i[0] for i in self.columns_ids]

        cursor.execute(
            f"SELECT users.login FROM users JOIN board ON users.id = board.author_id WHERE board.id = {self.board_id}")
        board_author = cursor.fetchone()[0]
        author.setText(board_author)

        cursor.execute(f"""SELECT users.login FROM board JOIN coauthors ON board.id = coauthors.table_id 
            JOIN users ON coauthors.user_id = users.id WHERE board.id = {self.board_id}""")
        coauthors = cursor.fetchall()

        if curr_user.username == board_author:
            coauthor.setStyleSheet("color: gray; font: 600 12pt 'Work Sans';")
        elif curr_user.username in [temp[0] for temp in coauthors]:
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

        cursor.execute(f"SELECT * FROM columns WHERE board_id = {self.board_id}")
        columns_from_db = cursor.fetchall()

        columns_names = []
        columns_indexies = []

        for column in columns_from_db:
            columns_id = column[0]
            column_name = column[2]

            columns_indexies.append(columns_id)
            columns_names.append(column_name)

        self.clickable_notes = []
        if len(columns_names) == 0:
            self.add_text.setVisible(False)
            horizontal_columns.addWidget(add_column_btn)
            table.setWidget(main_widget_of_column)
        else:
            for i in range(len(columns_names)):
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

                name_of_column = QLabel(f"{columns_names[i]}")

                name_of_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
                column.setStyleSheet("border: none;")
                name_of_column.setFixedWidth(170)

                scroll_column.setFixedSize(200, 275)
                widget_for_column_elements = QVBoxLayout(column)
                widget_for_column_elements.addWidget(name_of_column)
                widget_for_column_elements.addStretch()

                cursor.execute(f"SELECT * FROM tasks WHERE column_id = {columns_indexies[i]}")
                current_tasks = cursor.fetchall()

                if len(current_tasks) == 0 and i == 0:
                    widget_for_column_elements.addWidget(add_note_btn)
                    widget_for_column_elements.addStretch()
                else:
                    for j in range(len(current_tasks)):
                        temp_button = QPushButton()
                        temp_button.setStyleSheet("border: 1px solid #333333")
                        temp_button.setText(f"{current_tasks[j][2]}")
                        temp_button.setFixedWidth(170)
                        self.clickable_notes.append(temp_button)

                        widget_for_column_elements.addWidget(temp_button)
                        widget_for_column_elements.addStretch()

                        cont = QMenu(self)
                        show_action = QAction("Посмотреть запись", self)
                        show_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.show_window(b))
                        #
                        rename_action = QAction("Изменить название", self)
                        rename_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.change_name(b))

                        change_desc_action = QAction("Изменить описание", self)
                        change_desc_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.change_desc(b))

                        change_author_action = QAction("Изменить автора", self)
                        change_author_action.triggered.connect(
                            lambda checked, b=current_tasks[j][0]: self.change_author(b))

                        right_action = QAction("→", self)
                        right_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.right(b, 0))

                        left_action = QAction("←", self)
                        left_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.left(b))

                        cont.addAction(show_action)
                        cont.addAction(rename_action)
                        cont.addAction(change_desc_action)
                        cont.addAction(change_author_action)
                        cont.addAction(right_action)
                        cont.addAction(left_action)

                        temp_button.setMenu(cont)

                    if i == 0:
                        widget_for_column_elements.addWidget(add_note_btn)
                        widget_for_column_elements.addStretch()

                scroll_column.setWidget(column)

                spacer = QSpacerItem(100, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

                horizontal_columns.addWidget(scroll_column)
                if i < len(columns_names) - 1:
                    horizontal_columns.addItem(spacer)

            horizontal_columns.addWidget(add_column_btn)
            table.setWidget(main_widget_of_column)
        #
        # for i, button in enumerate(self.clickable_notes):
        #     button.clicked.connect(lambda _, index=i: self.show_window(self.clickable_notes[index].text()))

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

    def update_window(self):
        self.scrollArea.takeWidget()

        self.add_coauthors_button.clicked.connect(lambda checked, b=self.board_id: self.add_coauthors(b))
        self.to_main.clicked.connect(self.close)

        add_column_btn = QPushButton()
        add_column_btn.setText("+Добавить колонку")
        add_column_btn.setStyleSheet("""border-radius: 10px;
                                        font: 600 18pt "Segoe UI";
                                        border-left: 2px solid #3C288C;
                                        border-top: 2px solid #3C288C;
                                        border-right: 2px solid #3C288C;
                                        border-bottom: 2px solid #3C288C;
                                        background-color: rgb(255, 255, 255);""")

        add_note_btn = QPushButton()
        add_note_btn.setText("+ Добавить запись")
        add_note_btn.setStyleSheet("""border-radius: 10px;
                                                font: 600 9pt "Segoe UI";
                                                border-left: 2px solid #3C288C;
                                                border-top: 2px solid #3C288C;
                                                border-right: 2px solid #3C288C;
                                                border-bottom: 2px solid #3C288C;
                                                background-color: rgb(255, 255, 255);""")

        add_column_btn.clicked.connect(lambda checked, b=self.board_id: self.add_column(b))
        add_note_btn.clicked.connect(self.add_note)

        cursor.execute(f"SELECT id FROM columns WHERE board_id = {table_id}")
        self.columns_ids = cursor.fetchall()
        self.columns_ids = [i[0] for i in self.columns_ids]

        table = self.findChild(QScrollArea, 'scrollArea')
        scroll = table.verticalScrollBar()
        scroll.setOrientation(Qt.Orientation.Horizontal)

        main_widget_of_column = QWidget()
        horizontal_columns = QHBoxLayout(main_widget_of_column)

        cursor.execute(f"SELECT * FROM columns WHERE board_id = {self.board_id}")
        columns_from_db = cursor.fetchall()

        columns_names = []
        columns_indexies = []

        for column in columns_from_db:
            columns_id = column[0]
            column_name = column[2]

            columns_indexies.append(columns_id)
            columns_names.append(column_name)

        self.clickable_notes = []
        if len(columns_names) == 0:
            self.add_text.setVisible(False)
            horizontal_columns.addWidget(add_column_btn)
            table.setWidget(main_widget_of_column)
        else:
            for i in range(len(columns_names)):
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

                name_of_column = QLabel(f"{columns_names[i]}")

                name_of_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
                column.setStyleSheet("border: none;")
                name_of_column.setFixedWidth(170)

                scroll_column.setFixedSize(200, 275)
                widget_for_column_elements = QVBoxLayout(column)
                widget_for_column_elements.addWidget(name_of_column)
                widget_for_column_elements.addStretch()

                cursor.execute(f"SELECT * FROM tasks WHERE column_id = {columns_indexies[i]}")
                current_tasks = cursor.fetchall()

                if len(current_tasks) == 0 and i == 0:
                    widget_for_column_elements.addWidget(add_note_btn)
                    widget_for_column_elements.addStretch()
                else:
                    for j in range(len(current_tasks)):
                        temp_button = QPushButton()
                        temp_button.setStyleSheet("border: 1px solid #333333")
                        temp_button.setText(f"{current_tasks[j][2]}")
                        temp_button.setFixedWidth(170)
                        self.clickable_notes.append(temp_button)

                        widget_for_column_elements.addWidget(temp_button)
                        widget_for_column_elements.addStretch()

                        cont = QMenu(self)
                        show_action = QAction("Посмотреть запись", self)
                        show_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.show_window(b))
                        #
                        rename_action = QAction("Изменить название", self)
                        rename_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.change_name(b))

                        change_desc_action = QAction("Изменить описание", self)
                        change_desc_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.change_desc(b))

                        change_author_action = QAction("Изменить автора", self)
                        change_author_action.triggered.connect(
                            lambda checked, b=current_tasks[j][0]: self.change_author(b))

                        right_action = QAction("→", self)
                        right_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.right(b, 0))

                        left_action = QAction("←", self)
                        left_action.triggered.connect(lambda checked, b=current_tasks[j][0]: self.left(b))

                        cont.addAction(show_action)
                        cont.addAction(rename_action)
                        cont.addAction(change_desc_action)
                        cont.addAction(change_author_action)
                        cont.addAction(right_action)
                        cont.addAction(left_action)

                        temp_button.setMenu(cont)

                    if i == 0:
                        widget_for_column_elements.addWidget(add_note_btn)
                        widget_for_column_elements.addStretch()

                scroll_column.setWidget(column)

                spacer = QSpacerItem(100, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

                horizontal_columns.addWidget(scroll_column)
                if i < len(columns_names) - 1:
                    horizontal_columns.addItem(spacer)

            horizontal_columns.addWidget(add_column_btn)
            table.setWidget(main_widget_of_column)

    def change_name(self, table_id):
        global window

        window = 1
        self.window_temp1 = temp_class.TempClass(table_id)
        self.window_temp1.show()

    def change_desc(self, table_id):
        global window

        window = 2
        self.window_temp1 = temp_class.TempClass(table_id)
        self.window_temp1.show()

    def change_author(self, table_id):
        global window

        window = 3
        self.window_temp1 = temp_class.TempClass(table_id)
        self.window_temp1.show()

    def right(self, zapis_id, flag):
        if flag == 0:
            cursor.execute(f"SELECT column_id FROM tasks WHERE id = {zapis_id}")
            curr_column_id = int(cursor.fetchone()[0])

            id_of_curr_column = self.columns_ids.index(curr_column_id)

            if id_of_curr_column + 1 >= len(self.columns_ids):
                pass
            else:
                cursor.execute(
                    f"UPDATE tasks SET column_id = {self.columns_ids[id_of_curr_column + 1]} WHERE id = {zapis_id}")
                database.commit()
        else:
            flag += 0
            database.commit()
        self.update_window()

    def left(self, zapis_id):
        cursor.execute(f"SELECT column_id FROM tasks WHERE id = {zapis_id}")
        curr_column_id = int(cursor.fetchone()[0])

        id_of_curr_column = self.columns_ids.index(curr_column_id)

        if id_of_curr_column - 1 < 0:
            pass
        else:
            cursor.execute(
                f"UPDATE tasks SET column_id = {self.columns_ids[id_of_curr_column - 1]} WHERE id = {zapis_id}")
            database.commit()

        self.update_window()

    def show_window(self, zapis_id):
        self.window = zapis.EachNote(zapis_id)
        self.window.show()

    def add_column(self, table_id):
        self.col = add_column.AddColumn(table_id)
        self.col.show()

    def add_coauthors(self, table_id):
        self.coauthors = add_coauthors_window.AddCoauthors(table_id)
        self.coauthors.show()

    def add_note(self, col):
        self.note = add_note.AddNote(col)
        self.note.show()


def curr():
    return window_name


def current_name():
    return window_title


def current_id():
    return table_id


def window_for_action():
    return window
