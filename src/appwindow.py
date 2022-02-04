'''appWindow
The file contains the various widgets users will use to interface with PySQL'''

import mysql.connector
import settingsWindow
import themes
from tableDraw import tableDraw
from os import path
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QKeySequence, QTextCursor
from PyQt5.QtWidgets import (
    
    QToolBar,
    qApp,
    QMenu,
    QShortcut,
    QAction,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTextEdit,
    QMessageBox, 
    QSizePolicy
)


class EditingWindow(QMainWindow):
    '''Inherits QMainWindow
    The window that consists of the widgets the user will use
    to interface with PySQL
    
    Attributes
    ----------
    quickPoll : list
        A list that can be used to store and execute multiple
        commands at once
    sqlComp : tuple
        A tuple containing the db and cur objects
    panel : QToolBar
        A widget containing that provides access to a settings and
        a quit button
    exitAction : QAction
        A QAction that causes the app to quit when trigerred
    exitShortcut : QShortcut
        A shortcut that triggers exitAction when pressed
    settingsAction : QAction
        A QAction that launches the settings window
    settingsShortcut : QShortcut
        A shortcut that triggers settingsAction when pressed
    console : ConsoleEdit
        Displays queries and their results, with syntax highlighting
    entryField : EntryField
        Allows for the typing of queries
    macroOne : str
        A commonly used query that can be quickly inserted
    macroShortcutOne : QShortcut
        A shortcut that sets entryField's text to macroOne
    quickPollShortcut : QShortcut
        A shortcut that appends entryField's text to quickPoll
    runQuickPollShortcut : QShortcut
        A shortcut that executes all the queries in quickPoll
    eraseQuickPollShorcut : QShortcut
        A shortcut that erases all the queries in quickPoll
    tools : QMenuBar
        A menu. Allows for an alternative way
        of accessing exitAction and settingsAction'''


    def __init__(self, sqlComp):
        super().__init__()

        self.setWindowTitle('PySQL')
        self.quickPoll = [] #will contain commands that can be queried at once
        self.sqlComp = sqlComp #passes in the required components to work with mysql
        
        
       
        qApp.setPalette(themes.raspberry)
        self.panel = QToolBar(self)
        self.panel.palette = QPalette()
        self.panel.setAutoFillBackground(True)
        self.panel.palette.setColor(QPalette.Button, QColor('#FF1e1e1e'))
        self.panel.setPalette(self.panel.palette)
        
        stretcher = QWidget() #cheap way to separate buttons
        stretcher.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.aboutMeAction = QAction(QIcon(f'{path.dirname(__file__)}/assets/aboutme.png'), 'About Me' , self)
        self.aboutMeAction.triggered.connect(self.launchAboutMe)

        self.helpAction = QAction(QIcon(f'{path.dirname(__file__)}/assets/help.png'), 'Help', self)
        self.helpAction.triggered.connect(self.launchHelp)

        self.exitAction = QAction(QIcon(f'{path.dirname(__file__)}/assets/quitIcon.png'), 'Quit', self)
        self.exitAction.triggered.connect(qApp.quit)
        self.exitShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.exitShortcut.activated.connect(lambda: self.exitAction.triggered.emit())
        self.exitShortcut.setContext(Qt.ApplicationShortcut)

        self.settingsAction = QAction(QIcon(f'{path.dirname(__file__)}/assets/settingsicon.png'), 'Settings', self)
        self.settingsAction.triggered.connect(self.launchSettings)
        self.settingsShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.settingsShortcut.activated.connect(lambda: self.settingsAction.triggered.emit(True))
        self.settingsShortcut.setContext(Qt.ApplicationShortcut)

        self.panel.addAction(self.exitAction)
        self.panel.addWidget(stretcher)
        self.panel.addAction(self.settingsAction)
        self.panel.setOrientation(Qt.Vertical)
        self.panel.setIconSize(QSize(100,100))
        self.panel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)) #constrains the width to make it look decent
        self.panel.sizeHint = lambda: QSize(150,500)
        
        self.console = ConsoleEdit(self, self.sqlComp)
        
        self.entryField = EntryField()
        self.entryField.formatText.connect(self.console.append)
        self.entryField.parseText.connect(self.console.appendParse)

        writeLayout = QVBoxLayout() #contains console + text editor
        writeLayout.addWidget(self.console)
        writeLayout.addWidget(self.entryField)
        writeLayout.addSpacing(50)
        writeLayout.setSpacing(50)
        writeLayout.setContentsMargins(11,11,11,11)
        writeLayout.setAlignment(self.entryField, Qt.AlignHCenter)

        layout = QHBoxLayout() #contains toolbar and console+text editor 
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(self.panel, Qt.AlignLeft) 
        layout.addWidget(self.panel)
        layout.addLayout(writeLayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        
        self.macroOne = 'SELECT * FROM'
        self.macroShortcutOne = QShortcut(QKeySequence(Qt.Key_F1), self)
        self.macroShortcutOne.activated.connect(self.setMacroOne)
        self.macroShortcutOne.setContext(Qt.ApplicationShortcut)
        
        self.macroTwo = 'INSERT INTO TABLE_NAME VALUES()'
        self.macroShortcutTwo = QShortcut(QKeySequence(Qt.Key_F2), self)
        self.macroShortcutTwo.activated.connect(self.setMacroTwo)
        self.macroShortcutTwo.setContext(Qt.ApplicationShortcut)

        self.macroThree = 'SELECT MAX(COLUMN_NAME) FROM TABLE_NAME'
        self.macroShortcutThree = QShortcut(QKeySequence(Qt.Key_F3), self)
        self.macroShortcutThree.activated.connect(self.setMacroThree)
        self.macroShortcutThree.setContext(Qt.ApplicationShortcut)

        self.quickPollShortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        self.quickPollShortcut.setContext(Qt.ApplicationShortcut)
        self.quickPollShortcut.activated.connect(lambda: self.pollAppend(self.entryField.toPlainText()))

        self.runQuickPollShortcut =  QShortcut(QKeySequence(Qt.SHIFT + Qt.Key_F5), self)
        self.runQuickPollShortcut.setContext(Qt.ApplicationShortcut)
        self.runQuickPollShortcut.activated.connect(self.pollExecute)

        self.eraseQuickPollShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F5), self)
        self.eraseQuickPollShortcut.setContext(Qt.ApplicationShortcut)
        self.eraseQuickPollShortcut.activated.connect(self.pollErase)
        

        self.tools = QMenu('&Tools')
        self.menuBar().addMenu(self.tools)
        self.tools.addAction(self.exitAction)
        self.tools.addSeparator()
        self.tools.addAction(self.settingsAction)
        self.tools.addSeparator()
        self.tools.addAction(self.aboutMeAction)
        self.tools.addSeparator()
        self.tools.addAction(self.helpAction)
    

    

    def closeEvent(self,e) -> None:
        '''An overidden closeEvent that prompts the user before exit
        
        Parameters
        ----------
        e : QEvent

        Returns
        -------
        None'''

        confirmQuit = QMessageBox(QMessageBox.Question, 'Quit PySQL?', 'Confirm', QMessageBox.No | QMessageBox.Yes)
        if confirmQuit.exec() == QMessageBox.Yes:
            e.accept()
            qApp.quit()

        e.ignore() #the only way to prevent closing
        


    def launchSettings(self):
        '''Launches the settings window
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        self.settingsWindow = settingsWindow.SettingsWindow(self, self.entryField, self.console, self.panel)
        self.settingsWindow.setWindowModality(Qt.WindowModal)
        self.settingsWindow.show()
        self.statusBar().showMessage('Last Operation: Settings Launched')

    
    def launchAboutMe(self) -> None:
        '''Launches an about me dialog
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        message = f'Contact me for any further queries [here](https://github.com/BoomBox-8)'
        self.aboutMe = QMessageBox(QMessageBox.Information, 'About Me', message, QMessageBox.Ok)
        self.aboutMe.setTextFormat(Qt.MarkdownText) #I don't want to use HTML syntax for hyperlinks
        self.aboutMe.exec()

    
    def launchHelp(self) -> None:
        '''Launches a help dialog listing shortcuts
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        message = '''
        F1-3 : Use Macro 1-3
        F5 : Quick Poll
        Shift + F5 : Execute Polled Queries
        Ctrl + F5 : Erase Polled Queries
        Up/Down (When Entry Field Focused) : Flip through queries
        Ctrl + S : Launch Settings
        Ctrl + Q : Quit
        Alt + T : Open Menu Bar
        
        Open included README for more details'''
        self.help = QMessageBox(QMessageBox.Information, 'Help', message, QMessageBox.Ok)
        self.help.setSizeGripEnabled(True)
        self.help.exec()



    def setMacroOne(self) -> None: #all of this could be simplified if it weren't for the signal not returning any text
        '''Sets entryField's text to macroOne
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        self.entryField.setText(self.macroOne)
        self.entryField.moveCursor(QTextCursor.End)
        self.statusBar().showMessage('Last Operation: Macro One Entered')

    
    def setMacroTwo(self):
        '''Sets entryField's text to macroTwo
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        self.entryField.setText(self.macroTwo)
        self.entryField.moveCursor(QTextCursor.End)
        self.statusBar().showMessage('Last Operation: Macro Two Entered')


    def setMacroThree(self):
        '''Sets entryField's text to macroThree
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        self.entryField.setText(self.macroThree)
        self.entryField.moveCursor(QTextCursor.End)
        self.statusBar().showMessage('Last Operation: Macro Three Entered')


    def pollExecute(self) -> None:
        '''Executes the text within quickPoll
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        if self.quickPoll != []: #only execute if quickPoll isn't empty
            for i in self.quickPoll:
                self.entryField.wordParse(i)

    def pollErase(self) -> None:
        '''Erases the contents of quickPoll
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        self.quickPoll.clear()
        self.statusBar().showMessage('Last Operation: Poll List Cleared')



    def pollAppend(self, text) -> None:
        '''Appends the current query to quickPoll
        
        Parameters
        ----------
        
        Returns
        -------
        None'''

        self.quickPoll.append(text.rstrip().upper())
        self.entryField.clear()
        self.statusBar().showMessage('Last Operation: SQL Query Polled')



