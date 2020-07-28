from PySide2.QtWidgets import (QCheckBox)


class classCheckButton:
    def __init__(self, layout, filter, checkButtonName, callback):
        self.checkButtonName = checkButtonName
        self.layout = layout
        self.filter = filter
        self._callback = callback
        self.checkbutton = QCheckBox(text=self.checkButtonName)
        self.checkbutton.setChecked(True)
        self.stat = self.checkbutton.isChecked()
        self.checkbutton.toggled.connect(lambda: self.eventCheckButton())
        self.layout.addWidget(self.checkbutton)

    def get(self):
        return self.checkbutton.isChecked()

    def eventCheckButton(self):
        self.stat = self.checkbutton.isChecked()
        print("%s: checkButton=%d" % (self.checkButtonName, self.checkbutton.isChecked()))
        if self._callback:
            self._callback()
