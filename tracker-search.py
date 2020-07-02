#!/usr/bin/python3
from tkinter import Tk, Entry, Button, Frame, Checkbutton, IntVar
from tkinter import ttk

import time

import config
import search_tracker
import window
import multi_listbox
import sidebar

search = None
win = None
sideBar = None


# Event when moving/resizing the application window
def geometryChangedEvent(event):
    config.saveConfigfile()
    multiListbox.adaptColumns()


# Event callback when clicking on Ok button to search
def okButtonClickCallback():
    searchStr = win.searchBox.get()
    search.searchItems(searchStr)


# Event callback when pressing enter in search field
def keypressCallback(event):
    if event.char == '\r':
        searchStr = win.searchBox.get()
        print("Enter pressed: %s" % searchStr)
        search.searchItems(searchStr)
    else:
        print("Other key pressed:" + event)


root = Tk()
root.title("Tracker Search GUI")

config = config.Config(root)

# Recall stored window geometry settings
root.geometry(config.config.get('geometry', 'size'))

# Tkinter theme
# root.style = ttk.Style()
# root.style.theme_use("classic")

# Setup event callbacks:
root.bind('<Return>', keypressCallback) # When pressing return in search field
root.bind("<Configure>", geometryChangedEvent) # When window is resized

win = window.Window(okButtonClickCallback)

# Setup the multicolumn ListBox
multiListbox = multi_listbox.MultiListbox(win.mainFrame)

# Setup the sidebars to filter results
sideBar = sidebar.Sidebar(config, win)

# Setup the tracker search
search = search_tracker.SearchTracker(multiListbox.tree)

root.mainloop()
