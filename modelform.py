from PySide2.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide2.QtGui import (QIcon, QFont)
from PySide2.QtWidgets import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        #Dialog.resize(600, 500)
        Dialog.setMinimumSize(QSize(600, 500))
        Dialog.setMaximumSize(QSize(600, 500))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)

        self.toolBox_m = QToolBox(Dialog)
        self.toolBox_m.setObjectName("toolBox_m")
        self.toolBox_m.setGeometry(10, 10, 600, 500)
        self.toolBox_m.setFont(font)
        self.toolBox_m.setLayoutDirection(Qt.LeftToRight)

        self.lineEdit_ModelForm = QLineEdit(self.toolBox_m)
        self.lineEdit_ModelForm.setObjectName("lineEdit_ModelForm")
        self.lineEdit_ModelForm.setGeometry(QRect(10, 0, 300, 25))
        self.lineEdit_ModelForm.setFrame(True)
        self.lineEdit_ModelForm.setEchoMode(QLineEdit.Normal)
        self.lineEdit_ModelForm.setClearButtonEnabled(True)

        self.pB_add_ModelForm = QPushButton(self.toolBox_m)
        self.pB_add_ModelForm.setObjectName("pB_add_ModelForm")
        self.pB_add_ModelForm.setGeometry(QRect(10, 40, 100, 25))
        icon = QIcon()
        icon.addFile("images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_ModelForm.setIcon(icon)

        self.pB_edit_ModelForm = QPushButton(self.toolBox_m)
        self.pB_edit_ModelForm.setObjectName("pB_edit_ModelForm")
        self.pB_edit_ModelForm.setGeometry(QRect(110, 40, 100, 25))
        self.pB_edit_ModelForm.setCheckable(True)
        icon1 = QIcon()
        icon1.addFile("images/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_edit_ModelForm.setIcon(icon1)

        self.pB_delete_ModelForm = QPushButton(self.toolBox_m)
        self.pB_delete_ModelForm.setObjectName("pB_delete_ModelForm")
        self.pB_delete_ModelForm.setGeometry(QRect(210, 40, 100, 25))
        icon2 = QIcon()
        icon2.addFile("images/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_delete_ModelForm.setIcon(icon2)

        self.tableView_ModelForm = QTableView(self.toolBox_m)
        self.tableView_ModelForm.setObjectName("tableView_ModelForm")
        self.tableView_ModelForm.setGeometry(QRect(0, 90, 580, 380))
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Модели")
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))

    # retranslateUi

