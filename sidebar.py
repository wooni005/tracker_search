from tkinter import Checkbutton, IntVar
import check_button

docCheckButtons = []
searchAreaCheckButtons = []


class Sidebar:
    docFilter = []
    areaFilter = []

    def __init__(self, config, frame, setSearchFilters):
        self.frame = frame
        self.config = config
        self.setSearchFilters = setSearchFilters
        #Place the checkbuttons in the sidebar
        documentTypes = config.items('documentTypes')
        for docType, docTypeName in documentTypes:
            print("%s: %s" % (docType, docTypeName))
            docCheckButtons.append(check_button.classCheckButton(self.frame.sidebarTop, docType, docTypeName, self.applySearchFilter))

        searchAreas = config.items('searchAreas')
        #print(searchAreas)
        for searchArea, searchAreaPath in searchAreas:
            print("%s: %s" % (searchArea, searchAreaPath))
            searchAreaCheckButtons.append(check_button.classCheckButton(self.frame.sidebarBottom, searchAreaPath, searchArea, self.applySearchFilter))
        
        self.applySearchFilter()

    def applySearchFilter(self):
        print("Apply the new filter on the search window")

        self.docFilter.clear() # Reset filter
        for button in docCheckButtons:
            # print("%s: %d" % (button.filter, button.get()))
            if button.get():
                self.docFilter.append(button.filter)

        self.areaFilter.clear() # Reset filter
        for button in searchAreaCheckButtons:
            # print("%s: %d" % (button.filter, button.get()))
            if button.get():
                self.areaFilter.append(button.filter)

        self.setSearchFilters(self.docFilter, self.areaFilter)
