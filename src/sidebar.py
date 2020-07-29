from src import check_button
from PySide2.QtWidgets import (QFrame)

docCheckButtons = []
searchAreaCheckButtons = []
documentTypesDefaults = {
    ('PDF', 'pdf'), ('Markdown', 'md'), ('TXT', 'txt'), ('MP3', 'mp3'), ('Doc', 'docs')
}
searchAreasDefaults = {
    ('Tijdschriften', '/home/arjan/Nas/Tijdschriften'), ('Notities', '/home/arjan/Documenten/Gitea/Notities/Notities'), ('Computerboeken', '/home/arjan/Nas/Boeken/Computer')
}


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Sidebar:
    global documentTypesDefaults
    global searchAreasDefaults
    docFilter = []
    areaFilter = []

    def __init__(self, settings, layout, setSearchFilters):
        self.layout = layout
        self.settings = settings
        self.setSearchFilters = setSearchFilters

        self.searchAreas = {}
        self.documentTypes = {}
        self.readSettings()
        #Place the checkbuttons in the sidebar
        for docTypeName in self.documentTypes:
            docType = self.documentTypes[docTypeName]
            # print("%s: %s" % (docTypeName, docType))
            docCheckButtons.append(check_button.classCheckButton(self.layout, docType, docTypeName, self.applySearchFilter))

        self.layout.addWidget(QHLine())

        for searchArea in self.searchAreas:
            searchAreaPath = self.searchAreas[searchArea]
            # print("%s: %s" % (searchArea, searchAreaPath))
            searchAreaCheckButtons.append(check_button.classCheckButton(self.layout, searchAreaPath, searchArea, self.applySearchFilter))

        self.applySearchFilter()

    def applySearchFilter(self):
        # print("Apply the new filter on the search window")

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

    def readSettings(self):
        size = self.settings.beginReadArray("documentTypes")
        if size == 0:
            print("No array found: Init with default settings")
            self.settings.endArray()

            self.generateDefaultConfigSettings()
            size = self.settings.beginReadArray("documentTypes")

        for i in range(size):
            self.settings.setArrayIndex(i)
            docTypeName = self.settings.value("name")
            docType = self.settings.value("type")
            # print("%d - %s: %s" % (i + 1, docTypeName, docType))
            self.documentTypes[docTypeName] = docType
        self.settings.endArray()
        # print(self.documentTypes)

        size = self.settings.beginReadArray("searchAreas")
        for i in range(size):
            self.settings.setArrayIndex(i)
            searchArea = self.settings.value("name")
            searchAreaPath = self.settings.value("path")
            # print("%d - %s: %s" % (i + 1, searchArea, searchAreaPath))
            self.searchAreas[searchArea] = searchAreaPath
        self.settings.endArray()
        # print(self.searchAreas)

    def generateDefaultConfigSettings(self):
        # Generate config settings with defaults
        self.settings.beginWriteArray("documentTypes")
        i = 0
        for docTypeName, docType in documentTypesDefaults:
            self.settings.setArrayIndex(i)
            self.settings.setValue("name", docTypeName)
            self.settings.setValue("type", docType)
            i = i + 1
        self.settings.endArray()

        self.settings.beginWriteArray("searchAreas")
        i = 0
        for searchArea, searchAreaPath in searchAreasDefaults:
            self.settings.setArrayIndex(i)
            self.settings.setValue("name", searchArea)
            self.settings.setValue("path", searchAreaPath)
            i = i + 1
        self.settings.endArray()
