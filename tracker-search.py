#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk

import time

import config
import search
import window
import multi_listbox
import sidebar

# search = None
# win = None
# sideBar = None


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


root = tk.Tk(className="Tracker Search")
root.title("Tracker Search")
config = config.Config(root)
img = tk.Image("photo", file="/home/arjan/Documenten/Gitea/Python/Tracker-Search/icons/tracker-search.png")
root.tk.call('wm', 'iconphoto', root._w, img)

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

# Setup the tracker search
search = search.Search(multiListbox.tree)

# Setup the sidebars to filter results
sideBar = sidebar.Sidebar(config, win, search.setSearchFilters)

if __name__ == '__main__': 
    root.mainloop()
