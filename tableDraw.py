'''tableDraw
A file that is intended to take in MySQL table data in the form of
tuples and draws them in the traditional ASCII tables as seen with
the CLI of MySQL'''

def boundaryDraw(columnWidth : tuple) -> str:
    '''Takes in an array that contains the max width per-column
    and draws a horizontal boundary that bounds the vertical portions
    of the table
    
    Parameters
    ----------
    columnWidth : tuple
        An array where element n represents the max width of column n
        + 2 whitespaces on either side as padding
        
    Returns
    -------
    str'''

    returnStr = '' #''.joining a list would've been fine, but principle of least astonishment at the end of the day
    for i in columnWidth[:-1]:
        returnStr += f'+{"-" * i}'
    returnStr += f'+{"-" * columnWidth[-1]}+{chr(10)}' #draws the last line with a new line at the end

    return returnStr


def headerDraw(columnWidth : tuple, headerArr : tuple):
    '''Draws the column names in a box with required padding
    
    Parameters
    ----------
    columnWidth : tuple
        An array where element n represents the max width of column n
        + 2 whitespaces on either side as padding
    headerArr : tuple
        A tuple containing column names
    
    Returns
    -------
    str'''
        
    returnStr = ''
    returnStr += boundaryDraw(columnWidth)
    returnStr += rowDraw(columnWidth, headerArr)
    returnStr += boundaryDraw(columnWidth)

    return returnStr


def rowDraw(columnWidth : tuple, rowArr : tuple) -> str:
    '''Draws row data in a box with required padding
    
    Parameters
    ----------
    columnWidth : tuple
        An array where element n represents the max width of column n
        + 2 whitespaces on either side as padding
    rowArr : tuple
        A tuple containing row data

    Returns
    -------
    str'''

    returnStr = ''
    for index, val in enumerate(columnWidth[:-1]):
        returnStr += f'|{rowArr[index]!s:^{val}}' #convert to str and center within the specified space
    returnStr += f'|{rowArr[-1]!s:^{columnWidth[-1]}}|{chr(10)}'

    return returnStr


def tableDraw(columnWidth : tuple, headerArr : tuple, rowArr : tuple) -> list:
    '''Draws the entire table in a box with required padding
    
    Parameters
    ----------
    columnWidth : tuple
        An array where element n represents the max width of column n
        + 2 whitespaces on either side as padding
    headerArr : tuple
        A tuple containing column names
    rowArr : tuple
        A tuple containing row data
        
    Returns
    -------
    list'''

    returnArr = []

    returnArr.append(headerDraw(columnWidth, headerArr)) #draw header
    for i in rowArr: #draws rest of the table
        returnArr.append(rowDraw(columnWidth, i))
    returnArr.append(boundaryDraw(columnWidth))

    return returnArr

