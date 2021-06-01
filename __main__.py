#!/usr/bin/env python
import time
import sys
import os
import subprocess
from urllib.parse import unquote

from PySide2.QtCore import Qt, QAbstractTableModel, QRect, QSize, QPoint, QSettings
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QKeySequence
from PySide2.QtWidgets import (QApplication, QMenu, QMainWindow, QMessageBox, QHeaderView, QSplitter, QTableView, QGroupBox, QFrame, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QShortcut)

from src import search
from src import sidebar

__version__ = "0.1.1"

ABOUT_MSG = "<p><b>Tracker Search</b></p>" \
    "<p>Author: Arjan Wooning</p>" \
    "<p>Website: <a href='https://arjan.wooning.cz/linux-search-tracker-full-text-search-tool-gnome-desktop/'>arjan.wooning.cz</a></p>" \
    "<p>Version: %s</p>" \
    "<p>Released under the <a href='https://www.gnu.org/licenses/gpl-3.0.html'>GPL-3.0 License</a></p>"  % __version__


class MainWindow(QMainWindow):
    global ABOUT_MSG

    def __init__(self):
        super(MainWindow, self).__init__()

        fileMenu = QMenu("&File", self)
        # openAction = fileMenu.addAction("&Open...")
        # openAction.setShortcut("Ctrl+O")
        # saveAction = fileMenu.addAction("&Save As...")
        # saveAction.setShortcut("Ctrl+S")
        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")
        helpMenu = QMenu("&Help", self)
        aboutAction = helpMenu.addAction("&About")

        mainpath = os.path.dirname(os.path.abspath(__file__))
        iconpath = os.path.join(mainpath, "icons/tracker_search.png")
        appIcon = QIcon(iconpath)
        self.setWindowIcon(appIcon)

        self.settings = QSettings("tracker_search", "settings")

        # Initial window size/pos last saved. Use default values for first time
        self.resize(self.settings.value("size", QSize(800, 600)))
        self.move(self.settings.value("pos", QPoint(50, 50)))

        self.setupModel()

        # Setup the tracker search
        self.search = search.Search(self.model)

        self.setupViews()

        # openAction.triggered.connect(self.openFile)
        # saveAction.triggered.connect(self.saveFile)
        quitAction.triggered.connect(QApplication.instance().quit)
        aboutAction.triggered.connect(self.informationMessage)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(helpMenu)
        self.statusBar()
        self.setWindowTitle("Tracker Search")
        self.setSearchBoxFocus()

        shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        shortcut.activated.connect(self.setSearchBoxFocus)

    def setSearchBoxFocus(self):
        # print("setSearchBoxFocus")
        self.searchBoxLineEdit.setFocus()

    def informationMessage(self):
        QMessageBox.information(self, "About", ABOUT_MSG)

    def closeEvent(self, event):
        # Write window size and position to config file
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        QMainWindow.closeEvent(self, event)

    def enterOrOkButtonClicked(self):
        self.searchBoxLineEdit.text()
        # print("Search for:" + self.searchBoxLineEdit.text())
        self.search.searchItems(self.searchBoxLineEdit.text())
        self.setWindowTitle(self.searchBoxLineEdit.text() + ' - Tracker Search')

    def setupModel(self):
        self.model = QStandardItemModel(0, 6, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Filename")
        self.model.setHeaderData(1, Qt.Horizontal, "Snippet")
        self.model.setHeaderData(2, Qt.Horizontal, "Type")
        self.model.setHeaderData(3, Qt.Horizontal, "Size")
        self.model.setHeaderData(4, Qt.Horizontal, "Modified")
        self.model.setHeaderData(5, Qt.Horizontal, "Path")

    def setupViews(self):
        self.createSidebarView()
        self.createSearchAndTable()

        # Setup main window horizontal split
        self.mainLayout = QSplitter(Qt.Horizontal)
        self.mainLayout.addWidget(self.sidebarGroup)
        self.mainLayout.addWidget(self.searchAndTableSplit)

        # Make left split fixed and right split variable
        self.mainLayout.setStretchFactor(0, 0)
        self.mainLayout.setStretchFactor(1, 1)

        self.table.setModel(self.model)

        # Table setup, which column is variable and which is fixed
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)

        self.setCentralWidget(self.mainLayout)

    def btnstate(self, state):
        print("Button:" + str(state))

    def createSidebarView(self):
        # Setup sidebar
        self.sidebarGroup = QFrame()
        self.sidebarGroup.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.sidebarGroup.setLineWidth(1)
        self.sidebarLayout = QVBoxLayout()

        # Setup sidebar for filtering
        self.sideBar = sidebar.Sidebar(self.settings, self.sidebarLayout, self.search.setSearchFilters)

        self.sidebarLayout.setAlignment(Qt.AlignTop)
        self.sidebarGroup.setLayout(self.sidebarLayout)

    def createSearchAndTable(self):
        self.searchAndTableSplit = QSplitter(Qt.Vertical)

        self.searchGroup = QGroupBox()
        self.searchLayout = QHBoxLayout()

        #Search split top part
        self.searchBoxLabel = QLabel("Search:")
        self.searchLayout.addWidget(self.searchBoxLabel)

        self.searchBoxLineEdit = QLineEdit()

        self.searchLayout.addWidget(self.searchBoxLineEdit)

        self.searchBoxOKButton = QPushButton("&OK")
        self.searchBoxOKButton.clicked.connect(self.enterOrOkButtonClicked)
        self.searchBoxLineEdit.returnPressed.connect(self.enterOrOkButtonClicked)
        self.searchLayout.addWidget(self.searchBoxOKButton)
        self.searchGroup.setLayout(self.searchLayout)

        # Table split bottom part
        self.table = MyTableView(self.model)

        # Add parts to the split
        self.searchAndTableSplit.addWidget(self.searchGroup)
        self.searchAndTableSplit.addWidget(self.table)

        self.searchAndTableSplit.setSizes([50, 450])

        # Make top split fixed and bottom split variable
        self.searchAndTableSplit.setStretchFactor(0, 0)
        self.searchAndTableSplit.setStretchFactor(1, 1)


