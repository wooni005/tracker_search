from tkinter import Checkbutton, IntVar
import check_button

docCheckButtons = {}
searchAreaCheckButtons = {}


class Sidebar:
    def __init__(self, config, frame):
        self.frame = frame
        self.config = config

        #Place the checkbuttons in the sidebar
        documentTypes = config.items('documentTypes')
        for docType, docTypeName in documentTypes:
            print("%s: %s" % (docType, docTypeName))
            docCheckButtons[docTypeName] = check_button.classCheckButton(self.frame.sidebarTop, docTypeName, self.searchResultsFilter)

        searchAreas = config.items('searchAreas')
        #print(searchAreas)
        for searchArea, searchAreaPath in searchAreas:
            print("%s: %s" % (searchArea, searchAreaPath))
            searchAreaCheckButtons[searchArea] = check_button.classCheckButton(self.frame.sidebarBottom, searchArea, self.searchResultsFilter)

    def searchResultsFilter(self):
        print("Bereken de resultaten opnieuw")
