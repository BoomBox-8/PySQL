'''themes
A file that constructs themes, so to speak. In reality a constructor
function generates palettes with colors for various color roles
passed in as arguments

Extraneous color roles that don't affect the widgets in any
measurable way are left unchanged'''

from PyQt5.QtGui import  QPalette, QColor, QImage, QBrush
def createPalette(palette, base, window, text, button):
    '''Modifies some color roles of a QPalette object and returns the
       QPalette object
       
        Parameters
        ----------
        palette : QPalette
            A QPalette object to be operated on
        base : str
            Color provided in hex for the background
        window : str
            Color provided in hex for the window
        text : str
            Color provided in hex for the the text
        button : str
            Color provided in hex for various buttons
        
        Returns
        -------
        QPalette'''

    palette.setColor(QPalette.Base, QColor(base))
    palette.setColor(QPalette.Window, QColor(window))
    palette.setColor(QPalette.Text, QColor(text))
    palette.setColor(QPalette.Button, QColor(button))
    palette.setColor(QPalette.WindowText, QColor(text))
    palette.setColor(QPalette.Highlight, QColor(text))
    palette.setColor(QPalette.ButtonText, QColor(text))

    return palette


cottonCandy  = createPalette(QPalette(), '#FF131425','#FF1B1D36','#FFFCA6D1','#FFFCA6D1')
mango = createPalette(QPalette(), '#FF1E1E1E', '#FF313131', '#FFFFC800','#FFFFFFFF')
raspberry = createPalette(QPalette(), '#FF1E1E1E', '#FF313131', '#FFE30B5C','#FFFFFFFF')
lime = createPalette(QPalette(), '#FF1E1E1E', '#FF313131', '#FFBFFF00','#FFFFFFFF')
ocean = createPalette(QPalette(), '#FF090922', '#FF0E0F38', '#FF25B497', '#FFFFFFFF')
ube = createPalette(QPalette(), '#FF2A273F', '#FF3E3A5D', '#FFBCB4F6', '#FFBCB4F6')




themesDict = {
    'Cotton Candy' : cottonCandy, 'Mango Twist' : mango, 'Raspberry' : raspberry, 
    'QT Lime Pie' : lime, 'Ocean' : ocean, 'Ube' : ube
    }

#To add a new theme, set up a new pallete object,
#and add a key-value pair of the form themeName-paletteObj to themesDict

#window = 
#wconsole/textedit : 
#text : 