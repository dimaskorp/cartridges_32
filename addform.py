# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addform.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        #Dialog.resize(260, 200)
        Dialog.setMinimumSize(QSize(400, 300))
        Dialog.setMaximumSize(QSize(400, 300))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        Dialog.setFont(font)

        self.lineEdit_Firma = QLineEdit(Dialog)
        self.lineEdit_Firma.setObjectName("lineEdit_Firma")
        self.lineEdit_Firma.setGeometry(QRect(140, 120, 150, 25))

        self.lineEdit_Model = QLineEdit(Dialog)
        self.lineEdit_Model.setObjectName("lineEdit_Model")
        self.lineEdit_Model.setGeometry(QRect(140, 160, 150, 25))

        self.lineEdit_Barcode = QLineEdit(Dialog)
        self.lineEdit_Barcode.setObjectName("lineEdit_Barcode")
        self.lineEdit_Barcode.setGeometry(QRect(140, 40, 150, 25))

        self.lineEdit_Status = QLineEdit(Dialog)
        self.lineEdit_Status.setObjectName("lineEdit_Status")
        self.lineEdit_Status.setGeometry(QRect(140, 80, 150, 25))

        self.label = QLabel(Dialog)
        self.label.setObjectName("label_Barcode")
        self.label.setGeometry(QRect(20, 40, 60, 16))

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName("label_Firma")
        self.label_2.setGeometry(QRect(20, 120, 60, 16))

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName("label_Model")
        self.label_3.setGeometry(QRect(20, 160, 60, 13))

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName("label_Status")
        self.label_4.setGeometry(QRect(20, 80, 60, 21))

        self.pB_Save = QPushButton(Dialog)
        self.pB_Save.setObjectName("pB_Save")
        self.pB_Save.setEnabled(True)
        self.pB_Save.setGeometry(QRect(160, 200, 80, 25))

        self.comboBox_status_add = QComboBox(Dialog)
        self.comboBox_status_add.setObjectName("comboBox_status_add")
        self.comboBox_status_add.setGeometry(QRect(140, 80, 150, 25))
        self.comboBox_status_add.setEditable(False)

        self.comboBox_model_add = QComboBox(Dialog)
        self.comboBox_model_add.setObjectName("comboBox_model_add")
        self.comboBox_model_add.setGeometry(QRect(140, 160, 150, 25))
        self.comboBox_model_add.setEditable(False)
        self.comboBox_model_add.raise_()

        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QRect(140, 10, 150, 25))
        self.checkBox.setLayoutDirection(Qt.RightToLeft)
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)

        self.pB_add_status = QPushButton(Dialog)
        self.pB_add_status.setObjectName("pB_add_status")
        self.pB_add_status.setGeometry(QRect(300, 80, 40, 25))
        icon = QIcon()
        icon.addFile("images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_status.setIcon(icon)

        self.pB_add_model = QPushButton(Dialog)
        self.pB_add_model.setObjectName("pB_add_model")
        self.pB_add_model.setGeometry(QRect(300, 160, 40, 25))
        self.pB_add_model.setIcon(icon)

        QWidget.setTabOrder(self.lineEdit_Barcode, self.lineEdit_Status)
        QWidget.setTabOrder(self.lineEdit_Status, self.lineEdit_Firma)
        QWidget.setTabOrder(self.lineEdit_Firma, self.lineEdit_Model)
        QWidget.setTabOrder(self.lineEdit_Model, self.pB_Save)
        QWidget.setTabOrder(self.pB_Save, self.comboBox_status_add)
        QWidget.setTabOrder(self.comboBox_status_add, self.checkBox)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Добавление картриджа")
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))
        self.label.setText("Баркод:")
        self.label_2.setText("Фирма:")
        self.label_3.setText("Модель:")
        self.label_4.setText("Статус:")
        self.pB_Save.setText("Сохранить")
        self.checkBox.setText("Выбор из списка")

    # retranslateUi

