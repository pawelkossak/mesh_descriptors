# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceKRFdJO.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLayout, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1122, 851)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setCursor(QCursor(Qt.ArrowCursor))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(9)
        self.gridLayout.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.medicalText = QLineEdit(self.centralwidget)
        self.medicalText.setObjectName(u"medicalText")

        self.horizontalLayout_2.addWidget(self.medicalText)

        self.searchButton = QPushButton(self.centralwidget)
        self.searchButton.setObjectName(u"searchButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveButton = QPushButton(self.centralwidget)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.chartButton = QPushButton(self.centralwidget)
        self.chartButton.setObjectName(u"chartButton")

        self.horizontalLayout.addWidget(self.chartButton)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.resultTable = QTableWidget(self.centralwidget)
        if (self.resultTable.columnCount() < 2):
            self.resultTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.resultTable.setObjectName(u"resultTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resultTable.sizePolicy().hasHeightForWidth())
        self.resultTable.setSizePolicy(sizePolicy1)
        self.resultTable.setMinimumSize(QSize(0, 0))
        self.resultTable.setLayoutDirection(Qt.LeftToRight)
        self.resultTable.setAutoFillBackground(False)
        self.resultTable.setFrameShadow(QFrame.Plain)
        self.resultTable.setLineWidth(1)
        self.resultTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.resultTable.setTextElideMode(Qt.ElideLeft)
        self.resultTable.setShowGrid(True)
        self.resultTable.setGridStyle(Qt.NoPen)
        self.resultTable.setWordWrap(True)
        self.resultTable.setColumnCount(2)
        self.resultTable.horizontalHeader().setVisible(True)
        self.resultTable.horizontalHeader().setCascadingSectionResizes(True)
        self.resultTable.horizontalHeader().setMinimumSectionSize(33)
        self.resultTable.horizontalHeader().setDefaultSectionSize(300)
        self.resultTable.verticalHeader().setVisible(True)
        self.resultTable.verticalHeader().setMinimumSectionSize(20)
        self.resultTable.verticalHeader().setDefaultSectionSize(30)

        self.gridLayout.addWidget(self.resultTable, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1122, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.medicalText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Write medical text here...", None))
        self.searchButton.setText(QCoreApplication.translate("MainWindow", u"Search for descriptors", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save results to text file", None))
        self.chartButton.setText(QCoreApplication.translate("MainWindow", u"Generate chart", None))
        ___qtablewidgetitem = self.resultTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Descriptor", None));
        ___qtablewidgetitem1 = self.resultTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Number of occurrences\n"
"", None));
    # retranslateUi

