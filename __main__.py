#!/usr/bin/env python
import time
import sys
import os
import subprocess

from PySide2.QtCore import Qt, QAbstractTableModel, QRect, QSize, QPoint, QSettings
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2.QtWidgets import (QApplication, QMenu, QMainWindow, QHeaderView, QSplitter, QTableView, QGroupBox, QFrame, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton)

from src import search
from src import sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        fileMenu = QMenu("&File", self)
        # openAction = fileMenu.addAction("&Open...")
        # openAction.setShortcut("Ctrl+O")
        # saveAction = fileMenu.addAction("&Save As...")
        # saveAction.setShortcut("Ctrl+S")
        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")

        appIcon = QIcon("/home/arjan/Documenten/Gitea/Python/tracker_search/icons/tracker_search.png")
        self.setWindowIcon(appIcon)

        self.settings = QSettings("tracker_search", "settings")

        #TODO: Application Icon
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

        self.menuBar().addMenu(fileMenu)
        self.statusBar()
        self.setWindowTitle("Tracker Search")
        self.searchBoxLineEdit.setFocus()

    def closeEvent(self, event):
        # Write window size and position to config file
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        QMainWindow.closeEvent(self, event)

    def okButtonClicked(self):
        self.searchBoxLineEdit.text()
        print("Search for:" + self.searchBoxLineEdit.text())
        self.search.searchItems(self.searchBoxLineEdit.text())

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
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(4, 50)
        self.table.setColumnWidth(5, 50)

        # Table setup, which column is variable and which is fixed
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)

        # self.table.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)

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
        self.searchBoxOKButton.clicked.connect(self.okButtonClicked)
        self.searchBoxLineEdit.returnPressed.connect(self.okButtonClicked)
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
        self.doubleClicked.connect(self.onTableClicked)

        # When double click a cell/row, don't go into edit mode
        self.setEditTriggers(QTableView.NoEditTriggers)

    def onTableClicked(self, event):
        clickedRow = event.row()
        url = self.dataModel.index(clickedRow, 5).data()
        self.openFileWithDefaultApplication(url)

    def openFileWithDefaultApplication(self, file):
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)

    def resizeEvent(self, event):
        """ Resize all sections to content and user interactive """
        print("resizeEvent")
        # Header[0], width=300, stretch=False) #Filename
        # Header[1], minwidth=100, stretch=True) #Snippet
        # Header[2], width=40, stretch=False)  #Type
        # Header[3], width=60, stretch=False)  #Size
        # Header[4], width=160, stretch=False) #Modified
        # Header[5], minwidth=100, stretch=True) #Path

        columnSize = [300, 0, 40, 60, 160, 0]
        super(QTableView, self).resizeEvent(event)
        header = self.horizontalHeader()
        for column in range(header.count()):
            if columnSize[column] != 0:
                # header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                # width = header.sectionSize(column)
                # header.setSectionResizeMode(column, QHeaderView.Interactive)
                # header.resizeSection(column, width)
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, columnSize[column])
            else:
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                # width = header.sectionSize(column)
                # header.minimumSectionSize(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Search Tracker")

    rootWindow = MainWindow()

    rootWindow.show()
    sys.exit(app.exec_())
