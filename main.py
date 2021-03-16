import os
import random
import shutil
from datetime import datetime
from pathlib import Path

import barcode
import keyboard
import pandas as pd
from PySide2 import QtWidgets, QtGui, QtCore, QtSql
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *
from barcode.writer import ImageWriter

from fpdf import *

import addform
import mainwindow
import modelform
import statusform



# Главная форма
class MainApp(mainwindow.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, state=None):  # Переопределяем конструктор класса
        super(MainApp, self).__init__()  # Обязательно нужно вызвать метод супер класса
        self.setupUi(self)

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("CART_DB.db")
        self.db.open()

        self.modelTable_Select_status = QtSql.QSqlRelationalTableModel()
        self.modelTable_Insert_history = QtSql.QSqlRelationalTableModel()
        self.modelTable_Select_history = QtSql.QSqlRelationalTableModel()
        self.modelTable_Select_cart = QtSql.QSqlRelationalTableModel()
        self.checkBox.stateChanged.connect(lambda state=self.checkBox.isChecked(): self.MainApp_clicked_search_h())
        self.checkBox_All.stateChanged.connect(self.clicks_history)
        self.MainApp_spisok_cart()
        self.MainApp_spisok_history()

        self.spisok = []

        self.clicks = None
        self.clicks_history_ID = 0
        self.MainApp_combo_model()
        self.MainApp_combo_status()
        self.MainApp_combo_action()

        self.pB_add.clicked.connect(AddForm_open)
        self.guideDepartments.triggered.connect(StatusForm_open)
        self.guideModel.triggered.connect(ModelForm_open)

        self.pB_save.setEnabled(False)
        self.pB_delete.setEnabled(False)
        self.pB_edit.setEnabled(False)
        self.pB_save.clicked.connect(self.MainApp_clicked_pushButton_save)
        self.pB_delete.clicked.connect(self.MainApp_Delete_Cart)
        self.pB_clear_filter.clicked.connect(self.MainApp_clear_filter)
        self.pB_clear_filter_h.clicked.connect(self.MainApp_clear_filter_h)
        self.pB_edit.clicked.connect(self.MainApp_clicked_pushButton_edit)
        self.pB_print_select.clicked.connect(self.Barcode_print_g_Added)
        self.pB_print_select_2.clicked.connect(self.Barcode_print_Added)
        self.pB_excel.clicked.connect(self.uploading_to_Excel)
        self.pushButton_3.clicked.connect(self.report_for_period)
        self.pushButton_2.clicked.connect(self.refilled_for_period)
        self.pushButton_4.clicked.connect(self.status_report)
        self.pushButton_5.clicked.connect(self.action_report)

        self.comboBox_model.currentTextChanged.connect(self.MainApp_clicked_search)
        self.comboBox_status.currentTextChanged.connect(self.MainApp_clicked_search)
        self.comboBox_action.currentTextChanged.connect(self.MainApp_clicked_search_h)
        self.comboBox_status_h.currentTextChanged.connect(self.MainApp_clicked_search_h)

        self.dateEdit_min.setEnabled(False)
        self.dateEdit_max.setEnabled(False)
        self.dateEdit_min.dateChanged.connect(self.MainApp_clicked_search_h)
        self.dateEdit_max.dateChanged.connect(self.MainApp_clicked_search_h)
        self.dateEdit_min_otch.dateChanged.connect(self.MainApp_clicked_search_h)
        self.dateEdit_max_otch.dateChanged.connect(self.MainApp_clicked_search_h)

        self.lineEdit.setValidator(QtGui.QRegExpValidator(QRegExp("^([1-9][0-9]*|0)"), self))
        self.lineEdit.setEnabled(False)
        self.lineEdit.textChanged.connect(self.MainApp_vvod_nomera)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setFocus()
        self.tableView_select.doubleClicked.connect(self.tableView_select_doubleClicked)
        # self.tableView_history.changeEvent.connect(self.tableView_select_doubleClicked)

    # ----------------------------------Картриджи------------------------------------#
    # Ввод номера Баркода
    def MainApp_vvod_nomera(self):
        BarCod = self.lineEdit.text()
        self.comboBox_model.setCurrentIndex(0)
        self.comboBox_status.setCurrentIndex(0)
        self.comboBox_action.setCurrentIndex(0)
        self.comboBox_status_h.setCurrentIndex(0)
        keyboard.block_key('Enter')
        if len(BarCod) == 13:
            if self.MainApp_Select_Status(BarCod):  # Проверка на наличие номера в таблице Где
                self.spisok.append(BarCod)
                if self.spisok[0] == BarCod:  # Проверка на наличие номера в 0 индексе в списке
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setWindowTitle("Warning")
                    msgBox.information(self, "Warning", "Введен не верный ID")
                    self.lineEdit.clear()
                    self.spisok.clear()
                else:
                    self.MainApp_Update_Cart()
                    self.MainApp_Insert_History()
                    self.MainApp_Select_Cart()
                    self.spisok.remove(self.spisok[1])  # Удаление 1 индекса из списка
                    self.lineEdit.clear()
                    self.lineEdit.setFocus()
            else:
                self.spisok.clear()
                self.spisok.append(BarCod)
                if self.spisok[0] == BarCod:
                    self.MainApp_Select_Cart()
                    self.lineEdit.clear()
                else:
                    self.spisok.remove(self.spisok[0])  # Удаление 0 индекса из списка
                    self.lineEdit.clear()
                    self.MainApp_Select_Cart()
        else:
            return None

    # Вывод первоночального списка во вкладке Картриджи
    def MainApp_spisok_cart(self):
        self.modelTable_Select_cart.setTable("Cart")
        self.modelTable_Select_cart.setRelation(4, QSqlRelation("Status", "id", "status"))
        self.modelTable_Select_cart.setRelation(3, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_cart.setHeaderData(0, QtCore.Qt.Horizontal, "№")
        self.modelTable_Select_cart.setHeaderData(1, QtCore.Qt.Horizontal, "Номер")
        self.modelTable_Select_cart.setHeaderData(2, QtCore.Qt.Horizontal, "Фирма")
        self.modelTable_Select_cart.setHeaderData(3, QtCore.Qt.Horizontal, "Модель")
        self.modelTable_Select_cart.setHeaderData(4, QtCore.Qt.Horizontal, "Статус")
        self.modelTable_Select_cart.setHeaderData(5, QtCore.Qt.Horizontal, "Дата/Время")
        self.modelTable_Select_cart.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)
        self.modelTable_Select_cart.setSort(0,
                                            Qt.DescendingOrder)  # Устанавливаем сортировку по возрастанию данных по 0 колонке
        self.modelTable_Select_cart.select()
        self.tableView_select.setModel(self.modelTable_Select_cart)
        self.tableView_select.setStyleSheet("QHeaderView::section {background-color:gray}")
        self.tableView_select.setAlternatingRowColors(True)  # цвет четных и нечетных строк
        self.tableView_select.setSortingEnabled(True)
        self.tableView_select.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет редактирования
        self.tableView_select.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.tableView_select.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        # self.tableView_select.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # таблица по размеру содержимого
        # self.tableView_select.setSelectionBehavior(self.tableView_select.SelectRows)  # Разрешаем выделение строк
        # self.tableView_select.setSelectionMode(self.tableView_select.ExtendedSelection)  # режим выделения лишь одной ячейки в таблице

    # Вывод запроса по баркоду в таблице Картриджи
    def MainApp_Select_Cart(self):
        self.modelTable_Select_cart.setTable("Cart")
        self.modelTable_Select_cart.setFilter("cart.number= '" + self.spisok[0] + "' ")
        self.modelTable_Select_cart.setRelation(4, QSqlRelation("Status", "id", "status"))
        self.modelTable_Select_cart.setRelation(3, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_cart.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.modelTable_Select_cart.setHeaderData(1, QtCore.Qt.Horizontal, "Номер")
        self.modelTable_Select_cart.setHeaderData(2, QtCore.Qt.Horizontal, "Фирма")
        self.modelTable_Select_cart.setHeaderData(3, QtCore.Qt.Horizontal, "Модель")
        self.modelTable_Select_cart.setHeaderData(4, QtCore.Qt.Horizontal, "Статус")
        self.modelTable_Select_cart.setHeaderData(5, QtCore.Qt.Horizontal, "Дата/Время")
        self.modelTable_Select_cart.setEditStrategy(QtSql.QSqlRelationalTableModel.OnFieldChange)  # Сброс изменений
        self.modelTable_Select_cart.select()
        result_Select_Cart = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 1))
        int_BarCod = int(self.spisok[0])
        if result_Select_Cart == int_BarCod:
            self.tableView_select.setModel(self.modelTable_Select_cart)
            self.tableView_select.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            self.tableView_select.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            self.tableView_select.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            self.tableView_select.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            self.tableView_select.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            self.tableView_select.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            self.tableView_select.setSelectionMode(QAbstractItemView.SingleSelection)  # выбор диночного элемента
            self.tableView_select.setStyleSheet("QHeaderView::section {background-color:gray}")
            self.tableView_select.setCurrentIndex(
                self.modelTable_Select_cart.index(0, 1))  # Выбор первой ячейки (для удаления)
            self.tableView_select.setItemDelegate(QSqlRelationalDelegate())  # выбор из выподающего списк
            self.pB_save.setEnabled(True)
            self.pB_edit.setEnabled(True)
            self.pB_delete.setEnabled(True)
            self.pB_add.setEnabled(False)
            self.MainApp_Select_History()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Код отсутствует в базе. Желаете добавить?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            bttn = msgBox.exec_()
            if bttn == QMessageBox.Yes:
                qt_addform.lineEdit_Barcode.setText(self.spisok[0])
                qt_addform.show()
                self.lineEdit.clear()
                self.pB_save.setEnabled(True)
                self.pB_edit.setEnabled(True)
                self.pB_delete.setEnabled(True)
                self.pB_add.setEnabled(False)
                return 0
            elif bttn == QMessageBox.No:
                self.lineEdit.clear()
                self.spisok.clear()
                self.modelTable_Select_history.clear()
                self.MainApp_clear_filter()
                self.pB_save.setEnabled(False)
                self.pB_edit.setEnabled(False)
                self.pB_delete.setEnabled(False)
                self.pB_add.setEnabled(True)
                msgBox.close()

    # Фильтр по двойному клику в колонке Номер в таблице Картриджи
    def tableView_select_doubleClicked(self):
        if self.tableView_select.currentIndex().column() == 1:
            datas = self.tableView_select.currentIndex().data()
            self.spisok.append(str(datas))
            self.MainApp_Select_Cart()
            return QtCore.Qt.ItemIsEnabled
        else:
            return not QtCore.Qt.ItemIsEnabled

    # Выподающий список модели во вкладке Картриджи
    def MainApp_combo_model(self):
        model = QtSql.QSqlRelationalTableModel(self)
        model.setTable('Model')
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.setFilter("model!=''")
        column = model.fieldIndex('model')
        model.select()
        self.comboBox_model.setModel(model)
        self.comboBox_model.setModelColumn(column)

    # Выподающий список статуса во вкладке Картриджи
    def MainApp_combo_status(self):
        model = QtSql.QSqlTableModel(self)
        model.setTable('Status')
        model.setEditStrategy(
            QtSql.QSqlTableModel.OnManualSubmit)  # Все изменения будут кэшироваться в модели до тех пор, пока не будет вызвана функция submitAll() или revertAll ()
        model.setFilter("status!=''")
        column = model.fieldIndex('status')
        model.select()
        self.comboBox_status.setModel(model)
        self.comboBox_status.setModelColumn(column)
        self.comboBox_status_o.setModel(model)
        self.comboBox_status_o.setModelColumn(column)
        self.comboBox_status_h.setModel(model)
        self.comboBox_status_h.setModelColumn(column)

    # Поиск по фильтру из выподающего списка в таближе Картриджи
    def MainApp_clicked_search(self):
        model_box = self.comboBox_model.currentText()
        status_box = self.comboBox_status.currentText()
        TableModel = QtSql.QSqlTableModel()  # Временная модель таблицы Model
        TableModel.setTable('Model')
        TableModel.setFilter("Model.model= '" + model_box + "' ")
        TableModel.select()
        model_id = TableModel.data(TableModel.index(0, 0))
        TableStatus = QtSql.QSqlTableModel()  # Временная модель таблицы Status
        TableStatus.setTable('Status')
        TableStatus.setFilter("Status.status= '" + status_box + "' ")
        TableStatus.select()
        status_id = TableStatus.data(TableStatus.index(0, 0))
        self.modelTable_Select_cart.setTable("Cart")
        if model_id == 0 and status_id != 0:
            self.modelTable_Select_cart.setFilter("cart.status_id='" + str(status_id) + "' ")
        elif status_id == 0 and model_id != 0:
            self.modelTable_Select_cart.setFilter("cart.model_id= '" + str(model_id) + "' ")
        elif model_id != 0 and status_id != 0:
            self.modelTable_Select_cart.setFilter(
                "cart.model_id=" + str(model_id) + " AND " + "cart.status_id='" + str(status_id) + "' ")
        else:
            self.MainApp_spisok_cart()
        self.modelTable_Select_cart.setRelation(4, QSqlRelation("Status", "id", "status"))
        self.modelTable_Select_cart.setRelation(3, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_cart.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.modelTable_Select_cart.setHeaderData(1, QtCore.Qt.Horizontal, "Номер")
        self.modelTable_Select_cart.setHeaderData(2, QtCore.Qt.Horizontal, "Фирма")
        self.modelTable_Select_cart.setHeaderData(3, QtCore.Qt.Horizontal, "Модель")
        self.modelTable_Select_cart.setHeaderData(4, QtCore.Qt.Horizontal, "Статус")
        self.modelTable_Select_cart.setHeaderData(5, QtCore.Qt.Horizontal, "Дата/Время")
        self.modelTable_Select_cart.setEditStrategy(
            QtSql.QSqlRelationalTableModel.OnFieldChange)  # Все изменения в модели будут немедленно применены к базе данных
        self.modelTable_Select_cart.select()
        self.tableView_select.setModel(self.modelTable_Select_cart)
        self.tableView_select.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.tableView_select.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableView_select.setStyleSheet("QHeaderView::section {background-color:gray}")
        self.tableView_select.setAlternatingRowColors(True)  # цвет четных и нечетных строк
        self.tableView_select.setSortingEnabled(True)
        self.tableView_select.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет редактирования

    # Обновление в таблице Картриджи
    def MainApp_Update_Cart(self):
        todey = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        Cod_status = self.spisok[1]
        model = QtSql.QSqlTableModel(self)
        model.setTable('Status')
        model.setFilter("Status.id= '" + Cod_status + "' ")
        model.select()
        # BarCod_status = model.data(model.index(0, 1))
        self.modelTable_Select_cart.selectRow(0)
        self.modelTable_Select_cart.setData(self.modelTable_Select_cart.index(0, 4), Cod_status)
        self.modelTable_Select_cart.setData(self.modelTable_Select_cart.index(0, 5), str(todey))
        self.modelTable_Select_cart.submitAll()

    #  Удаление из таблицы Картриджи
    def MainApp_Delete_Cart(self):
        msgBox = QtWidgets.QMessageBox.warning(self, "Warning", "Желаете удалить выбранную строку?",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if msgBox == QtWidgets.QMessageBox.Yes:
            self.clicks = 0
            self.MainApp_Insert_History()
            query = QtSql.QSqlQuery("DELETE "
                                    " FROM Cart"
                                    " WHERE Cart.number = " + self.spisok[0] + "")  # объект запроса
            while query.next():
                query.record().clear()
            self.MainApp_spisok_cart()
            self.spisok.clear()
            self.lineEdit.setFocus()
            self.modelTable_Select_cart.clear()
            self.MainApp_clear_filter()
        elif msgBox == QMessageBox.No:
            self.lineEdit.setFocus()

    # Очистка фильтра во вкладке Картриджи
    def MainApp_clear_filter(self):
        self.spisok.clear()
        self.lineEdit.clear()
        self.MainApp_spisok_cart()

        self.MainApp_clear_filter_h()
        self.MainApp_vvod_nomera()
        self.lineEdit.setFocus()
        self.comboBox_model.setCurrentIndex(0)
        self.comboBox_status.setCurrentIndex(0)
        self.pB_save.setEnabled(False)
        self.pB_add.setEnabled(True)
        self.pB_edit.setEnabled(False)
        self.pB_delete.setEnabled(False)

    # Кнопка сохранить
    def MainApp_clicked_pushButton_save(self):
        todey = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.modelTable_Select_cart.selectRow(0)
        self.modelTable_Select_cart.setData(self.modelTable_Select_cart.index(0, 5), str(todey))
        self.modelTable_Select_cart.submitAll()
        self.MainApp_Insert_History()
        self.MainApp_Select_Cart()
        self.lineEdit.setFocus()

    # Кнопка редактирование
    def MainApp_clicked_pushButton_edit(self):
        if self.pB_edit.isChecked():
            self.tableView_select.setEditTriggers(QAbstractItemView.AllEditTriggers)
        else:
            self.tableView_select.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # -----------------------------------Журнал--------------------------------------#
    def clicks_history(self):  # Проверка состояния таблицы
        if self.clicks_history_ID == 0:
            self.MainApp_spisok_history()
        elif self.clicks_history_ID == 1:
            self.MainApp_Select_History()
        elif self.clicks_history_ID == 2:
            self.MainApp_clicked_search_h()

    def MainApp_spisok_history(self):
        self.clicks_history_ID = 0
        self.template_History()
        row = 0
        query = QtSql.QSqlQuery("SELECT "
                                "History.id, "
                                "Cart.number, "
                                "Model.model, "
                                "Status.status, "
                                "History.datatime, "
                                "tb_Action.action "
                                "FROM History "
                                "JOIN Cart ON History.cart_id = Cart.id "
                                "JOIN Model ON History.model_id = Model.id "
                                "JOIN Status ON History.status_id = Status.id "
                                "JOIN tb_Action ON History.action_id = tb_Action.id")  # объект запроса
        self.TableWidget_History.setRowCount(0)
        while query.next():
            self.TableWidget_History.insertRow(row)
            id = QtWidgets.QTableWidgetItem(str(query.value(0)))
            number = QtWidgets.QTableWidgetItem(str(query.value(1)))
            model = QtWidgets.QTableWidgetItem(str(query.value(2)))
            status = QtWidgets.QTableWidgetItem(str(query.value(3)))
            datetime = QtWidgets.QTableWidgetItem(str(query.value(4)))
            action = QtWidgets.QTableWidgetItem(str(query.value(5)))
            self.TableWidget_History.setItem(row, 0, id)
            self.TableWidget_History.setItem(row, 1, number)
            self.TableWidget_History.setItem(row, 2, model)
            self.TableWidget_History.setItem(row, 3, status)
            self.TableWidget_History.setItem(row, 4, datetime)
            self.TableWidget_History.setItem(row, 5, action)
            cart_id = query.value(1)
            self.chkBoxItem = QTableWidgetItem()
            self.chkBoxItem.setText(str(cart_id))
            self.chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if self.checkBox_All.isChecked():
                self.chkBoxItem.setCheckState(QtCore.Qt.Checked)
            else:
                self.chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.TableWidget_History.setItem(row, 1, self.chkBoxItem)
            row = row + 1

    # Выподающий список действие во вкладке Журнал
    def MainApp_combo_action(self):
        model = QtSql.QSqlRelationalTableModel(self)
        model.setTable('tb_Action')
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.setFilter("action!=''")
        column = model.fieldIndex('action')
        model.select()
        self.comboBox_action.setModel(model)
        self.comboBox_action.setModelColumn(column)
        self.comboBox_action_o.setModel(model)
        self.comboBox_action_o.setModelColumn(column)

    # Выподающий список статуса во вкладке Журнал
    def MainApp_combo_status_h(self):
        model = QtSql.QSqlTableModel(self)
        model.setTable('Status')
        model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model.setFilter("status!=''")
        column = model.fieldIndex('status')
        model.select()
        self.comboBox_status_h.setModel(model)
        self.comboBox_status_h.setModelColumn(column)

    # Очистка фильтра во вкладке Журнал
    def MainApp_clear_filter_h(self):
        self.dateEdit_min.setDateTime(datetime.today())
        self.dateEdit_max.setDateTime(datetime.today())
        self.MainApp_spisok_history()
        self.comboBox_action.setCurrentIndex(0)
        self.comboBox_status_h.setCurrentIndex(0)

    # Проверка из какой таблицы баркод
    def MainApp_Select_Status(self, BarCod):
        self.modelTable_Select_status.setTable("Status")
        self.modelTable_Select_status.setFilter("Status.id= '" + str(BarCod) + "' ")
        self.modelTable_Select_status.select()
        result_Select = self.modelTable_Select_status.data(self.modelTable_Select_status.index(0, 0))
        return result_Select

    # Проверка на повторение рандомного кода
    def checking_for_random_code_repetition(self, BarCod):
        self.modelTable_Select_cart.setTable("Cart")
        self.modelTable_Select_cart.setFilter("Cart.number= '" + str(BarCod) + "' ")
        self.modelTable_Select_cart.select()
        result_Select_Gde = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 1))
        return result_Select_Gde

    # Добавление в таблицу Журнал
    def MainApp_Insert_History(self):
        todey = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.modelTable_Insert_history.setTable("History")
        self.modelTable_Select_cart.setRelation(3, QSqlRelation("Model", "id", "id"))
        self.modelTable_Select_cart.setRelation(4, QSqlRelation("Status", "id", "id"))
        self.modelTable_Select_cart.setFilter("cart.number=" + self.spisok[0])
        self.modelTable_Select_cart.select()
        result_cart_id = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 0))
        result_model_id = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 3))
        result_status_id = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 4))
        row = self.modelTable_Insert_history.rowCount()
        self.modelTable_Insert_history.insertRow(row)
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 1), str(result_cart_id))
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 2), str(result_model_id))
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 3), str(result_status_id))
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 4), str(todey))
        if self.clicks == 0:
            TableAction = QtSql.QSqlTableModel()  # Временная модель таблицы Action
            TableAction.setTable('tb_Action')
            TableAction.setFilter("tb_Action.action = 'Удаление' ")
            TableAction.select()
            action_id = TableAction.data(TableAction.index(0, 0))
            self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 5), action_id)
        else:
            TableAction = QtSql.QSqlTableModel()  # Временная модель таблицы Action
            TableAction.setTable('tb_Action')
            TableAction.setFilter("tb_Action.action = 'Перемещение' ")
            TableAction.select()
            action_id = TableAction.data(TableAction.index(0, 0))
            self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 5), action_id)
        self.modelTable_Insert_history.submitAll()

    # Шаблон таблицы Журнал
    def template_History(self):
        self.TableWidget_History.setRowCount(0)
        self.TableWidget_History.setColumnCount(6)
        self.TableWidget_History.setHorizontalHeaderLabels(
            ["№", "Номер", "Модель", "Статус", "Дата/Время", "Действие"])  # Устанавливаем заголовки таблицы
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(0,
                                                                         QHeaderView.ResizeToContents)  # Ширина по содержимому
        self.TableWidget_History.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TableWidget_History.setStyleSheet("QHeaderView::section {background-color:gray}")
        self.TableWidget_History.setAlternatingRowColors(True)  # цвет четных и нечетных строк
        # Устанавливаем выравнивание на заголовки
        self.TableWidget_History.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.TableWidget_History.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.TableWidget_History.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.TableWidget_History.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.TableWidget_History.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.TableWidget_History.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)
        # Устанавливаем всплывающие подсказки на заголовки
        self.TableWidget_History.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.TableWidget_History.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.TableWidget_History.horizontalHeaderItem(2).setToolTip("Column 3 ")
        self.TableWidget_History.horizontalHeaderItem(3).setToolTip("Column 4 ")
        self.TableWidget_History.horizontalHeaderItem(4).setToolTip("Column 5 ")
        self.TableWidget_History.horizontalHeaderItem(5).setToolTip("Column 6 ")
        # Устанавливаем ширины колонок
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.TableWidget_History.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        # делаем ресайз колонок по содержимому
        # self.TableWidget.resizeColumnsToContents()
        # self.TableWidget_History.setSortingEnabled(True)  # Возможность сортироваки

    # Фильтр по баркоду в таблице Журнал
    def MainApp_Select_History(self):
        self.clicks_history_ID = 1
        self.template_History()
        row = 0
        query = QtSql.QSqlQuery("SELECT "
                                "History.id, "
                                "Cart.number, "
                                "Model.model, "
                                "Status.status, "
                                "History.datatime, "
                                "tb_Action.action "
                                " FROM History"
                                " JOIN Cart ON History.cart_id = Cart.id "
                                " JOIN Model ON History.model_id = Model.id "
                                " JOIN Status ON History.status_id = Status.id "
                                " JOIN tb_Action ON History.action_id = tb_Action.id"
                                " WHERE Cart.number = " + self.spisok[0] + "")  # объект запроса
        self.TableWidget_History.setRowCount(0)
        while query.next():
            self.TableWidget_History.insertRow(row)
            id = QtWidgets.QTableWidgetItem(str(query.value(0)))
            number = QtWidgets.QTableWidgetItem(str(query.value(1)))
            model = QtWidgets.QTableWidgetItem(str(query.value(2)))
            status = QtWidgets.QTableWidgetItem(str(query.value(3)))
            datetime = QtWidgets.QTableWidgetItem(str(query.value(4)))
            action = QtWidgets.QTableWidgetItem(str(query.value(5)))
            self.TableWidget_History.setItem(row, 0, id)
            self.TableWidget_History.setItem(row, 1, number)
            self.TableWidget_History.setItem(row, 2, model)
            self.TableWidget_History.setItem(row, 3, status)
            self.TableWidget_History.setItem(row, 4, datetime)
            self.TableWidget_History.setItem(row, 5, action)
            cart_id = query.value(1)
            self.chkBoxItem = QTableWidgetItem()
            self.chkBoxItem.setText(str(cart_id))
            self.chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if self.checkBox_All.isChecked():
                self.chkBoxItem.setCheckState(QtCore.Qt.Checked)
            else:
                self.chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.TableWidget_History.setItem(row, 1, self.chkBoxItem)
            row = row + 1

    # Проверка чекбокса для даты
    def checkBox_clicked(self):
        if self.checkBox.isChecked():
            self.dateEdit_min.setEnabled(True)
            self.dateEdit_max.setEnabled(True)
            return True
        else:
            self.dateEdit_min.setEnabled(False)
            self.dateEdit_max.setEnabled(False)
            return False

    # Поиск по фильтру из выподающего списка в таближе Журнал
    def MainApp_clicked_search_h(self):
        self.clicks_history_ID = 2
        action_box = self.comboBox_action.currentText()
        TableAction = QtSql.QSqlTableModel()  # Временная модель таблицы Action
        TableAction.setTable('tb_Action')
        TableAction.setFilter("tb_Action.action = '" + action_box + "' ")
        TableAction.select()
        action_id = TableAction.data(TableAction.index(0, 0))

        status_box_h = self.comboBox_status_h.currentText()
        TableStatus = QtSql.QSqlTableModel()  # Временная модель таблицы Status
        TableStatus.setTable('Status')
        TableStatus.setFilter("Status.status= '" + status_box_h + "' ")
        TableStatus.select()
        status_id = TableStatus.data(TableStatus.index(0, 0))

        date_Changed_min = self.dateEdit_min.date().toString('yyyy-MM-dd 00:00:00')
        date_Changed_max = self.dateEdit_max.date().toString('yyyy-MM-dd 23:59:59')

        self.template_History()

        if self.spisok:  # Если введен баркод
            if action_box == '-Выбрать-' and status_box_h != '-Выбрать-' and self.checkBox_clicked():  # 011
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""                                          
                                             " AND History.status_id = " + str(status_id) + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box != '-Выбрать-' and status_box_h == '-Выбрать-' and self.checkBox_clicked():  # 101
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""                                          
                                             " AND History.action_id = " + str(action_id) + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box != '-Выбрать-' and status_box_h != '-Выбрать-' and self.checkBox_clicked():  # 111
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""                                          
                                             " AND History.action_id = " + str(action_id) + ""
                                             " AND History.status_id = " + str(status_id) + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box == '-Выбрать-' and status_box_h == '-Выбрать-' and self.checkBox_clicked():  # 001
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box != '-Выбрать-' and status_box_h == '-Выбрать-' and not self.checkBox_clicked():  # 100
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""                                          
                                             " AND History.action_id = " + str(action_id) + "")
            elif action_box == '-Выбрать-' and status_box_h != '-Выбрать-' and not self.checkBox_clicked():  # 010
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""                                          
                                             " AND History.status_id = " + str(status_id) + "")
            elif action_box != '-Выбрать-' and status_box_h != '-Выбрать-' and not self.checkBox_clicked():  # 110
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.cart_id = " + self.spisok[0] + ""                                          
                                             " AND History.action_id = " + str(action_id) + ""
                                             " AND History.status_id = " + str(status_id) + "")
            else:
                self.MainApp_Select_History()
        else:  # Если баркод не введен
            if action_box == '-Выбрать-' and status_box_h != '-Выбрать-' and self.checkBox_clicked():  # 011
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.status_id = " + str(status_id) + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box != '-Выбрать-' and status_box_h == '-Выбрать-' and self.checkBox_clicked():  # 101
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.action_id = " + str(action_id) + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box != '-Выбрать-' and status_box_h != '-Выбрать-' and self.checkBox_clicked():  # 111
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.action_id = " + str(action_id) + ""
                                             " AND History.status_id = " + str(status_id) + ""
                                             " AND History.datatime >= '" + date_Changed_min + "'"
                                             " AND History.datatime <= '" + date_Changed_max + "'")
            elif action_box == '-Выбрать-' and status_box_h == '-Выбрать-' and self.checkBox_clicked():  # 001
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE history.datatime >= '" + date_Changed_min + "'"
                                             " AND history.datatime <= '" + date_Changed_max + "'")
            elif action_box != '-Выбрать-' and status_box_h == '-Выбрать-' and not self.checkBox_clicked():  # 100
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, " 
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History "
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id "
                                             " WHERE History.action_id = " + str(action_id) + "")
            elif action_box == '-Выбрать-' and status_box_h != '-Выбрать-' and not self.checkBox_clicked():  # 010
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History "
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id "
                                             " WHERE History.status_id=" + str(status_id) + "")
            elif action_box != '-Выбрать-' and status_box_h != '-Выбрать-' and not self.checkBox_clicked():  # 110
                self.query = QtSql.QSqlQuery("SELECT "
                                             "History.id, "
                                             "Cart.number, "
                                             "Model.model, "
                                             "Status.status, "
                                             "History.datatime, "
                                             "tb_Action.action "
                                             " FROM History"                                    
                                             " JOIN Cart ON History.cart_id = Cart.id "
                                             " JOIN Model ON History.model_id = Model.id "
                                             " JOIN Status ON History.status_id = Status.id "
                                             " JOIN tb_Action ON History.action_id = tb_Action.id"
                                             " WHERE History.action_id = " + str(action_id) + ""
                                             " AND History.status_id = " + str(status_id) + "")
            else:
                self.MainApp_spisok_history()
        row = 0
        while self.query.next():
            self.TableWidget_History.insertRow(row)
            id = QtWidgets.QTableWidgetItem(str(self.query.value(0)))
            number = QtWidgets.QTableWidgetItem(str(self.query.value(1)))
            model = QtWidgets.QTableWidgetItem(str(self.query.value(2)))
            status = QtWidgets.QTableWidgetItem(str(self.query.value(3)))
            datetime = QtWidgets.QTableWidgetItem(str(self.query.value(4)))
            action = QtWidgets.QTableWidgetItem(str(self.query.value(5)))
            self.TableWidget_History.setItem(row, 0, id)
            self.TableWidget_History.setItem(row, 1, number)
            self.TableWidget_History.setItem(row, 2, model)
            self.TableWidget_History.setItem(row, 3, status)
            self.TableWidget_History.setItem(row, 4, datetime)
            self.TableWidget_History.setItem(row, 5, action)
            cart_id = self.query.value(1)
            self.chkBoxItem = QTableWidgetItem()
            # self.chkBoxItem = QCheckBox()
            self.chkBoxItem.setText(str(cart_id))
            self.chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if self.checkBox_All.isChecked():
                self.chkBoxItem.setCheckState(QtCore.Qt.Checked)
            else:
                self.chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.TableWidget_History.setItem(row, 1, self.chkBoxItem)
            row = row + 1


    # --------------------------------Отчеты и выгрузки----------------------------------#
    # Выгрузка в Excel
    def uploading_to_Excel(self):
        count = self.TableWidget_History.rowCount()
        if count >= 1:
            l_number = list()
            l_firma = list()
            l_model = list()
            l_status = list()
            l_date = list()
            for elem in range(count):
                number = self.modelTable_Select_cart.record(elem).value(1)
                firma = self.modelTable_Select_cart.record(elem).value(2)
                model = self.modelTable_Select_cart.record(elem).value(3)
                status = self.modelTable_Select_cart.record(elem).value(4)
                date = self.modelTable_Select_cart.record(elem).value(5)
                l_number.append(number)
                l_firma.append(firma)
                l_model.append(model)
                l_status.append(status)
                l_date.append(date)
                df = pd.DataFrame(
                    {'Номер': l_number, 'Фирма': l_firma, 'Модель': l_model, 'Статус': l_status, 'Дата': l_date})
                writer = pd.ExcelWriter("./test1.xlsx", engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                format1 = workbook.add_format({'num_format': '###'})
                worksheet.set_column('A:A', 18, format1)
                worksheet.set_column('E:E', 18)
                worksheet.set_column('D:D', 18)
                writer.save()
            os.startfile(r'.\test1.xlsx')
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных по указанным параметрам")
            return msgBox

    # Печать добавленных штрих кодов
    def Barcode_print_Added(self):
        count = self.TableWidget_History.rowCount()
        if count >= 1:
            path = Path(r".\temp_png")
            path.mkdir(exist_ok=True)
            l_number = list()
            l_item_name = list()
            item_name = 1
            for i in range(count):
                if self.TableWidget_History.item(i, 1).checkState() == QtCore.Qt.Checked:
                    number = self.TableWidget_History.item(i, 1).text()
                    l_number.append(number)
                else:
                    pass
            for elem in range(len(l_number)):
                barCodeImage = barcode.codex.Code39(str(l_number[elem]), writer=ImageWriter(), add_checksum=False)
                file_name = barCodeImage.save(path / str(item_name),
                                              {"quiet_zone": 2, "text_distance": 1, "module_height": 8})
                l_item_name.append(file_name)
                item_name += 1
            df = pd.DataFrame(l_item_name)
            writer = pd.ExcelWriter("./test.xlsx", engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', header=False, index=False, merge_cells=True, startcol=-1)
            worksheet = writer.sheets['Sheet1']
            worksheet.set_column(0, 3, 21.40)
            worksheet.set_default_row(35)

            # Вставьте изображение с масштабированием.
            y_offset = 0
            x_offset = 0
            col = "A1"
            for i in range(0, len(l_number), 1):
                if i == 22:
                    y_offset = 0
                    x_offset = 156
                elif i == 44:
                    y_offset = 0
                    x_offset = 312
                elif i == 66:
                    y_offset = 0
                    x_offset = 468
                elif i == 88:
                    y_offset = 0
                    x_offset = 624
                worksheet.insert_image(col, l_item_name[i], {'x_offset': x_offset, 'y_offset': y_offset, 'x_scale': 0.25, 'y_scale': 0.3})
                y_offset += 46
                i += 1
            writer.save()
            os.startfile(r'.\test.xlsx')
            shutil.rmtree(path)  # Удаляет текущую директорию и все поддиректории
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных по указанным параметрам")
            return msgBox

    def Barcode_print_g_Added(self):
        count = self.TableWidget_History.rowCount()
        if count >= 1:
            path = Path(r".\temp_png")
            path.mkdir(exist_ok=True)
            l_number = list()
            l_item_name = list()
            item_name = 1
            for i in range(count):
                if self.TableWidget_History.item(i, 1).checkState() == QtCore.Qt.Checked:
                    number = self.TableWidget_History.item(i, 1).text()
                    l_number.append(number)
                else:
                    pass
            for elem in range(len(l_number)):
                barCodeImage = barcode.codex.Code39(str(l_number[elem]), writer=ImageWriter(), add_checksum=False)
                file_name = barCodeImage.save(path / str(item_name),
                                              {"quiet_zone": 2, "text_distance": 1, "module_height": 8})
                l_item_name.append(file_name)
                item_name += 1
            df = pd.DataFrame(l_item_name)
            writer = pd.ExcelWriter("./test.xlsx", engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', header=False, index=False, merge_cells=True, startcol=-1)
            worksheet = writer.sheets['Sheet1']
            # Вставьте изображение с масштабированием.
            y_offset = 0
            x_offset = 0
            col = "A1"
            for i in range(0, len(l_number), 1):
                if i == 18:
                    y_offset = 0
                    x_offset = 187
                elif i == 36:
                    y_offset = 0
                    x_offset = 374
                elif i == 54:
                    y_offset = 0
                    x_offset = 561
                elif i == 72:
                    y_offset = 0
                    x_offset = 748
                worksheet.insert_image(col, l_item_name[i],
                                       {'x_offset': x_offset, 'y_offset': y_offset, 'x_scale': 0.25, 'y_scale': 0.3})
                if i % 2 == 0:
                    y_offset += 45
                else:
                    y_offset += 80
                i += 1
            writer.save()
            os.startfile(r'.\test.xlsx')
            shutil.rmtree(path)  # Удаляет текущую директорию и все поддиректории
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных по указанным параметрам")
            return msgBox

    # Класс CustomPDF
    class CustomPDF(FPDF):
        #  нижний колонтитул
        def footer(self):
            self.set_y(-10)
            self.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
            self.set_font('DejaVu', 'I', 8)
            # Добавляем номер страницы
            page = 'Страница ' + str(self.page_no()) + '/{nb}'
            self.cell(0, 10, page, 0, 0, 'C')

    # Отчет по движению картриждей за период
    def report_for_period(self):
        todey = datetime.today().strftime("%Y-%m-%d")
        date_Changed_min_o = self.dateEdit_min_otch.dateTime().toString('yyyy-MM-dd 00:00:00')
        date_Changed_max_o = self.dateEdit_max_otch.dateTime().toString('yyyy-MM-dd 23:59:59')
        date_min = self.dateEdit_min_otch.date().toString('dd-MM-yyyy')
        date_max = self.dateEdit_max_otch.date().toString('dd-MM-yyyy')
        #  Выборка из журнала
        self.modelTable_Select_history.setTable("History")
        self.modelTable_Select_history.setRelation(1, QSqlRelation("Cart", "id", "number"))
        self.modelTable_Select_history.setRelation(2, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_history.setRelation(3, QSqlRelation("Status", "id", "status"))
        self.modelTable_Select_history.setRelation(5, QSqlRelation("Action", "id", "action"))
        self.modelTable_Select_history.setFilter(
            "history.datatime >= '" + date_Changed_min_o + "' AND history.datatime <= '" + date_Changed_max_o + "' ")
        self.modelTable_Select_history.setSort(0,
                                               Qt.DescendingOrder)  # Устанавливаем сортировку по возрастанию данных по 0 колонке
        self.modelTable_Select_history.select()
        count = self.TableWidget_History.rowCount()
        if count >= 1:
            l_number = []
            l_model = []
            l_status = []
            l_date = []
            l_action = []
            for elem in range(count):
                number = self.modelTable_Select_history.record(elem).value(1)
                status = self.modelTable_Select_history.record(elem).value(3)
                date = self.modelTable_Select_history.record(elem).value(4)
                action = self.modelTable_Select_history.record(elem).value(5)
                l_number.append(number)
                l_status.append(status)
                l_date.append(date)
                l_action.append(action)
                self.modelTable_Select_cart.setTable("Cart")
                self.modelTable_Select_cart.setFilter("cart.number= '" + str(number) + "' ")
                self.modelTable_Select_cart.select()
                model = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 2))
                l_model.append(model)

            pdf = qt_mainform.CustomPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            #  Добавление шрифта для кириллицы
            pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
            pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
            pdf.add_font('DejaVu', 'I', 'fonts/DejaVuSansCondensed-Oblique.ttf', uni=True)
            pdf.add_font('DejaVu', 'BI', 'fonts/DejaVuSansCondensed-BoldOblique.ttf', uni=True)
            # Устанавливаем лого
            pdf.image(r'images\RKIB.jpg', 25, 10, 25)
            # Добавляем адрес
            pdf.set_font('DejaVu', 'I', 12)
            pdf.cell(130)
            pdf.cell(0, 5, 'БУЗ УР «РКИБ МЗ УР»', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'г. Ижевск, ул. Труда, 17', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'тел./факс:(3412)21-86-94', ln=1)
            pdf.ln(15)  # Разрыв линии
            #  Заголовок
            pdf.set_font('DejaVu', 'B', 14)
            s = 'Отчет по движению картриждей за период'
            w = pdf.get_string_width(s) + 6  # Вычисляем ширину названия и позицию
            pdf.set_x((210 - w) / 2)
            pdf.cell(w, 5, s, 0, 2,
                     'C')  # В вышеприведенном коде: ширина — 60, высота — 10, текст — Powered by FPDF., граница ячейки — 0, текущая позиция после вывода ячейки — 1, выравнивание текста в ячейке — C(по центру).
            pdf.ln(2)
            pdf.set_x(70)
            pdf.cell(35, 5, 'с ' + str(date_min), 0, 0, 'C')
            pdf.cell(35, 5, ' по ' + str(date_max), 0, 2, 'C')
            pdf.ln(10)  # Разрыв строки
            #  Заполнение таблицы
            pdf.set_x(15)  # Отступ
            pdf.cell(35, 5, str("Номер"), border=1, align='C')
            pdf.cell(30, 5, str("Модель"), border=1, align='C')
            pdf.cell(45, 5, str("Статус"), border=1, align='C')
            pdf.cell(45, 5, str("Дата"), border=1, align='C')
            pdf.cell(35, 5, str("Действие"), border=1, ln=1, align='C')
            for i in range(count):
                pdf.set_font('DejaVu', '', 11)
                pdf.set_x(15)  # Отступ
                pdf.cell(35, 5, str(l_number[i]), border=1, align='C')
                pdf.cell(30, 5, str(l_model[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_status[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_date[i]), border=1, align='C')
                pdf.cell(35, 5, str(l_action[i]), border=1, ln=1, align='C')
            pdf.ln()
            pdf.cell(5)
            pdf.cell(0, 5, 'Количество: ' + str(count), ln=1)
            pdf.output(str(todey) + "-движение за период.pdf")
            os.startfile(str(todey) + "-движение за период.pdf")
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных за указанный период")
        self.MainApp_clear_filter()

    # Отчет заправлено картриждей за период
    def refilled_for_period(self):
        todey = datetime.today().strftime("%Y-%m-%d")
        date_Changed_min_o = self.dateEdit_min_otch.dateTime().toString('yyyy-MM-dd 00:00:00')
        date_Changed_max_o = self.dateEdit_max_otch.dateTime().toString('yyyy-MM-dd 23:59:59')
        date_min = self.dateEdit_min_otch.date().toString('dd-MM-yyyy')
        date_max = self.dateEdit_max_otch.date().toString('dd-MM-yyyy')
        #  Выборка из журнала
        self.modelTable_Select_history.setTable("History")
        self.modelTable_Select_history.setRelation(1, QSqlRelation("Cart", "id", "number"))
        self.modelTable_Select_history.setRelation(2, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_history.setRelation(3, QSqlRelation("Status", "id", "status"))
        self.modelTable_Select_history.setRelation(5, QSqlRelation("Action", "id", "action"))
        self.modelTable_Select_history.setFilter(
            "history.datatime >= '" + date_Changed_min_o + "' AND history.datatime <= '" + date_Changed_max_o + "' AND history.status_id = '" + str(
                1410104600456) + "' ")
        self.modelTable_Select_history.setSort(0,
                                               Qt.DescendingOrder)  # Устанавливаем сортировку по возрастанию данных по 0 колонке
        self.modelTable_Select_history.select()
        count = self.modelTable_Select_history.rowCount()
        if count >= 1:
            l_number = []
            l_model = []
            l_status = []
            l_date = []
            l_action = []
            for elem in range(count):
                number = self.modelTable_Select_history.record(elem).value(1)
                status = self.modelTable_Select_history.record(elem).value(3)
                date = self.modelTable_Select_history.record(elem).value(4)
                action = self.modelTable_Select_history.record(elem).value(5)
                l_number.append(number)
                l_status.append(status)
                l_date.append(date)
                l_action.append(action)
                self.modelTable_Select_cart.setTable("Cart")
                self.modelTable_Select_cart.setFilter("cart.number= '" + str(number) + "' ")
                self.modelTable_Select_cart.select()
                model = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 2))
                l_model.append(model)

            pdf = qt_mainform.CustomPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            #  Добавление шрифта для кириллицы
            pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
            pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
            pdf.add_font('DejaVu', 'I', 'fonts/DejaVuSansCondensed-Oblique.ttf', uni=True)
            pdf.add_font('DejaVu', 'BI', 'fonts/DejaVuSansCondensed-BoldOblique.ttf', uni=True)
            # Устанавливаем лого
            pdf.image(r'images\RKIB.jpg', 25, 10, 25)
            # Добавляем адрес
            pdf.set_font('DejaVu', 'I', 12)
            pdf.cell(130)
            pdf.cell(0, 5, 'БУЗ УР «РКИБ МЗ УР»', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'г. Ижевск, ул. Труда, 17', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'тел./факс:(3412)21-86-94', ln=1)
            pdf.ln(15)  # Разрыв линии
            #  Заголовок
            pdf.set_font('DejaVu', 'B', 14)
            s = 'Отчет по заправке картриждей за период'
            w = pdf.get_string_width(s) + 6  # Вычисляем ширину названия и позицию
            pdf.set_x((210 - w) / 2)
            pdf.cell(w, 5, s, 0, 2,
                     'C')  # В вышеприведенном коде: ширина — 60, высота — 10, текст — Powered by FPDF., граница ячейки — 0, текущая позиция после вывода ячейки — 1, выравнивание текста в ячейке — C(по центру).
            pdf.ln(2)
            pdf.set_x(70)
            pdf.cell(35, 5, 'с ' + str(date_min), 0, 0, 'C')
            pdf.cell(35, 5, ' по ' + str(date_max), 0, 2, 'C')
            pdf.ln(10)  # Разрыв строки
            #  Заполнение таблицы
            pdf.set_x(15)  # Отступ
            pdf.cell(35, 5, str("Номер"), border=1, align='C')
            pdf.cell(30, 5, str("Модель"), border=1, align='C')
            pdf.cell(45, 5, str("Статус"), border=1, align='C')
            pdf.cell(45, 5, str("Дата"), border=1, align='C')
            pdf.cell(35, 5, str("Действие"), border=1, ln=1, align='C')
            for i in range(count):
                pdf.set_font('DejaVu', '', 11)
                pdf.set_x(15)  # Отступ
                pdf.cell(35, 5, str(l_number[i]), border=1, align='C')
                pdf.cell(30, 5, str(l_model[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_status[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_date[i]), border=1, align='C')
                pdf.cell(35, 5, str(l_action[i]), border=1, ln=1, align='C')
            pdf.ln()
            pdf.cell(5)
            pdf.cell(0, 5, 'Количество: ' + str(count), ln=1)
            pdf.output(str(todey) + "-заправлено за период.pdf")
            os.startfile(str(todey) + "-заправлено за период.pdf")
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных за указанный период")
        self.MainApp_clear_filter()

    # Отчет по статусу за период
    def status_report(self):
        todey = datetime.today().strftime("%Y-%m-%d")
        status_box_o = self.comboBox_status_o.currentText()
        TableStatus = QtSql.QSqlTableModel()  # Временная модель таблицы Status
        TableStatus.setTable('Status')
        TableStatus.setFilter("Status.status= '" + status_box_o + "' ")
        TableStatus.select()
        status_id = TableStatus.data(TableStatus.index(0, 0))

        date_Changed_min_o = self.dateEdit_min_otch.dateTime().toString('yyyy-MM-dd 00:00:00')
        date_Changed_max_o = self.dateEdit_max_otch.dateTime().toString('yyyy-MM-dd 23:59:59')
        date_min = self.dateEdit_min_otch.date().toString('dd-MM-yyyy')
        date_max = self.dateEdit_max_otch.date().toString('dd-MM-yyyy')
        #  Выборка из журнала
        self.modelTable_Select_history.setTable("History")
        self.modelTable_Select_history.setRelation(1, QSqlRelation("Cart", "id", "number"))
        self.modelTable_Select_history.setRelation(2, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_history.setRelation(3, QSqlRelation("Status", "id", "status"))
        if status_box_o != '-Выбрать-':
            self.modelTable_Select_history.setFilter(
                "history.datatime >= '" + date_Changed_min_o + "' AND history.datatime <= '" + date_Changed_max_o + "' AND history.status_id = '" + str(
                    status_id) + "' ")
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Не выбран статус")
            return 0

        self.modelTable_Select_history.setSort(0,
                                               Qt.DescendingOrder)  # Устанавливаем сортировку по возрастанию данных по 0 колонке
        self.modelTable_Select_history.select()
        count = self.modelTable_Select_history.rowCount()
        if count >= 1:
            l_number = []
            l_model = []
            l_status = []
            l_date = []
            for elem in range(count):
                number = self.modelTable_Select_history.record(elem).value(1)
                status = self.modelTable_Select_history.record(elem).value(3)
                date = self.modelTable_Select_history.record(elem).value(4)
                action = self.modelTable_Select_history.record(elem).value(5)
                l_number.append(number)
                l_status.append(status)
                l_date.append(date)
                self.modelTable_Select_cart.setTable("Cart")
                self.modelTable_Select_cart.setFilter("cart.number= '" + str(number) + "' ")
                self.modelTable_Select_cart.select()
                model = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 2))
                l_model.append(model)

            pdf = qt_mainform.CustomPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            #  Добавление шрифта для кириллицы
            pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
            pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
            pdf.add_font('DejaVu', 'I', 'fonts/DejaVuSansCondensed-Oblique.ttf', uni=True)
            pdf.add_font('DejaVu', 'BI', 'fonts/DejaVuSansCondensed-BoldOblique.ttf', uni=True)
            # Устанавливаем лого
            pdf.image(r'images\RKIB.jpg', 25, 10, 25)
            # Добавляем адрес
            pdf.set_font('DejaVu', 'I', 12)
            pdf.cell(130)
            pdf.cell(0, 5, 'БУЗ УР «РКИБ МЗ УР»', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'г. Ижевск, ул. Труда, 17', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'тел./факс:(3412)21-86-94', ln=1)
            pdf.ln(15)  # Разрыв линии
            #  Заголовок
            pdf.set_font('DejaVu', 'B', 14)
            s = 'Отчет по статусу за период'
            w = pdf.get_string_width(s) + 6  # Вычисляем ширину названия и позицию
            pdf.set_x((210 - w) / 2)
            pdf.cell(w, 5, s, 0, 2,
                     'C')  # В вышеприведенном коде: ширина — 60, высота — 10, текст — Powered by FPDF., граница ячейки — 0, текущая позиция после вывода ячейки — 1, выравнивание текста в ячейке — C(по центру).
            pdf.ln(2)
            pdf.set_x(70)
            pdf.cell(35, 5, 'с ' + str(date_min), 0, 0, 'C')
            pdf.cell(35, 5, ' по ' + str(date_max), 0, 2, 'C')
            pdf.ln(10)  # Разрыв строки
            #  Заполнение таблицы
            pdf.set_x(15)  # Отступ
            pdf.cell(35, 5, str("Номер"), border=1, align='C')
            pdf.cell(30, 5, str("Модель"), border=1, align='C')
            pdf.cell(45, 5, str("Статус"), border=1, align='C')
            pdf.cell(45, 5, str("Дата"), border=1, ln=1, align='C')

            for i in range(count):
                pdf.set_font('DejaVu', '', 11)
                pdf.set_x(15)  # Отступ
                pdf.cell(35, 5, str(l_number[i]), border=1, align='C')
                pdf.cell(30, 5, str(l_model[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_status[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_date[i]), border=1, ln=1, align='C')
            pdf.ln()
            pdf.cell(5)
            pdf.cell(0, 5, 'Количество: ' + str(count), ln=1)
            pdf.output(str(todey) + "-по статусу за период.pdf")
            os.startfile(str(todey) + "-по статусу за период.pdf")
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных за указанный период")
        self.MainApp_clear_filter()

    # Отчет по действию за период
    def action_report(self):
        todey = datetime.today().strftime("%Y-%m-%d")
        action_box_o = self.comboBox_action_o.currentText()
        TableAction = QtSql.QSqlTableModel()  # Временная модель таблицы Action
        TableAction.setTable('Action')
        TableAction.setFilter("Action.action = '" + action_box_o + "' ")
        TableAction.select()
        action_id = TableAction.data(TableAction.index(0, 0))

        date_Changed_min_o = self.dateEdit_min_otch.dateTime().toString('yyyy-MM-dd 00:00:00')
        date_Changed_max_o = self.dateEdit_max_otch.dateTime().toString('yyyy-MM-dd 23:59:59')
        date_min = self.dateEdit_min_otch.date().toString('dd-MM-yyyy')
        date_max = self.dateEdit_max_otch.date().toString('dd-MM-yyyy')
        #  Выборка из журнала
        self.modelTable_Select_history.setTable("History")
        self.modelTable_Select_history.setRelation(1, QSqlRelation("Cart", "id", "number"))
        self.modelTable_Select_history.setRelation(2, QSqlRelation("Model", "id", "model"))
        self.modelTable_Select_history.setRelation(3, QSqlRelation("Status", "id", "status"))
        self.modelTable_Select_history.setRelation(5, QSqlRelation("Action", "id", "action"))
        if action_box_o != '-Выбрать-':
            self.modelTable_Select_history.setFilter(
                "history.datatime >= '" + date_Changed_min_o + "' AND history.datatime <= '" + date_Changed_max_o + "' AND history.action_id = '" + str(
                    action_id) + "' ")
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Не выбрано действие")
            return 0
        self.modelTable_Select_history.setSort(0,
                                               Qt.DescendingOrder)  # Устанавливаем сортировку по возрастанию данных по 0 колонке
        self.modelTable_Select_history.select()
        count = self.modelTable_Select_history.rowCount()
        if count >= 1:
            l_number = []
            l_model = []
            l_status = []
            l_date = []
            l_action = []
            for elem in range(count):
                number = self.modelTable_Select_history.record(elem).value(1)
                status = self.modelTable_Select_history.record(elem).value(3)
                date = self.modelTable_Select_history.record(elem).value(4)
                action = self.modelTable_Select_history.record(elem).value(5)
                l_number.append(number)
                l_status.append(status)
                l_date.append(date)
                l_action.append(action)
                self.modelTable_Select_cart.setTable("Cart")
                self.modelTable_Select_cart.setFilter("cart.number= '" + str(number) + "' ")
                self.modelTable_Select_cart.select()
                model = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 2))
                l_model.append(model)

            pdf = qt_mainform.CustomPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            #  Добавление шрифта для кириллицы
            pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
            pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
            pdf.add_font('DejaVu', 'I', 'fonts/DejaVuSansCondensed-Oblique.ttf', uni=True)
            pdf.add_font('DejaVu', 'BI', 'fonts/DejaVuSansCondensed-BoldOblique.ttf', uni=True)
            # Устанавливаем лого
            pdf.image(r'images\RKIB.jpg', 25, 10, 25)
            # Добавляем адрес
            pdf.set_font('DejaVu', 'I', 12)
            pdf.cell(130)
            pdf.cell(0, 5, 'БУЗ УР «РКИБ МЗ УР»', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'г. Ижевск, ул. Труда, 17', ln=1)
            pdf.cell(130)
            pdf.cell(0, 5, 'тел./факс:(3412)21-86-94', ln=1)
            pdf.ln(15)  # Разрыв линии
            #  Заголовок
            pdf.set_font('DejaVu', 'B', 14)
            s = 'Отчет по действию за период'
            w = pdf.get_string_width(s) + 6  # Вычисляем ширину названия и позицию
            pdf.set_x((210 - w) / 2)
            pdf.cell(w, 5, s, 0, 2,
                     'C')  # В вышеприведенном коде: ширина — 60, высота — 10, текст — Powered by FPDF., граница ячейки — 0, текущая позиция после вывода ячейки — 1, выравнивание текста в ячейке — C(по центру).
            pdf.ln(2)
            pdf.set_x(70)
            pdf.cell(35, 5, 'с ' + str(date_min), 0, 0, 'C')
            pdf.cell(35, 5, ' по ' + str(date_max), 0, 2, 'C')
            pdf.ln(10)  # Разрыв строки
            #  Заполнение таблицы
            pdf.set_x(15)  # Отступ
            pdf.cell(35, 5, str("Номер"), border=1, align='C')
            pdf.cell(30, 5, str("Модель"), border=1, align='C')
            pdf.cell(45, 5, str("Статус"), border=1, align='C')
            pdf.cell(45, 5, str("Дата"), border=1, align='C')
            pdf.cell(35, 5, str("Действие"), border=1, ln=1, align='C')
            for i in range(count):
                pdf.set_font('DejaVu', '', 11)
                pdf.set_x(15)  # Отступ
                pdf.cell(35, 5, str(l_number[i]), border=1, align='C')
                pdf.cell(30, 5, str(l_model[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_status[i]), border=1, align='C')
                pdf.cell(45, 5, str(l_date[i]), border=1, align='C')
                pdf.cell(35, 5, str(l_action[i]), border=1, ln=1, align='C')
            pdf.ln()
            pdf.cell(5)
            pdf.cell(0, 5, 'Количество: ' + str(count), ln=1)
            pdf.output(str(todey) + "-по действию за период.pdf")
            os.startfile(str(todey) + "-по действию за период.pdf")
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных за указанный период")
        self.MainApp_clear_filter()

    # Закрытие программы
    def closeEvent(self, event):  # Спросим при закрытии программы
        close = QtWidgets.QMessageBox.question(self, "Выход", "Завершить работу?", QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            qt_addform.close()
            qt_statusform.close()
            qt_modelform.close()
            self.db.close()
            event.accept()
        else:
            event.ignore()


#  Открытие формы Добавить
def AddForm_open():
    rand = random.randint(1000000000000, 9999999999999)
    qt_addform.show()
    qt_addform.lineEdit_Barcode.setText(str(rand))
    qt_addform.lineEdit_Status.setFocus()
    return rand


#  Открытие формы Статус
def StatusForm_open():
    qt_statusform.show()


#  Открытие формы Модель
def ModelForm_open():
    qt_modelform.show()


# Форма Добавления
class AddForm(addform.Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super(AddForm, self).__init__(parent)
        self.setupUi(self)
        self.comboBox_status_add.setVisible(False)
        self.comboBox_model_add.setVisible(False)
        self.checkBox.stateChanged.connect(self.Select_from_the_list)

        self.modelTable_Select_gde = QtSql.QSqlRelationalTableModel()
        self.modelTable_Select_cart = QtSql.QSqlRelationalTableModel()
        self.modelTable_Insert_cart = QtSql.QSqlRelationalTableModel()
        self.modelTable_Insert_history = QtSql.QSqlRelationalTableModel()
        self.modelTable_Model = QtSql.QSqlRelationalTableModel()
        self.modelTable_Status = QtSql.QSqlRelationalTableModel()

        self.lineEdit_Barcode.setMaxLength(13)
        self.lineEdit_Status.setMaxLength(13)
        self.lineEdit_Barcode.setValidator(QtGui.QRegExpValidator(QRegExp("^([1-9][0-9]*|0)"), self))
        self.lineEdit_Status.setValidator(QtGui.QRegExpValidator(QRegExp("^([1-9][0-9]*|0)"), self))

        self.lineEdit_Status.setPlaceholderText('Где находится...')
        self.lineEdit_Firma.setPlaceholderText('Введите фирму...')
        self.lineEdit_Model.setPlaceholderText('Введите марку...')

        self.pB_Save.clicked.connect(self.AddForm_Saves)
        self.pB_add_model.clicked.connect(ModelForm_open)
        self.pB_add_status.clicked.connect(StatusForm_open)

        # self.pB_print.clicked.connect(self.Barcode_print)

    def AddForm_Saves(self):
        BarCod = self.lineEdit_Barcode.text()
        if not BarCod:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Вы не заполнили поле Баркод!")
        else:
            if qt_mainform.checking_for_random_code_repetition(BarCod):
                re_rand = random.randint(1000000000000, 9999999999999)
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.information(self, "Warning", "Данный ID занят!")
                self.lineEdit_Barcode.setText(str(re_rand))
            elif qt_mainform.MainApp_Select_Status(BarCod):  # Проверка на наличие номера в таблице Где
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.information(self, "Warning", "Данный ID используется (Статус) !")
                self.lineEdit_Status.clear()
            else:
                qt_mainform.spisok.append(BarCod)
                if not self.checkBox.isChecked():
                    Cod_status = self.lineEdit_Status.text()
                    model = QtSql.QSqlTableModel(self)
                    model.setTable('Status')
                    model.setFilter("Status.id= '" + Cod_status + "' ")
                    model.select()
                    BarCod_status = model.data(model.index(0, 0))
                else:
                    BarCod_status = self.comboBox_status_add.currentText()
                    TableStatus = QtSql.QSqlTableModel()  # Временная модель таблицы Status
                    TableStatus.setTable('Status')
                    TableStatus.setFilter("Status.status= '" + BarCod_status + "' ")
                    TableStatus.select()
                    status_id = TableStatus.data(TableStatus.index(0, 0))
                    if BarCod_status == '-Выбрать-':
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setWindowTitle("Warning")
                        msgBox.information(self, "Warning", "Не выбрано поле Статус!")
                        return self.comboBox_status_add.setFocus()
                    else:
                        self.AddForm_Select_Gde(BarCod_status)
                if not BarCod_status:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setWindowTitle("Warning")
                    msgBox.information(self, "Warning", "Вы не заполнили поле Статус!")
                else:
                    p_insert_firma = self.lineEdit_Firma.text()
                    if not p_insert_firma:
                        msgBox = QtWidgets.QMessageBox()
                        msgBox.setWindowTitle("Warning")
                        msgBox.information(self, "Warning", "Вы не заполнили поле Фирма!")
                    else:
                        if not self.checkBox.isChecked():
                            p_insert_model = self.lineEdit_Model.text()
                            model_m = QtSql.QSqlTableModel(self)
                            model_m.setTable('Model')
                            model_m.setFilter("model.model= '" + p_insert_model + "' ")
                            model_m.select()
                            result = model_m.data(model_m.index(0, 1))
                            if not result:
                                msgBox = QtWidgets.QMessageBox()
                                msgBox.setWindowTitle("Warning")
                                msgBox.setText(f"Модель {p_insert_model} отсутствует в базе. Желаете добавить?")
                                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                                bttn = msgBox.exec_()
                                if bttn == QMessageBox.Yes:
                                    model_m = QtSql.QSqlTableModel(self)
                                    model_m.setTable('Model')
                                    model_m.select()
                                    row = model_m.rowCount()
                                    model_m.insertRow(row)
                                    model_m.setData(model_m.index(row, 1), p_insert_model)
                                    model_m.submitAll()
                                    msgBox = QtWidgets.QMessageBox()
                                    msgBox.setWindowTitle("Warning")
                                    msgBox.information(self, "Warning", f"Модель {p_insert_model} успешно добавлена!")
                                    qt_mainform.MainApp_combo_model()
                                    return self.lineEdit_Model.setFocus()
                                elif bttn == QMessageBox.No:
                                    msgBox.close()
                                    return self.comboBox_model_add.setFocus()
                        else:
                            p_insert_model = self.comboBox_model_add.currentText()
                            TableModel = QtSql.QSqlTableModel()  # Временная модель таблицы Status
                            TableModel.setTable('Model')
                            TableModel.setFilter("Model.model= '" + p_insert_model + "' ")
                            TableModel.select()
                            model_id = TableModel.data(TableModel.index(0, 0))
                            if p_insert_model == '-Выбрать-':
                                msgBox = QtWidgets.QMessageBox()
                                msgBox.setWindowTitle("Warning")
                                msgBox.information(self, "Warning", "Не выбрано поле модель")
                                return self.comboBox_model_add.setFocus()
                        if not p_insert_model:
                            msgBox = QtWidgets.QMessageBox()
                            msgBox.setWindowTitle("Warning")
                            msgBox.information(self, "Warning", "Вы не заполнили поле модель.")
                        else:
                            self.AddForm_Insert_to_DB(BarCod, status_id, p_insert_firma, model_id)
                            self.AddForm_Insert_History(BarCod)
                            self.lineEdit_Status.clear()
                            self.lineEdit_Firma.clear()
                            self.lineEdit_Model.clear()
                            index = 0
                            self.comboBox_model_add.setCurrentIndex(index)
                            self.comboBox_status_add.setCurrentIndex(index)
                            qt_mainform.MainApp_spisok_cart()
                            qt_mainform.MainApp_spisok_history()
                            return AddForm_open()

    # Выбор из списка
    def Select_from_the_list(self):
        if self.checkBox.isChecked():  # Ручной ввод
            self.lineEdit_Status.setVisible(False)
            self.lineEdit_Model.setVisible(False)
            self.comboBox_status_add.setVisible(True)
            self.comboBox_model_add.setVisible(True)
            self.modelTable_Status.setTable('Status')
            self.modelTable_Status.setFilter("status!= '' ")
            column = self.modelTable_Status.fieldIndex('status')
            self.modelTable_Status.select()
            self.comboBox_status_add.setModel(self.modelTable_Status)
            self.comboBox_status_add.setModelColumn(column)

            self.modelTable_Model.setTable('Model')
            self.modelTable_Model.setFilter("model!='' ")
            column = self.modelTable_Model.fieldIndex('model')
            self.modelTable_Model.select()
            self.comboBox_model_add.setModel(self.modelTable_Model)
            self.comboBox_model_add.setModelColumn(column)

        else:
            self.lineEdit_Status.setVisible(True)
            self.lineEdit_Model.setVisible(True)
            self.comboBox_status_add.setVisible(False)
            self.comboBox_model_add.setVisible(False)

    def AddForm_Select_Gde(self, BarCod_status):
        global result_Select_Gde
        self.modelTable_Select_gde.setTable("Status")
        self.modelTable_Select_gde.setFilter("Status.status= '" + BarCod_status + "' ")
        self.modelTable_Select_gde.select()
        result_Select_Gde = self.modelTable_Select_gde.data(self.modelTable_Select_gde.index(0, 0))
        return result_Select_Gde

    # Добавление в базу Картриджи
    def AddForm_Insert_to_DB(self, BarCod, status_id, p_insert_firma, model_id):
        todey = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.modelTable_Insert_cart.setTable("Cart")
        row = self.modelTable_Insert_cart.rowCount()
        self.modelTable_Insert_cart.insertRow(row)
        self.modelTable_Insert_cart.setData(self.modelTable_Insert_cart.index(row, 1), BarCod)
        self.modelTable_Insert_cart.setData(self.modelTable_Insert_cart.index(row, 2), p_insert_firma)
        self.modelTable_Insert_cart.setData(self.modelTable_Insert_cart.index(row, 3), model_id)
        self.modelTable_Insert_cart.setData(self.modelTable_Insert_cart.index(row, 4), status_id)
        self.modelTable_Insert_cart.setData(self.modelTable_Insert_cart.index(row, 5), str(todey))
        self.modelTable_Insert_cart.submitAll()

    def AddForm_Select_History(self, BarCod):
        global result_Select_Model, result_Select_Status
        self.modelTable_Select_cart.setTable("Cart")
        self.modelTable_Select_cart.setFilter("cart.id= '" + str(BarCod) + "' ")
        self.modelTable_Select_cart.select()
        result_Select_Model = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 3))
        result_Select_Status = self.modelTable_Select_cart.data(self.modelTable_Select_cart.index(0, 4))

    # Добавление в базу Журнал
    def AddForm_Insert_History(self, BarCod):
        todey = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        TableCart = QtSql.QSqlTableModel()  # Временная модель таблицы Status
        TableCart.setTable('Cart')
        TableCart.setFilter("Cart.number = '" + BarCod + "' ")
        TableCart.select()
        cart_id = TableCart.data(TableCart.index(0, 0))
        TableAction = QtSql.QSqlTableModel()  # Временная модель таблицы Action
        TableAction.setTable('tb_Action')
        TableAction.setFilter("tb_Action.action = 'Добавление' ")
        TableAction.select()
        action_id = TableAction.data(TableAction.index(0, 0))
        self.modelTable_Insert_history.setTable("History")
        self.AddForm_Select_History(cart_id)
        row = self.modelTable_Insert_history.rowCount()
        self.modelTable_Insert_history.insertRow(row)
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 1), cart_id)
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 2), result_Select_Model)
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 3), result_Select_Status)
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 4), str(todey))
        self.modelTable_Insert_history.setData(self.modelTable_Insert_history.index(row, 5), action_id)
        self.modelTable_Insert_history.submitAll()

    # Закрытие формы
    def closeEvent(self, event):  # Спросим при закрытии программы
        self.lineEdit_Barcode.clear()
        self.lineEdit_Status.clear()
        self.lineEdit_Firma.clear()
        self.lineEdit_Model.clear()
        self.comboBox_status_add.clear()
        self.comboBox_model_add.clear()
        self.checkBox.setChecked(False)
        qt_addform.close()
        event.accept()


