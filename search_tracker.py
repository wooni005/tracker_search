from tkinter import Checkbutton, IntVar
import gi
gi.require_version("Tracker", "2.0")
from gi.repository import Tracker
import os
import sys


class SearchTracker:
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
        # Clear the listbox for the new search items
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = Tracker.SparqlConnection.get(None)
        # cursor = conn.query("SELECT ?url fts:snippet(?r) ?type ?filename ?filesize ?modifiedDate fts:rank(?r) WHERE { ?r a nfo:Document ; nie:url ?url ; nie:mimeType ?type ; nfo:fileName ?filename ; nfo:fileSize ?filesize ; nfo:fileLastModified ?modifiedDate ;fts:match '%s' } ORDER BY DESC (fts:rank(?r))" % searchStr)
        cursor = conn.query("SELECT ?url fts:snippet(?r) ?filename ?filesize ?modifiedDate WHERE { ?r a nfo:Document ; nie:url ?url ; nfo:fileName ?filename ; nfo:fileSize ?filesize ; nfo:fileLastModified ?modifiedDate ;fts:match '%s' } ORDER BY ASC (?url)" % searchStr)
        listCount = 0
        while cursor.next():
            url = cursor.get_string([0][0])[0]
            snippet = cursor.get_string([1][0])[0]
            # mimeType = cursor.get_string([2][0])[0]
            filename = cursor.get_string([2][0])[0]
            filesize = cursor.get_string([3][0])[0]
            modifiedDate = cursor.get_string([4][0])[0]
            # rank = cursor.get_string([6][0])[0]

            snippet = snippet.replace("\n", " ") # Remove all linefeeds in snippet

            currentItem = []
            currentItem.append(filename)                #0-filename
            currentItem.append(snippet)                 #1-snippet
            # currentItem.append(rank)                  #-rank
            currentItem.append(filename.split(".")[-1]) #2-type (extension)
            #currentItem.append(self.fileSizeFmt(int(filesize)))
            if int(filesize) < 1024:
                filesize = 1 #Minimum filesize=1kB and not 0kB
            else:
                filesize = int(filesize) / 1024
            currentItem.append("%dkB" % (filesize))     #3-filesize
            currentItem.append(url)                     #4-url
            #Cleanup modifiedDate
            modifiedDate = modifiedDate.replace("T", " ")
            modifiedDate = modifiedDate.replace("Z", "")
            currentItem.append(modifiedDate)            #5-modifiedDate

            currentItem[4] = url[7:] # Remove "file://" from url
            listCount += 1
            self.tree.insert('', 'end', values=currentItem)

            #adjust column's width if necessary to fit each value
            # for ix, val in enumerate(currentItem):
            #     col_w = tkFont.Font().measure(val)
            #     if tree.column(searchListHeader[ix], width=None) < col_w:
            #         tree.column(searchListHeader[ix], width=col_w)
