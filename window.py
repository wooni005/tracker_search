from tkinter import ttk


class Window:
    def __init__(self, okButtonClickCallback):
        self._okButtonClickCallback = okButtonClickCallback
        # the main window is divided into left and right sections,
        # and the sidebar is divided into a top and bottom section.
        self.panedWindow = ttk.PanedWindow(orient="horizontal")
        self.sidebar = ttk.PanedWindow(self.panedWindow, orient="vertical")

        self.mainFrame = ttk.Frame(self.panedWindow, width=400, height=400)
        self.mainFrame.pack(fill='both', expand=True)

        self.searchBox = ttk.Entry(self.mainFrame)
        self.searchBox.focus_set()
        self.searchBox.grid(column=0, row=0, sticky='ew', in_=self.mainFrame)

        self.okButton = ttk.Button(self.mainFrame, text="OK", width=10, command=self._okButtonClickCallback)
        self.okButton.grid(column=1, row=0, sticky='e', in_=self.mainFrame)

        self.sidebarTop = ttk.Frame(self.sidebar, width=200, height=200)
        self.sidebarBottom = ttk.Frame(self.sidebar, width=200, height=200)

        # add the paned window to the root
        self.panedWindow.pack(fill="both", expand=True)

        # add the sidebar and main area to the main paned window
        self.panedWindow.add(self.sidebar)
        self.panedWindow.add(self.mainFrame)

        # add the top and bottom to the sidebar
        self.sidebar.add(self.sidebarTop)
        self.sidebar.add(self.sidebarBottom)
