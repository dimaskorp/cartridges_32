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
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(260, 200)
        Dialog.setMinimumSize(QSize(260, 200))
        Dialog.setMaximumSize(QSize(260, 200))
        font = QFont()
        font.setFamily(u"Times New Roman")
        Dialog.setFont(font)
        Dialog.setFocusPolicy(Qt.NoFocus)
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        Dialog.setAcceptDrops(False)
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)

        self.lineEdit_Firma = QLineEdit(Dialog)
        self.lineEdit_Firma.setObjectName(u"lineEdit_Firma")
        self.lineEdit_Firma.setGeometry(QRect(70, 100, 135, 20))
        self.lineEdit_Firma.raise_()
        self.lineEdit_Model = QLineEdit(Dialog)
        self.lineEdit_Model.setObjectName(u"lineEdit_Model")
        self.lineEdit_Model.setGeometry(QRect(70, 130, 135, 20))
        self.lineEdit_Model.raise_()
        self.lineEdit_Barcode = QLineEdit(Dialog)
        self.lineEdit_Barcode.setObjectName(u"lineEdit_Barcode")
        self.lineEdit_Barcode.setGeometry(QRect(70, 40, 135, 20))
        self.lineEdit_Barcode.raise_()
        self.lineEdit_Status = QLineEdit(Dialog)
        self.lineEdit_Status.setObjectName(u"lineEdit_Status")
        self.lineEdit_Status.setGeometry(QRect(70, 70, 135, 20))
        self.lineEdit_Status.raise_()

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 40, 16))
        self.label.raise_()
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(24, 101, 41, 16))
        self.label_2.raise_()
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(18, 133, 47, 13))
        self.label_3.raise_()
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 70, 41, 21))
        self.label_4.raise_()

        self.pB_Save = QPushButton(Dialog)
        self.pB_Save.setObjectName(u"pB_Save")
        self.pB_Save.setEnabled(True)
        self.pB_Save.setGeometry(QRect(100, 160, 75, 23))
        self.pB_Save.setTabletTracking(False)
        self.pB_Save.setCheckable(False)
        self.pB_Save.setChecked(False)
        self.pB_Save.raise_()

        self.comboBox_status_add = QComboBox(Dialog)
        self.comboBox_status_add.setObjectName(u"comboBox_status_add")
        self.comboBox_status_add.setGeometry(QRect(70, 70, 135, 20))
        self.comboBox_status_add.setEditable(False)
        self.comboBox_status_add.raise_()
        self.comboBox_model_add = QComboBox(Dialog)
        self.comboBox_model_add.setObjectName(u"comboBox_model_add")
        self.comboBox_model_add.setGeometry(QRect(70, 130, 135, 20))
        self.comboBox_model_add.setEditable(False)
        self.comboBox_model_add.raise_()

        self.checkBox = QCheckBox(Dialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QRect(140, 0, 111, 20))
        self.checkBox.setLayoutDirection(Qt.RightToLeft)
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)
        self.checkBox.raise_()

        self.pB_add_status = QPushButton(Dialog)
        self.pB_add_status.setObjectName(u"pB_add_status")
        self.pB_add_status.setGeometry(QRect(210, 70, 31, 21))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_add_status.sizePolicy().hasHeightForWidth())
        self.pB_add_status.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_status.setIcon(icon)
        self.pB_add_status.raise_()
        self.pB_add_model = QPushButton(Dialog)
        self.pB_add_model.setObjectName(u"pB_add_model")
        self.pB_add_model.setGeometry(QRect(210, 130, 31, 21))
        sizePolicy.setHeightForWidth(self.pB_add_model.sizePolicy().hasHeightForWidth())
        self.pB_add_model.setSizePolicy(sizePolicy)
        self.pB_add_model.setIcon(icon)
        self.pB_add_model.raise_()

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
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Добавление картриджа", None))
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))
        self.label.setText(QCoreApplication.translate("Dialog", u"Баркод:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Фирма:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Модель:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Статус:", None))
        self.pB_Save.setText(QCoreApplication.translate("Dialog", u"Сохранить", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"Выбор из списка", None))
        self.pB_add_status.setText("")
        self.pB_add_model.setText("")
    # retranslateUi

