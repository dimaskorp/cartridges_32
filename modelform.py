from PySide2.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide2.QtGui import (QIcon)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(260, 200)
        Dialog.setMinimumSize(QSize(260, 200))
        Dialog.setMaximumSize(QSize(260, 205))
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(10, 10, 241, 181))
        self.splitter.setOrientation(Qt.Vertical)

        self.lineEdit_ModelForm = QLineEdit(self.splitter)
        self.lineEdit_ModelForm.setObjectName(u"lineEdit_ModelForm")
        self.splitter.addWidget(self.lineEdit_ModelForm)

        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.splitter.addWidget(self.widget)

        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pB_add_ModelForm = QPushButton(self.widget)
        self.pB_add_ModelForm.setObjectName(u"pB_add_ModelForm")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_add_ModelForm.sizePolicy().hasHeightForWidth())
        self.pB_add_ModelForm.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"images/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_add_ModelForm.setIcon(icon)
        self.horizontalLayout.addWidget(self.pB_add_ModelForm)

        self.pB_edit_ModelForm = QPushButton(self.widget)
        self.pB_edit_ModelForm.setObjectName(u"pB_edit_ModelForm")
        self.pB_edit_ModelForm.setMouseTracking(False)
        self.pB_edit_ModelForm.setTabletTracking(False)
        self.pB_edit_ModelForm.setFocusPolicy(Qt.StrongFocus)
        self.pB_edit_ModelForm.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u"images/edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_edit_ModelForm.setIcon(icon1)
        self.pB_edit_ModelForm.setCheckable(True)
        self.pB_edit_ModelForm.setChecked(False)
        self.pB_edit_ModelForm.setAutoRepeat(False)
        self.pB_edit_ModelForm.setAutoExclusive(False)
        self.horizontalLayout.addWidget(self.pB_edit_ModelForm)

        self.pB_delete_ModelForm = QPushButton(self.widget)
        self.pB_delete_ModelForm.setObjectName(u"pB_delete_ModelForm")
        icon2 = QIcon()
        icon2.addFile(u"images/delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pB_delete_ModelForm.setIcon(icon2)
        self.horizontalLayout.addWidget(self.pB_delete_ModelForm)

        self.tableView_ModelForm = QTableView(self.splitter)
        self.tableView_ModelForm.setObjectName(u"tableView_ModelForm")
        self.splitter.addWidget(self.tableView_ModelForm)
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Модели", None))
        Dialog.setWindowIcon(QIcon('images/iconc.jpg'))
        self.pB_add_ModelForm.setText("")
        self.pB_edit_ModelForm.setText("")
        self.pB_delete_ModelForm.setText("")
    # retranslateUi

