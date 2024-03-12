import os.path
import sqlite3
import sys
import time
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
# import sqlite3
# 1|a|b|
# q0||q1||
# q1|q4|q1|q2|
# q2|q4|q3|q4|
# q4|q4|q1|q4|
# q3|q3|q3|q3|

# a|b|1|
# q0|q1|q4|q4|
# q1|q2|q0|q0|
# q2|q4|q3|q4|
# q3|qf|qf|qf|
# q4|q5|q0|q0|
# q5|q6|q4|q4|
# q6|q0|qf|q0|
# qf|q3|q3|q3|

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle("Сюда вставить название")

        self.tableStyle = "QTableWidget{\ngridline-color: #666666}"
        self.headerStyle = "::section:pressed {background-color: #323232;\nborder: none;}\n::section {background-color: #323232;\nborder: none;}"
        self.words = []
        self.alphabet = []
        self.dka = {}
        self.btn_load.triggered.connect(self.load)
        self.btn_check.clicked.connect(lambda: self.check_word(self.word.text(), self.dka, self.words[0]))

    def load(self):
        file = open("test.txt").readlines()
        words = []
        alphabet = file[0].split("|")
        alphabet.pop()
        dka = {}
        print(f"{alphabet}")
        for i in range(1, len(file)):
            line = file[i].split("|")
            line.pop()
            val = {}
            for j in range(1, len(line)):
                val[alphabet[j - 1]] = line[j]
            dka[line[0]] = val
            words.append(line[0])

        print(words)
        print(dka)
        self.println(words)
        self.println(dka)
        m = f"M = ({words}, {alphabet}, δ, {words[0]}, '{words[len(words) - 1]}')"
        self.about_m.setText(m)

        self.tableWidget.horizontalHeader().setStyleSheet(self.headerStyle)
        self.tableWidget.setStyleSheet(self.tableStyle)
        self.tableWidget.verticalHeader().hide()

        self.tableWidget.setColumnCount(len(alphabet) + 1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        headers = ['']
        for i in alphabet:
            headers.append(f"'{i}'")
        self.tableWidget.setHorizontalHeaderLabels(headers)

        keys = dka.keys()
        for i in dka:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(i)))
            vals = dka.get(i).values()
            v = 1
            for j in vals:
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, v, QtWidgets.QTableWidgetItem(f"'{str(j)}'"))
                v+=1

        self.words = words
        self.alphabet = alphabet
        self.dka = dka


    def check_word(self, word, machine, state):
        if word == "":
            self.println(f"({state}, {word})")
            self.println(f"End state: {state}")
            if state in self.words[len(self.words) - 1]:
                self.println("Цепочка принадлежит языку!")
            else:
                self.println("error: code 3 Конечное состояние не принадлежит множеству конечных состояний ДКА.")
                self.println("Цепочка не принадлежит языку")
            return

        # self.println(f"({state}, {word})")
        if len(word) > 1:
            self.println(f"(({state},{word[0]}), {word[1:]})")
            try:
                state = machine[state][word[0]]
            except KeyError:
                self.println(f"error: code 1 Ошибка. Отсутсвует переход для данного состояния: {word[0]}")
                self.println("Цепочка не принадлежит языку")
                return
            word = word[1:]
        else:
            self.println(f"(({state},{word[0]}), )")
            try:
                state = machine[state][word[0]]
            except KeyError:
                self.println(f"error: code 2 Ошибка. Отсутсвует переход для данного состояния: {word[0]}.")
                self.println("Цепочка не принадлежит языку")
                return
            word = ""
        self.check_word(word, machine, state)

    def println(self, text):
        current_datetime = datetime.now()
        self.log.setText(str(current_datetime) + ": " + str(text) + "\n" + self.log.text())
        logFile = open("log.txt", "a")
        logFile.write(f"{str(current_datetime)} : {str(text)}\n")
        logFile.close()