class EntryField(QTextEdit):
    '''Inherits QTextEdit
    Accepts queries as inputs and passes it to console for parsing
    Widget performs minor syntax highlighting of its own
    
    Attributes
    ----------

    keyWords : set
        A set of all MySQL keywords, used to add syntax highlighting
    queryArray : list
        A list of queries entered in the past, acting as a command
        history of sorts
    curIndex : int
        Stores the current position in queryArray
    
    Methods
    -------
    formatText : pyqtSignal
        A signal that passes along syntax highlighted text
        implemented using HTML color tags to console for
        being displayed
    parseText : pyqtSignal
        A signal that passes along the text itself, to be parsed
        by console and executed as a query'''    

    keyWords = {'ADD', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC',
                     'AUTO_INCREMENT', 'BDB', 'BERKELEYDB', 'BETWEEN',
                     'BIGINT', 'BINARY', 'BLOB', 'BOTH', 'BTREE', 'BY',
                     'CASCADE', 'CASE', 'CHANGE', 'CHAR', 'CHARACTER',
                     'CHECK', 'COLLATE', 'COLUMN', 'COLUMNS', 'CONSTRAINT',
                     'CREATE', 'CROSS', 'CURRENT_DATE', 'CURRENT_TIME',
                     'CURRENT_TIMESTAMP', 'DATABASE', 'DATABASES',
                     'DAY_HOUR', 'DAY_MINUTE', 'DAY_SECOND', 'DEC',
                     'DECIMAL', 'DEFAULT', 'DELAYED', 'DELETE',
                     'DESC', 'DESCRIBE', 'DISTINCT', 'DISTINCTROW',
                     'DIV', 'DOUBLE', 'DROP', 'ELSE', 'ENCLOSED',
                     'ERRORS', 'ESCAPED', 'EXISTS', 'EXPLAIN',
                     'FALSE', 'FIELDS', 'FLOAT', 'FOR', 'FORCE',
                     'FOREIGN', 'FROM', 'FULLTEXT', 'FUNCTION',
                     'GEOMETRY', 'GRANT', 'GROUP', 'HASH',
                     'HAVING', 'HELP', 'HIGH_PRIORITY', 'HOUR_MINUTE',
                     'HOUR_SECOND', 'IF', 'IGNORE', 'IN', 'INDEX',
                     'INFILE', 'INNER', 'INNODB', 'INSERT', 'INT',
                     'INTEGER', 'INTERVAL', 'INTO', 'IS', 'JOIN',
                     'KEY', 'KEYS', 'KILL', 'LEADING', 'LEFT',
                     'LIKE', 'LIMIT', 'LINES', 'LOAD', 'LOCALTIME',
                     'LOCALTIMESTAMP', 'LOCK', 'LONG', 'LONGBLOB',
                     'LONGTEXT', 'LOW_PRIORITY', 'MASTER_SERVER_ID',
                     'MATCH', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT',
                     'MIDDLEINT', 'MINUTE_SECOND', 'MOD', 'MRG_MYISAM',
                     'NATURAL', 'NOT', 'NULL', 'NUMERIC', 'ON', 'OPTIMIZE',
                     'OPTION', 'OPTIONALLY', 'OR', 'ORDER', 'OUTER', 'OUTFILE',
                     'PRECISION', 'PRIMARY', 'PRIVILEGES', 'PROCEDURE', 'PURGE',
                     'READ', 'REAL', 'REFERENCES', 'REGEXP', 'RENAME', 'REPLACE',
                     'REQUIRE', 'RESTRICT', 'RETURNS', 'REVOKE', 'RIGHT', 'RLIKE',
                     'RTREE', 'SELECT', 'SET', 'SHOW', 'SMALLINT', 'SOME', 'SONAME',
                     'SPATIAL', 'SQL_BIG_RESULT', 'SQL_CALC_FOUND_ROWS',
                     'SQL_SMALL_RESULT', 'SSL', 'STARTING',
                     'STRAIGHT_JOIN', 'STRIPED', 'TABLE', 'TABLES',
                     'TERMINATED', 'THEN', 'TINYBLOB', 'TINYINT',
                     'TINYTEXT', 'TO', 'TRAILING', 'TRUE',
                     'TYPES', 'UNION', 'UNIQUE', 'UNLOCK',
                     'UNSIGNED', 'UPDATE', 'USAGE', 'USE',
                     'USER_RESOURCES', 'USING', 'VALUES', 'VARBINARY',
                     'VARCHAR', 'VARCHARACTER', 'VARYING', 'WARNINGS',
                     'WHEN', 'WHERE', 'WITH', 'WRITE', 'XOR', 'YEAR_MONTH', 'ZEROFILL'} #to perform syntax highlighting
    
    formatText = pyqtSignal(str) #yes, a custom signal had to be created just to cleanly pass data to the console :(
    parseText = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setFont(QFont('Fira Code Medium', 16))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.sizeHint = lambda: QSize(600,60)
        self.palette = QPalette()
        self.setPalette(self.palette)

        self.queryArray = ['']
        self.curIndex = 0      
        

    def keyPressEvent(self,e) -> None:
        '''Overrides keyPressEvent
        Allows for accessing commands from queryArray, sending text
        text to be parsed upon hitting enter, and auto-completion
        of paranthesis
        
        Parameters
        ----------
        e : QEvent
        
        Returns
        -------
        None'''

        e.accept()
        super().keyPressEvent(e)
        
        if e.key() == Qt.Key_ParenLeft:
            self.insertPlainText(')')
            self.moveCursor(QTextCursor.Left)
        
        elif e.key() == Qt.Key_Up: #command history feature
            self.curIndex -= 1
            self.setText(self.queryArray[self.curIndex % len(self.queryArray)])

        elif e.key() == Qt.Key_Down: 
            self.curIndex += 1
            self.setText(self.queryArray[self.curIndex % len(self.queryArray)])

        elif e.key() == Qt.Key_Return:
            cleanedText = self.toPlainText().rstrip()
            if cleanedText[-1] == ';':
                self.wordParse(cleanedText.upper())
            
        

    def wordParse(self, text):
        '''Emits both the query and a version of the query with
        syntax highlighting to console
        
        Parameters
        ----------
        text : str
        
        Returns
        -------
        None'''
        textArray = []

        for i in text.split():
            if i in self.keyWords:
                textArray.append(f'<font color = orange>{i}</font>')
            else:
                textArray.append(i)
        
        self.formatText.emit(f'{"mysql> "}{" ".join(textArray)}') #allows for cross-widget comms
        self.parseText.emit(text)
        self.queryArray.append(text)
        self.curIndex = 0
        self.clear()