class MyTableView(QTableView):
    def __init__(self, dataModel):
        self.dataModel = dataModel
        super(MyTableView, self).__init__()
        self.setSelectionBehavior(QTableView.SelectRows)

        # Get an event when clicking on the table (row)
        self.doubleClicked.connect(self.onTableDoubleClicked)
        self.clicked.connect(self.onTableClicked)

        # When double click a cell/row, don't go into edit mode
        self.setEditTriggers(QTableView.NoEditTriggers)

    def keyPressEvent(self, event):
        super(QTableView, self).keyPressEvent(event)
        # Determine the current selected table row
        indexes = self.selectionModel().selectedRows()
        for index in sorted(indexes):
            self.selectedRow = index.row()

        # Open the file when hitting enter or return
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            url = self.dataModel.index(self.selectedRow, 5).data()
            self.openFileWithDefaultApplication(unquote(url))

    def onTableClicked(self, event):
        self.selectedRow = event.row()
        # print("SingleClick:" + str(self.selectedRow))

    def onTableDoubleClicked(self, event):
        self.selectedRow = event.row()
        # print("DoubleClick:" + str(self.selectedRow))
        url = self.dataModel.index(self.selectedRow, 5).data()
        self.openFileWithDefaultApplication(unquote(url))

    def openFileWithDefaultApplication(self, file):
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)

    def resizeEvent(self, event):
        """ Resize all sections to content and user interactive """
        tableWidth = event.size().width()
        # print("resizeEvent: width=%d" % tableWidth)

        columnSize = [300, 0, 40, 60, 160, 0]
        # [0], width=300, flexible=False)  #Filename
        # [1], width=0,   flexible=True)   #Snippet
        # [2], width=40,  flexible=False)  #Type
        # [3], width=60,  flexible=False)  #Size
        # [4], width=160, flexible=False)  #Modified
        # [5], width=0,   flexible=True)   #Path

        # Calculate the total fixed column width
        totalFixedWidth = sum(columnSize)
        # There are 2 flexible columns, so divide by 2
        restWidth = (tableWidth - totalFixedWidth) / 2
        if restWidth < 0:
            restWidth = 0
        # print("FixedWith=%d restWidth=%d" % (totalFixedWidth, restWidth))

        super(QTableView, self).resizeEvent(event)
        header = self.horizontalHeader()
        for column in range(header.count()):
            if columnSize[column] != 0:
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, columnSize[column])
            else:
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                contentWidth = header.sectionSize(column)
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                if contentWidth < restWidth:
                    width = contentWidth
                else:
                    width = restWidth
                header.resizeSection(column, width)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Search Tracker")

    rootWindow = MainWindow()

    rootWindow.show()
    sys.exit(app.exec_())
