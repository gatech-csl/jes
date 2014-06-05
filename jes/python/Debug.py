
DEBUG_ON  = None
FILE_NAME = 'debugFile'
FILE_MODE = 'a'


import os


def writeln(msg):
    if ( msg[-1] != '\n' ):
        write( msg + '\n')
    else:
        write(msg)

def write(msg):
    if DEBUG_ON:
        file = open( FILE_NAME, FILE_MODE)
        if (msg[-1] != '\n'):
            file.write(msg + '\n')
        else:
            file.write(msg)
        file.close()
        
def clear():
    try:
        os.unlink(FILE_NAME)
    except:
        pass