class ConsoleEdit(QTextEdit):
    '''Inherits QTextEdit
    Displays queries and their results, with syntax higlighting where
    possible
    
    Attributes
    ----------
    callingWindow : EditingWindow
        Allows for the accessing of window widgets/properties
    sqlComp : tuple
        A tuple containing the db and cur objects
    myDb
        The database object
    myCur
        The cursor object'''

    def __init__(self,  callingWindow,  sqlComp = None):
        super().__init__()
        self.callingWindow = callingWindow
        self.sqlComp = sqlComp
        self.myDb = self.sqlComp[0]
        self.myCur = self.sqlComp[1]
        
        self.setLineWrapMode(QTextEdit.NoWrap) #prevents letters and words from warping to the next line
        self.setReadOnly(True)
        self.setFont(QFont('Fira Code Medium', 10))
        
    def appendParse(self, text : str) -> None:
        '''Executes query text and displays the result
        In the case of an error, an error message is displayed in red
        
        Parameters
        ----------
        text : str
            The query to be executed'''

        try:
           self.myCur.execute(text)
           #self.myDb.commit()
           
           textArray = [i for i in self.myCur]
           if textArray != []:
                textArray.insert(0, self.myCur.column_names)
                columnWidth = [max([len(str(j)) for j in i]) + 2 for i in zip(*textArray)]

                self.append(''.join(tableDraw(columnWidth, textArray[0], textArray[1:])))
                self.callingWindow.statusBar().showMessage('Last Operation: SQL Query Entered')

           for i in self.myCur:
                self.append(f'{i}')
                

            
        except Exception as e:
            self.append(f'mysql> <font color = red>{e}</font>')
            self.callingWindow.statusBar().showMessage('Last Operation: SQL Query Entered (Error)')
