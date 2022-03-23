'''signinWindow
Contains the initial sign-in screen. Successfully logging in results
in connecting to said database, which is passed over to the appWindow
constructor to be used to execute MySQL queries'''

from enum import auto
import mysql.connector
import appwindow
from os import path
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QBrush
from PyQt5.QtWidgets import (

    qApp,
    QLabel,
    QLineEdit,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)


class SignIn(QMainWindow):
    '''Inherits from QMainWindow
    The SignIn window class prompts the user to enter their
    details to be authenticated. Contains two text entry fields
    among several other widgets
       
    Attributes
    ----------
    bg : QPixmap
        An image to be used as the background of the window palette
    enter : ClickableQLabel
        A button that authenticates the provided details
    fail : ClickableQLabel
        A button that is displayed upon the authentication failing
    nameEntry : QLineEdit
        A text entry field that takes in the user name
    passwordEntry : QLineEdit
        A text entry field that takes in the password'''

    def __init__(self):
        super().__init__()
        
        f = QFont('Open Sans', 14)
        self.setFont(f)
        self.setWindowTitle('Sign In')
        self.setMinimumSize(QSize(640,480))
        
        self.bg = QPixmap(f'{path.dirname(path.abspath(__file__))}/assets/icons/signinbg.png')
        self.pallete = self.palette()
        self.brush = QBrush()
        self.brush.setTexture(self.bg)
        self.pallete.setBrush(QPalette.Window, self.brush) #Add a fancy bg image
        
        self.setPalette(self.pallete)
        
        widgContainer = QWidget()
        screenGridLayout = QGridLayout()
        namePassLayout = QVBoxLayout() #contains name & pass entry
        
        
        cancelButton = ClickableQLabel('< Cancel', lambda: qApp.exit(), hlColor = QColor('#FFE30B5C'))
        
        heading = ClickableQLabel('Sign In', lambda: None)
        heading.setFixedSize(260, 100)
        heading.setFont(QFont('Open Sans', 40))
        
        self.enter = Authenticate(self)
        self.enter.transferObj.connect(self.launchappwindow) #launch mainwindow with cur and db objects
        
        
        name = QLabel()
        name.setScaledContents(True)
        name.setFixedSize(QSize(128,128))
        name.setPixmap(QPixmap(f'{path.dirname(path.abspath(__file__))}/assets/icons/alternativeLogo.png'))
 
        #fit logo within the label
        
        self.fail = ClickableQLabel('Details not correct, please enter again', lambda: None, textColor = QColor('#FFFF0000'), hlColor = QColor('#FFFF0000') )
        self.fail.setFixedSize(QSize(360,30))
        self.fail.setVisible(False) #should only become visible post the entry of wrong details
        
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText('Enter Name: ')
        self.setProperties(self.nameEntry)
        
        
        
        self.passwordEntry = QLineEdit()
        self.passwordEntry.setPlaceholderText('Enter Password: ')
        self.passwordEntry.setEchoMode(QLineEdit.Password)
        self.passwordEntry.keyPressEvent = self.keyPressWrapper(self.passwordEntry)
        self.setProperties(self.passwordEntry)

        self.autoFill = ClickableQLabel('Auto-Fill Credentials', pressFunc = lambda: extractCredentials(self),  hlColor = QColor('#FFE30B5C'))
        self.autoFill.setFixedSize(QSize(320,100))
        self.autoFill.setVisible(path.exists(f'{path.dirname(path.abspath(__file__))}/credentials.txt'))


        namePassLayout.addWidget(heading)
        namePassLayout.addWidget(self.nameEntry)
        namePassLayout.addWidget(self.passwordEntry)
        namePassLayout.addWidget(self.enter)
        namePassLayout.addWidget(self.autoFill)
        namePassLayout.addWidget(self.fail)
        
        namePassLayout.setAlignment(self.nameEntry, Qt.AlignHCenter)
        namePassLayout.setAlignment(self.passwordEntry, Qt.AlignHCenter)
        namePassLayout.setAlignment(heading, Qt.AlignHCenter)
        namePassLayout.setAlignment(self.enter, Qt.AlignHCenter)
        namePassLayout.setAlignment(self.autoFill, Qt.AlignHCenter)
        namePassLayout.setAlignment(self.fail, Qt.AlignHCenter)
        
        
        namePassLayout.insertSpacing(5,800)
        namePassLayout.insertSpacing(1, 400)
        namePassLayout.insertSpacing(0,200)
        namePassLayout.setSpacing(40)
        
        screenGridLayout.addLayout(namePassLayout,1,2)
        screenGridLayout.addWidget(cancelButton, 0, 0)
        screenGridLayout.addWidget(name, 10, 10)
        screenGridLayout.setHorizontalSpacing(0)
        widgContainer.setLayout(screenGridLayout)
        
        self.setCentralWidget(widgContainer)
        
        
    def launchappwindow(self, content : tuple) -> None:
        '''Launches appwindow and passes the cur and db objects
        
        Parameters
        ----------
        content : tuple
        Contains the cursor and db objects
        
        Returns:
        None'''

        self.appwindow = appwindow.EditingWindow(content)
        self.appwindow.show()
        self.close()
        
    

    def setProperties(self, obj : QLineEdit) -> None:
        '''Mutates properties of the object obj
        
        Parameters
        ----------
        obj : QLineEdit
        
        Returns:
        None'''

        obj.setFixedWidth(450)
        obj.setFixedHeight(35)
        obj.palette = obj.palette()
        obj.palette.setColor(QPalette.Highlight, QColor('#FF350a49'))
        obj.setPalette(obj.palette)


    def keyPressWrapper(self, obj : QLineEdit): #least astonishment? what's that?
        '''A decorator that overloads the keyPressEvent
        Adds in the ability to hit the enter button to authenticate
        
        Parameters
        ----------
        obj : QLineEdit
        
        Returns
        -------
        func'''

        def passKeyPress(e, obj = obj):

            e.accept()
            QLineEdit.keyPressEvent(obj,e)
            if e.key() == Qt.Key_Return:    
                self.enter.authenticate()

        return passKeyPress

    

       

