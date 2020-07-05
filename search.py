import gi
gi.require_version("Tracker", "2.0")
from gi.repository import Tracker
import os
import sys
# import time


class Search:
    searchIndex = []

    def __init__(self, tree):
        self.tree = tree

    def fileSizeFmt(num, suffix='B'):
        print(num)
        for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.0f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%1.0f%s%s" % (num, 'Yi', suffix)

    def searchItems(self, searchStr):
        # start = time.time()

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
            item.append(url)                     #4-url
            #Cleanup modifiedDate
            modifiedDate = modifiedDate.replace("T", " ")
            modifiedDate = modifiedDate.replace("Z", "")
            item.append(modifiedDate)            #5-modifiedDate

            item[4] = url[7:] # Remove "file://" from url
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
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.searchIndex:
            #item[2]: docFilter
            #item[4]: url
            if (item[2] in self.docFilter) and any(x in item[4] for x in self.areaFilter):
                self.tree.insert('', 'end', values=item)
                #adjust column's width if necessary to fit each value
                # for ix, val in enumerate(currentItem):
                #     col_w = tkFont.Font().measure(val)
                #     if tree.column(searchListHeader[ix], width=None) < col_w:
                #         tree.column(searchListHeader[ix], width=col_w)
        # end = time.time()
        # print(end - start)
