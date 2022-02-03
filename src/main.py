'''main
The main file of the PySQL project. The file is intended to be run to
to use the application

The file in of itself contains little in the way of the various
functions, classes and algorithm that make this project possible.
Much of the heavy lifting is done by the importing of the other
program files included with this file

It is preferred if the user has the Fira Code Medium font installed,
as opposed to the default monospace fonts found on most systems
The Open Sans font is also recommended to be installed'''

import signinWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication


def main():
    '''Instantiates QApplication and runs the event loop
    
    Parameters
    ----------
    
    Returns
    -------
    None'''

    app = QApplication([])
    app.setWindowIcon(QIcon(r'assets\logoBlack.ico'))
    app.setStyle("fusion")
    signIn = signinWindow.SignIn()

    signIn.show()
    app.exec()


main()