class ClickableQLabel(QLabel):
    '''Inherits from QLabel.
    Adds extra functionality, like a function that is run upon a 
    click, or the text changing color upon hovering
    
    Attributes
    ----------
    textColor : QColor
        The color to which the text color is set to
    hlColor : QColor
        The color to which the text is set to upon hovering'''
    
    
    
    
    def __init__(self, text : str, pressFunc, textColor : QColor = QColor('#FFFFFFFF')  , hlColor : QColor = QColor('#FFFFFFFF') ):
        super().__init__(text)
        
        self.palette = self.palette()
        self.palette.setColor(QPalette.WindowText, textColor)
        self.setPalette(self.palette)
        self.textColor = textColor
        
        self.hlColor = hlColor
        self.pressFunc = pressFunc
        self.setMouseTracking(True) #The mouse is tracked even when it is not held down
        self.setFixedSize(QSize(160,60))
        self.setAlignment(Qt.AlignHCenter)
        
        
    def mousePressEvent(self, e) -> None:
        '''Overrides mousePressEvent
        Calls pressFunc

        Parameters
        ----------
        e : QEvent
        
        Returns
        -------
        None'''

        self.pressFunc()
        
        
    
    def enterEvent(self, e) -> None:
        '''Overrides enterEvent
        Sets the color of the text to hlColor upon the mouse
        entering the widget
        
        Parameters
        ----------
        e : QEvent
        
        Returns
        -------
        None'''

        e.accept()
        self.palette.setColor(QPalette.WindowText, self.hlColor)
        self.setPalette(self.palette)

    
    def leaveEvent(self, e) -> None:
        '''Overrides leaveEvent
        Sets the color of the text to textColor upon the mouse
        leaving the widget. Resets the color, so to speak
        
        Parameters
        ----------
        e : QEvent
        
        Returns
        -------
        None'''

        e.accept()
        self.palette.setColor(QPalette.WindowText, self.textColor)
        self.setPalette(self.palette)
        
    
    
        
class Authenticate(ClickableQLabel):
    '''Inherits from ClickableQLabel
    Authenticates the provided details and connects to the database
    if successful
    
    Attributes
    ----------
    window : SignIn
        Used to access values of text entry fields in window
    
    Methods
    -------
    transferObj : pyqtSignal
        A signal that can pass along a tuple of objects when emitted'''

    transferObj = pyqtSignal(tuple)
    
    
    def __init__(self, window):
        super().__init__('Authenticate', self.authenticate, hlColor = QColor('#FFE30B5C'))
        self.setFixedSize(QSize(300,60))
        self.window = window
        
   
    def authenticate(self):
        '''Passes the entered name and password
        (or reads from a credentials file if available), and validates them
        A failure causes the function to return, a success passes
        the db and cur objects in a tuple
        
        Parameters
        ----------
        
        Returns
        -------
        None'''
        
        try:
            
            myDb = mysql.connector.connect(host = 'localhost', user = self.window.nameEntry.text(), password = self.window.passwordEntry.text())
            myCur = myDb.cursor()
            
            
            
        except Exception: #if it cant connect with the provided details, the details must be wrong
            self.window.nameEntry.clear()
            self.window.passwordEntry.clear()
            self.window.fail.setVisible(True)
            
            return None #quit the func


        if not path.exists(f'{path.dirname(path.abspath(__file__))}/credentials.txt'):
            with open(f'{path.dirname(path.abspath(__file__))}/credentials.txt', 'w+') as credentials:
                credentials.write(f'name = {self.window.nameEntry.text()}{chr(10)}password = {self.window.passwordEntry.text()}') #set credentials to file
        self.transferObj.emit((myDb, myCur))
            
    
def extractCredentials(window):
    '''Extracts user credentials from a text file
    Extracts user credentials from a text file. If no file is
    available, create file upon the next successful login
    
    Parameters
    ----------
    window : SignIn
        Used to access values of text entry fields in window
        
    Returns
    -------
    None'''

    with open(f'{path.dirname(path.abspath(__file__))}/credentials.txt', 'r') as credentials:
        window.nameEntry.setText(credentials.readline().split(' = ')[1][:-1]) #newline gets included, must W I P E 
        window.passwordEntry.setText(credentials.readline().split(' = ')[1])
            
    