import gi
gi.require_version("Tracker", "2.0")
from gi.repository import Tracker
import os
import sys
# import time
from PySide2.QtGui import QStandardItem


class Search:
    searchIndex = []

    def __init__(self, model):
        self.model = model

    def fileSizeFmt(num, suffix='B'):
        print(num)
        for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.0f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%1.0f%s%s" % (num, 'Yi', suffix)

    def searchItems(self, searchStr):
        # start = time.time()

        # Cleanup the search index
        self.searchIndex.clear()

        conn = Tracker.SparqlConnection.get(None)
        # cursor = conn.query("SELECT ?url fts:snippet(?r) ?type ?filename ?filesize ?modifiedDate fts:rank(?r) WHERE { ?r a nfo:Document ; nie:url ?url ; nie:mimeType ?type ; nfo:fileName ?filename ; nfo:fileSize ?filesize ; nfo:fileLastModified ?modifiedDate ;fts:match '%s' } ORDER BY DESC (fts:rank(?r))" % searchStr)
        cursor = conn.query("SELECT ?url fts:snippet(?r) ?filename ?filesize ?modifiedDate WHERE { ?r a nfo:Document ; nie:url ?url ; nfo:fileName ?filename ; nfo:fileSize ?filesize ; nfo:fileLastModified ?modifiedDate ;fts:match '%s' } ORDER BY ASC (?url)" % searchStr)
        while cursor.next():
            url = cursor.get_string([0][0])[0]
            snippet = cursor.get_string([1][0])[0]
            # mimeType = cursor.get_string([2][0])[0]
            filename = cursor.get_string([2][0])[0]
            filesize = cursor.get_string([3][0])[0]
            modifiedDate = cursor.get_string([4][0])[0]
            # rank = cursor.get_string([6][0])[0]

            snippet = snippet.replace("\n", " ") # Remove all linefeeds in snippet

            item = []
            item.append(filename)                #0-filename
            item.append(snippet)                 #1-snippet
            # currentItem.append(rank)                  #-rank
            item.append(filename.split(".")[-1]) #2-type (extension)
            #currentItem.append(self.fileSizeFmt(int(filesize)))
            if int(filesize) < 1024:
                filesize = 1 #Minimum filesize=1kB and not 0kB
            else:
                filesize = int(filesize) / 1024
            item.append("%dkB" % (filesize))     #3-filesize

            #Cleanup modifiedDate
            modifiedDate = modifiedDate.replace("T", " ")
            modifiedDate = modifiedDate.replace("Z", "")
            item.append(modifiedDate)            #4-modifiedDate

            # Append to item and remove "file://" from url
            item.append(url[7:])                     #5-url

            self.searchIndex.append(item)
        self.displayIndex()
        # end = time.time()
        # print(end - start)

    def setSearchFilters(self, docFilter, areaFilter):
        self.docFilter = docFilter
        self.areaFilter = areaFilter
        self.displayIndex()

    def displayIndex(self):
        # start = time.time()

        # Clear the listbox for the new search items
        self.model.setRowCount(0)

        for item in self.searchIndex:
            #item[2]: docFilter
            #item[5]: url
            if (item[2] in self.docFilter) and any(x in item[5] for x in self.areaFilter):
                row = []
                for v in item:
                    row.append(QStandardItem(v))
                self.model.appendRow(row)

        # end = time.time()
        # print(end - start)
