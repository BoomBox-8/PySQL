'''settingsWindow
A file used to store the SettingsWindow class along with its
associated methods. '''

import json
import themes
from os import path
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (

    QFormLayout,
    qApp,
    QComboBox,
    QFontComboBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QWidget,
)


class SettingsWindow(QMainWindow):
    '''A modal window used to modify various settings
    Allows for the changing of various settings, such as the font and
    font size for the console & editor, themes, and so on.
       
    Widgets to control the font family, and font sizes of the
    console and text entry fields are included, along with
    widgets that control the theme and change macros

    No settings persistence is offered, so as such, preferred settings
    will have to be set everytime the program is booted up
       
    Attributes
    ----------
    paletteList
        Contains palette objects created in themes.py, to allow
        for theming
    container
        The widget containing the 'master' layout of the window
    themesComboBox
        A combo box listing the various themes on offer
    
    Methods
    -------
    changeFont
        In reality, sets font size of object obj to size size
        As QTextEdits don't offer a method to change font sizes as
        easily as they do to change font families, the method was
        created for this purpose
    changeTheme
        Uses the returned index from themesComboBox to set the app
        theme.
        The toolbar/panel is passed in to set its bg color to that
        of the app's due to the fact that it is considered a
        button and takes on the specified button color as a result,
        causing one to end up with a garishly colored toolbar'''

    def __init__(self, window, textEdit, console, panel):
        super().__init__(window)

        self.paletteDict = themes.themesDict

        self.setWindowTitle('Settings')
        self.setMaximumSize(QSize(180,30))
        self.container = QWidget()
        self.layout = QFormLayout()
        self.container.setLayout(self.layout)

        self.fontSelector = QFontComboBox()
        self.fontSelector.setFontFilters(QFontComboBox.MonospacedFonts)
        self.fontSelector.setCurrentFont(textEdit.font()) #setting initial value
        self.fontSelector.currentFontChanged.connect(lambda font: self.changeFont(textEdit, textEdit.font().pointSize(), font.family()))
        self.fontSelector.currentFontChanged.connect(lambda font: self.changeFont(console, console.font().pointSize(), font.family()))

        self.fontSizeConsole = QSpinBox()
        self.fontSizeConsole.setValue(console.font().pointSize()) #setting initial value
        self.fontSizeConsole.valueChanged.connect(lambda size: self.changeFont(console, size, console.font().family()))

        self.fontSizeEntry = QSpinBox()
        self.fontSizeEntry.setValue(textEdit.font().pointSize())
        self.fontSizeEntry.valueChanged.connect(lambda size: self.changeFont(textEdit, size, textEdit.font().family()))

        self.macroOneEdit = QLineEdit()
        self.macroOneEdit.setText(window.macroOne)
        self.macroOneEdit.returnPressed.connect(lambda: setattr(window,'macroOne', self.macroOneEdit.text()))

        self.macroTwoEdit = QLineEdit()
        self.macroTwoEdit.setText(window.macroTwo)
        self.macroTwoEdit.returnPressed.connect(lambda: setattr(window,'macroTwo', self.macroTwoEdit.text()))

        self.macroThreeEdit = QLineEdit()
        self.macroThreeEdit.setText(window.macroThree)
        self.macroThreeEdit.returnPressed.connect(lambda: setattr(window,'macroThree', self.macroThreeEdit.text()))

        

        self.themesComboBox = QComboBox()
        self.themesComboBox.addItems([i for i in self.paletteDict])
        self.themesComboBox.textActivated.connect(lambda theme: self.changeTheme(theme, panel, window))

        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(lambda: self.saveSettings(window))
        
        for i in (self.fontSelector, self.fontSizeConsole, self.fontSizeEntry,
                self.macroOneEdit, self.macroTwoEdit, self.macroThreeEdit, self.themesComboBox, self.saveButton):

            i.sizeHint = lambda: QSize(180,30) #sets size hint of all widgets

       
        self.layout.setSpacing(30)
        self.layout.addRow('Font Selector', self.fontSelector)
        self.layout.addRow('Font Size (Console)', self.fontSizeConsole)
        self.layout.addRow('Font Size (Entry Field)', self.fontSizeEntry)
        self.layout.addRow('Edit Macro One', self.macroOneEdit)
        self.layout.addRow('Edit Macro Two', self.macroTwoEdit)
        self.layout.addRow('Edit Macro Three', self.macroThreeEdit)
        self.layout.addRow('Theme Selector', self.themesComboBox)
        self.layout.addRow(self.saveButton)
        self.layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.setCentralWidget(self.container)


    @staticmethod
    def changeFont(obj, size, family) -> None:
        fontObj = obj.font()
        fontObj.setFamily(family)
        fontObj.setPointSize(size)
        obj.setFont(fontObj)


    def changeTheme(self, theme, panel, window) -> None:
        qApp.setPalette(self.paletteDict[theme])
        panelPalette = panel.palette
        panelPalette.setBrush(QPalette.Button, self.paletteDict[theme].base())
        panel.setPalette(panelPalette)
        window.statusBar().showMessage(f'Last Operation: Theme Changed to {self.themesComboBox.currentText()}')

    
    def saveSettings(self, window) -> None:
        with open(f'{path.dirname(path.abspath(__file__))}/assets/config/settings.json', 'w+') as settings:

                json.dump({
                    'Font' : self.fontSelector.currentFont().family() ,
                    'Font Size (Console)' : self.fontSizeConsole.value(),
                    'Font Size (Entry Field)' :  self.fontSizeEntry.value(),
                    'Macro One' : self.macroOneEdit.text(),
                    'Macro Two' : self.macroTwoEdit.text(),
                    'Macro Three' : self.macroThreeEdit.text(),
                    'Theme' : self.themesComboBox.currentText()
                    }, settings, indent = 1)
                
                window.statusBar().showMessage(f'Settings Saved')
   
