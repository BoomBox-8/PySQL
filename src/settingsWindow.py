'''settingsWindow
A file used to store the SettingsWindow class along with its
associated methods. '''

import themes
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (

    QFormLayout,
    qApp,
    QComboBox,
    QFontComboBox,
    QLineEdit,
    QMainWindow,
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

        
        self.paletteList = [themes.cottonCandy, themes.mango, themes.raspberry, themes.lime,  themes.ocean] #cotton candy rasperbyy/lime monochrome ocean
        self.setWindowTitle('Settings')
        self.container = QWidget()
        self.layout = QFormLayout()
        self.container.setLayout(self.layout)

        fontSelector = QFontComboBox()
        fontSelector.setFontFilters(QFontComboBox.MonospacedFonts)
        fontSelector.setCurrentFont(textEdit.font()) #setting initial value
        fontSelector.currentFontChanged.connect(lambda font: textEdit.setFontFamily(font.family()))
        fontSelector.currentFontChanged.connect(lambda font: console.setFontFamily(font.family()))

        fontSizeConsole = QSpinBox()
        fontSizeConsole.setValue(console.font().pointSize()) #setting initial value
        fontSizeConsole.valueChanged.connect(lambda size: self.changeFont(console, size))

        fontSizeEntry = QSpinBox()
        fontSizeEntry.setValue(textEdit.font().pointSize())
        fontSizeEntry.valueChanged.connect(lambda size: self.changeFont(textEdit, size))

        macroOneEdit = QLineEdit()
        macroOneEdit.setPlaceholderText(window.macroOne)
        macroOneEdit.returnPressed.connect(lambda: setattr(window,'macroOne', macroOneEdit.text()))

        macroTwoEdit = QLineEdit()
        macroTwoEdit.setPlaceholderText(window.macroTwo)
        macroTwoEdit.returnPressed.connect(lambda: setattr(window,'macroTwo', macroTwoEdit.text()))

        macroThreeEdit = QLineEdit()
        macroThreeEdit.setPlaceholderText(window.macroThree)
        macroThreeEdit.returnPressed.connect(lambda: setattr(window,'macroThree', macroThreeEdit.text()))

        self.themesComboBox = QComboBox()
        self.themesComboBox.addItems(['Cotton Candy', 'Mango Twist', 'Raspberry', 'QT Lime Pie', 'Ocean'])
        self.themesComboBox.activated.connect(lambda index: self.changeTheme(index, panel, window))

        for i in (fontSelector, fontSizeConsole, fontSizeEntry,
                macroOneEdit,macroTwoEdit, macroThreeEdit, self.themesComboBox):

            i.sizeHint = lambda: QSize(180,30) #sets size hint of all widgets
       
        self.layout.setSpacing(30)
        self.layout.addRow('Font Selector', fontSelector)
        self.layout.addRow('Font Size (Console)', fontSizeConsole)
        self.layout.addRow('Font Size (Entry Field)', fontSizeEntry)
        self.layout.addRow('Edit Macro One', macroOneEdit)
        self.layout.addRow('Edit Macro Two', macroTwoEdit)
        self.layout.addRow('Edit Macro Three', macroThreeEdit)
        self.layout.addRow('Theme Selector', self.themesComboBox)
        self.layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.setCentralWidget(self.container)


    @staticmethod
    def changeFont(obj,size) -> None:
        fontObj = obj.font()
        fontObj.setPointSize(size)
        obj.setFont(fontObj)


    def changeTheme(self, index, panel, window) -> None:
        qApp.setPalette(self.paletteList[index])
        panelPalette = panel.palette
        panelPalette.setColor(QPalette.Button, self.paletteList[index].base().color())
        panel.setPalette(panelPalette)
        window.statusBar().showMessage(f'Last Operation: Theme Changed to {self.themesComboBox.currentText()}')
   

