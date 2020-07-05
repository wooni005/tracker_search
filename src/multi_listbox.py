from tkinter import ttk
import tkinter.font as tkFont
import os
import sys
import subprocess

searchListHeader = ['Filename', "Snippet", "Type", "Size", "Path", "Modified"]

###############################################
# Use a ttk.TreeView as a multicolumn ListBox
###############################################


class MultiListbox:
    def __init__(self, frame):
        self.frame = frame
        self.tree = None
        self.setupWidgets()
        self.buildTree()

    def setupWidgets(self):
        # Create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=searchListHeader, show="headings")
        self.tree.bind('<Double-1>', self.eventSelectListbox)

        vertScrollbar = ttk.Scrollbar(orient="vertical",  command=self.tree.yview)
        horScrollbar = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vertScrollbar.set, xscrollcommand=horScrollbar.set)
        self.tree.configure(yscrollcommand=vertScrollbar.set)

        self.tree.grid(column=0, columnspan=2, row=1, sticky='nsew', in_=self.frame)

        vertScrollbar.grid(column=2, row=1, sticky='ns', in_=self.frame)
        horScrollbar.grid(column=0, columnspan=2, row=2, sticky='ew', in_=self.frame)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

    def buildTree(self):
        for col in searchListHeader:
            self.tree.heading(col, text=col.title(), command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        self.adaptColumns()

    def adaptColumns(self):
        self.tree.column(searchListHeader[0], width=300, stretch=False) #Filename
        self.tree.column(searchListHeader[1], minwidth=100, stretch=True) #Snippet
        self.tree.column(searchListHeader[2], width=40, stretch=False)  #Type
        self.tree.column(searchListHeader[3], width=60, stretch=False)  #Size
        self.tree.column(searchListHeader[4], minwidth=100, stretch=True) #Path
        self.tree.column(searchListHeader[5], width=150, stretch=False) #Modified

    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(self.tree.set(child, col), child) for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def eventSelectListbox(self, event):
        #Skip the header row
        if self.tree.focus() != "":
            item = self.tree.item(self.tree.focus())
            # print(item)
            self.openFileWithDefaultApplication(item['values'][4])

    def openFileWithDefaultApplication(self, file):
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", file])
        else:
            os.startfile(file)