class StatusForm(statusform.Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super(StatusForm, self).__init__(parent)
        self.setupUi(self)
        self.modelTable_Status = QtSql.QSqlRelationalTableModel()
        self.lineEdit_StatusForm.setFocus()
        self.lineEdit_StatusForm.textChanged[str].connect(self.StatusForm_filter)
        self.StatusForm_spisok()
        self.pB_add_StatusForm.clicked.connect(self.StatusForm_add)
        self.pB_delete_StatusForm.clicked.connect(self.StatusForm_delete)
        self.pB_edit_StatusForm.clicked.connect(self.StatusForm_edit)
        self.pB_print_StatusForm.clicked.connect(self.StatusForm_print_Added)

    # Фильтр по введенным символам
    def StatusForm_filter(self):
        StatusForm_symbol = self.lineEdit_StatusForm.text()
        if StatusForm_symbol == '':
            self.StatusForm_spisok()
        else:
            self.modelTable_Status.setTable("Status")
            self.modelTable_Status.setHeaderData(0, QtCore.Qt.Horizontal, "Номер")
            self.modelTable_Status.setHeaderData(1, QtCore.Qt.Horizontal, "Статус")
            self.modelTable_Status.setFilter("status.status LIKE '" + StatusForm_symbol.capitalize() + "%' ")
            self.modelTable_Status.select()
            self.tableView_StatusForm.setModel(self.modelTable_Status)
            self.tableView_StatusForm.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет редактирования
            self.tableView_StatusForm.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)  # таблица по размеру содержимого
            self.tableView_StatusForm.setStyleSheet("QHeaderView::section {background-color:gray}")
            self.tableView_StatusForm.setAlternatingRowColors(True)  # цвет четных и нечетных строк
            self.tableView_StatusForm.setSortingEnabled(True)
            self.tableView_StatusForm.setSelectionMode(
                self.tableView_StatusForm.ExtendedSelection)  # режим выделения лишь одной ячейки в таблице

    # Список формы Статус
    def StatusForm_spisok(self):
        self.modelTable_Status.setTable("Status")
        self.modelTable_Status.setHeaderData(0, QtCore.Qt.Horizontal, "Номер")
        self.modelTable_Status.setHeaderData(1, QtCore.Qt.Horizontal, "Статус")
        self.modelTable_Status.setFilter("status.id > 0")
        self.modelTable_Status.select()
        self.tableView_StatusForm.setModel(self.modelTable_Status)
        self.tableView_StatusForm.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет редактирования
        self.tableView_StatusForm.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # таблица по размеру содержимого
        self.tableView_StatusForm.setStyleSheet("QHeaderView::section {background-color:gray}")
        self.tableView_StatusForm.setAlternatingRowColors(True)  # цвет четных и нечетных строк
        self.tableView_StatusForm.setSortingEnabled(True)
        # self.tableView_StatusForm.setSelectionMode(self.tableView_StatusForm.ExtendedSelection)  # режим выделения лишь одной ячейки в таблице
        self.tableView_StatusForm.setSelectionBehavior(QAbstractItemView.SelectRows)  # Разрешаем выделение строк

    # Добавление отдела
    def StatusForm_add(self):
        Status_str = self.lineEdit_StatusForm.text()
        if not Status_str:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Не введено значение в поле")
        else:
            BarCod = random.randint(1000000000000, 9999999999999)
            if qt_mainform.checking_for_random_code_repetition(str(BarCod)):
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.information(self, "Warning", "Данный ID занят!")
                return 0
            elif qt_mainform.MainApp_Select_Status(str(BarCod)):  # Проверка на наличие номера в таблице Где
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.information(self, "Warning", "Данный ID используется (Статус) !")
                return 0
            else:
                self.modelTable_Status.setTable("Status")
                row = self.modelTable_Status.rowCount()
                self.modelTable_Status.insertRow(row)
                self.modelTable_Status.setData(self.modelTable_Status.index(row, 0), BarCod)
                self.modelTable_Status.setData(self.modelTable_Status.index(row, 1), Status_str.capitalize())
                self.modelTable_Status.submitAll()
                self.lineEdit_StatusForm.clear()
                self.StatusForm_spisok()
                qt_mainform.MainApp_spisok_cart()

    # Удаление отдела
    def StatusForm_delete(self):
        msgBox = QtWidgets.QMessageBox.warning(self, "Warning", "Желаете удалить выбранную строку?",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if msgBox == QtWidgets.QMessageBox.Yes:
            index_row = self.tableView_StatusForm.currentIndex().row()
            datas_id = self.modelTable_Status.data(self.modelTable_Status.index(index_row, 0))
            modelTable = QtSql.QSqlTableModel()
            modelTable.setTable("Cart")
            modelTable.setFilter("Cart.id = '" + str(datas_id) + "' ")
            modelTable.select()
            result_Select_Cart = modelTable.data(modelTable.index(0, 4))
            if not result_Select_Cart:
                self.modelTable_Status.removeRow(self.tableView_StatusForm.currentIndex().row())
                self.tableView_StatusForm.update()
                self.StatusForm_spisok()
                self.lineEdit_StatusForm.setFocus()
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.information(self, "Warning", "Данный отдел имеет связь с другой таблицей")
        elif msgBox == QMessageBox.No:
            self.lineEdit_StatusForm.setFocus()

    # Редактирование отдела
    def StatusForm_edit(self):
        if self.pB_edit_StatusForm.isChecked():
            self.tableView_StatusForm.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.modelTable_Status.setEditStrategy(QtSql.QSqlRelationalTableModel.OnFieldChange)
        else:
            self.tableView_StatusForm.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # Печать штрихкода отделов
    def StatusForm_print_Added(self):
        count = self.modelTable_Status.rowCount()
        if count >= 1:
            path = Path(r".\temp_png")
            path.mkdir(exist_ok=True)
            l_number = list()
            l_name = list()
            l_item_name = list()
            item_name = 1
            for elem in range(count):
                number = self.modelTable_Status.record(elem).value(0)
                name = self.modelTable_Status.record(elem).value(1)
                l_number.append(number)
                l_name.append(name)
                barcode_writer = ImageWriter()
                barCodeImage = barcode.codex.Code39(str(l_number[elem]), writer=ImageWriter(), add_checksum=False)
                file_name = barCodeImage.save(path / str(item_name),
                                              {"quiet_zone": 5, "text_distance": 2, "module_height": 10})
                l_item_name.append(file_name)
                item_name += 1
            df = pd.DataFrame(l_item_name)
            writer = pd.ExcelWriter("./test.xlsx", engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', header=False, index=False, merge_cells=True, startcol=-1)
            worksheet = writer.sheets['Sheet1']
            # Вставьте изображение с масштабированием.
            y_offset = 0  # положение штрихкода
            x_offset = 0
            y_offset_2 = 55  # положение текста
            col = "A1"
            for i in range(0, count, 1):
                if i == 8:  # первый столбец первая страница
                    y_offset = 0
                    y_offset_2 = 55
                    x_offset = 200
                elif i == 16:  # второй столбец первая страница
                    y_offset = 0
                    y_offset_2 = 55
                    x_offset = 400
                elif i == 24:  # третий столбец первая страница
                    y_offset = 1000
                    y_offset_2 = 1055
                    x_offset = 0

                elif i == 32:  # первый столбец вторая страница
                    y_offset = 1000
                    y_offset_2 = 1055
                    x_offset = 200
                elif i == 40:  # второй столбец вторая страница
                    y_offset = 1000
                    y_offset_2 = 1055
                    x_offset = 400
                elif i == 48:  # третий столбец вторая страница
                    y_offset = 2000
                    y_offset_2 = 2055
                    x_offset = 0

                worksheet.insert_image(col, l_item_name[i],
                                       {'x_offset': x_offset, 'y_offset': y_offset, 'x_scale': 0.25, 'y_scale': 0.3})
                y_offset += 120
                worksheet.insert_textbox(col, l_name[i],
                                         {'x_offset': x_offset, 'y_offset': y_offset_2, 'x_scale': 0.89, 'y_scale': 0.2,
                                          'font': {'color': 'black', 'bold': True, 'size': 10},
                                          'align': {'vertical': 'middle', 'horizontal': 'center'},
                                          'line': {'none': True}, })
                y_offset_2 += 120
                i += 1
            writer.save()
            os.startfile(r'.\test.xlsx')
            shutil.rmtree(path)  # Удаляет текущую директорию и все поддиректории
        if count == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Нет данных по указанным параметрам")
            return msgBox

    # Закрытие формы
    def closeEvent(self, event):  # Спросим при закрытии программы
        self.lineEdit_StatusForm.clear()
        qt_statusform.close()
        event.accept()


class ModelForm(modelform.Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super(ModelForm, self).__init__(parent)
        self.setupUi(self)
        self.modelTable_Model = QtSql.QSqlRelationalTableModel()
        self.lineEdit_ModelForm.setFocus()
        self.lineEdit_ModelForm.textChanged[str].connect(self.ModelForm_filter)
        self.ModelForm_spisok()
        self.pB_add_ModelForm.clicked.connect(self.ModelForm_add)
        self.pB_delete_ModelForm.clicked.connect(self.ModelForm_delete)
        self.pB_edit_ModelForm.clicked.connect(self.ModelForm_edit)

    # Фильтр по введенным символам
    def ModelForm_filter(self):
        Model_symbol = self.lineEdit_ModelForm.text()
        if Model_symbol == '':
            self.ModelForm_spisok()
        else:
            self.modelTable_Model.setTable("Model")
            self.modelTable_Model.setHeaderData(0, QtCore.Qt.Horizontal, "Номер")
            self.modelTable_Model.setHeaderData(1, QtCore.Qt.Horizontal, "Модель")
            self.modelTable_Model.setFilter("Model.model LIKE '" + Model_symbol + "%' ")
            self.modelTable_Model.select()
            self.tableView_ModelForm.setModel(self.modelTable_Model)
            self.tableView_ModelForm.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет редактирования
            self.tableView_ModelForm.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)  # таблица по размеру содержимого
            self.tableView_ModelForm.setStyleSheet("QHeaderView::section {background-color:gray}")
            self.tableView_ModelForm.setAlternatingRowColors(True)  # цвет четных и нечетных строк
            self.tableView_ModelForm.setSortingEnabled(True)
            self.tableView_ModelForm.setSelectionMode(
                self.tableView_ModelForm.ExtendedSelection)  # режим выделения лишь одной ячейки в таблице

    # Список формы Модель
    def ModelForm_spisok(self):
        self.modelTable_Model.setTable("Model")
        self.modelTable_Model.setHeaderData(0, QtCore.Qt.Horizontal, "Номер")
        self.modelTable_Model.setHeaderData(1, QtCore.Qt.Horizontal, "Модель")
        self.modelTable_Model.setFilter("model.id > 0")
        self.modelTable_Model.select()
        self.tableView_ModelForm.setModel(self.modelTable_Model)
        self.tableView_ModelForm.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет редактирования
        self.tableView_ModelForm.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # таблица по размеру содержимого
        self.tableView_ModelForm.setStyleSheet("QHeaderView::section {background-color:gray}")
        self.tableView_ModelForm.setAlternatingRowColors(True)  # цвет четных и нечетных строк
        self.tableView_ModelForm.setSortingEnabled(True)
        # self.tableView_ModelForm.setSelectionMode(QAbstractItemView.MultiSelection)  # режим выделения нескольких полей в  таблице
        self.tableView_ModelForm.setSelectionBehavior(QAbstractItemView.SelectRows)  # Разрешаем выделение строк

    # Добавление модели
    def ModelForm_add(self):
        Model_str = self.lineEdit_ModelForm.text()
        if not Model_str:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.information(self, "Warning", "Не введено значение в поле")
        else:
            self.modelTable_Model.setTable("Model")
            row = self.modelTable_Model.rowCount()
            self.modelTable_Model.insertRow(row)
            self.modelTable_Model.setData(self.modelTable_Model.index(row, 1), Model_str)
            self.modelTable_Model.submitAll()
            self.lineEdit_ModelForm.clear()
            self.ModelForm_spisok()

    # Удаление модели
    def ModelForm_delete(self):
        msgBox = QtWidgets.QMessageBox.warning(self, "Warning", "Желаете удалить выбранную строку?",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if msgBox == QtWidgets.QMessageBox.Yes:
            index_row = self.tableView_ModelForm.currentIndex().row()
            datas_id = self.modelTable_Model.data(self.modelTable_Model.index(index_row, 0))
            modelTable = QtSql.QSqlTableModel()
            modelTable.setTable("Cart")
            modelTable.setFilter("Cart.id = '" + str(datas_id) + "' ")
            modelTable.select()
            result_Select_Cart = modelTable.data(modelTable.index(0, 3))
            if not result_Select_Cart:
                self.modelTable_Model.removeRow(self.tableView_ModelForm.currentIndex().row())
                self.tableView_ModelForm.update()
                self.ModelForm_spisok()
                self.lineEdit_ModelForm.setFocus()
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.information(self, "Warning", "Данная модель имеет связь с другой таблицей")
        elif msgBox == QMessageBox.No:
            self.lineEdit_ModelForm.setFocus()

    # Редактирование модели
    def ModelForm_edit(self):
        if self.pB_edit_ModelForm.isChecked():
            self.tableView_ModelForm.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.modelTable_Model.setEditStrategy(QtSql.QSqlRelationalTableModel.OnFieldChange)
        else:
            self.tableView_ModelForm.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # Закрытие формы
    def closeEvent(self, event):  # Спросим при закрытии программы
        self.lineEdit_ModelForm.clear()
        qt_modelform.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication()
    qt_mainform = MainApp()
    qt_addform = AddForm()
    qt_statusform = StatusForm()
    qt_modelform = ModelForm()
    qt_mainform.show()
    app.setStyle(u"fusion")
    app.exec_()
