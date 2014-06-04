#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import java.awt as awt

BEGINNER_MODE = 'Normal'
EXPERT_MODE = 'Expert'

MAIL_SERVER = 'smtp.mail.gatech.edu'
WEB_DEFINITIONS = '127.0.0.1:8080/Test/7'

JESHELP = 'JESHelp/JESHelp'
LOW_FONT = 8
MID_FONT = 32
HIGH_FONT = 72


# AUTOOPENDOC is an option that's been removed, but for compatability for 
# folks who may be using earlier beta versions, it retains a slot.
CONFIG_NAME = 0
CONFIG_GT = 1
CONFIG_MAIL = 2
CONFIG_MODE = 3
CONFIG_FONT = 4
CONFIG_EMAIL_ADDR = 5
CONFIG_GUTTER = 6
CONFIG_BLOCK = 7
CONFIG_WEB_TURNIN = 8
CONFIG_AUTOSAVEONRUN = 9
CONFIG_AUTOOPENDOC = 10
CONFIG_WRAPPIXELVALUES = 11
CONFIG_SKIN = 12
CONFIG_SHOWTURNIN = 13
CONFIG_BACKUPSAVE = 14
CONFIG_LOGBUFFER = 15
CONFIG_MEDIAPATH = 16
CONFIG_NLINES = 17


FONT_MODE_LOW = [ LOW_FONT, MID_FONT, HIGH_FONT]
FONT_MODE_MID = [ MID_FONT, LOW_FONT, HIGH_FONT]
FONT_MODE_HIGH = [ HIGH_FONT, MID_FONT, LOW_FONT]

USER_MODES = [ BEGINNER_MODE, EXPERT_MODE ]
USER_MODES_2 = [ EXPERT_MODE, BEGINNER_MODE ]

TO_ADDR = 'csltestaccount@yahoo.com'

# The turnin types for the class.  You can turn the methods on and off by
# assigning 1 for on, and 0 for off.
EMAIL_TURNIN = 0
COWEB_TURNIN = 0

# Using the CoWeb Table - automatically assigns turnin type per assignment basis
# Ignores EMAIL_TURNIN and COWEB_TURNIN constants
TURNIN_TYPE_TABLE = 1
# This URL should be a link to the table containg file turnin types for EACH
# assignment.
HW_TABLE_LINK = 'http://coweb.cc.gatech.edu/mediaComp-plan/109'

# This URL should be a link TO the table containing the URL for the email HW
# submission information.  The file should be of the following format:
# Any stuff here will be ignored by the parser
# #BEGIN
# studentGT#|HW#|TARGET_MAIL_ADDRESS
# #END
# Anything here or after will also be thrown away by the parser
# Important, HW# must exactly match a HW# from the ASSIGNMENT_URL or the 
# program will not know where to turn the file in to.  Also, the target email
# must be complete and exact.
#HW_ADDRESS_URL = 'http://coweb.cc.gatech.edu/mediaComp-plan/33'
HW_ADDRESS_URL = 'http://coweb.cc.gatech.edu/mediaComp-plan/111'# DEBUG

# This URL will contain the file which contains the list of possible assignments
# that the student will be able to turn in.  It will look like:
# Stuff here gets ignored
# #BEGIN
# HW#|HW#|HW#
# #END
# Stuff here gets ignored
#ASSIGNMENT_URL='http://coweb.cc.gatech.edu/mediaComp-plan/32'
ASSIGNMENT_URL='http://coweb.cc.gatech.edu/mediaComp-plan/112'# DEBUG

#This URL will contain the file which contains the Web turnin
#Address definitions.  It should look like this:
# #BEGIN_TA_ASSIGNMENTS
# STUDENT_GT_NUM|TA_GT_NUM
# ...
# #END_TA_ASSIGNMENTS
# #BEGIN_TURNIN_LOCATIONS
# TA_GT_NUM|ASSIGNMENT_NAME|TARGET_COWEB_ADDRESS
# ...
# #END_TURNIN_LOCATIONS
#HW_COWEB_ADDRESS_URL = 'http://coweb.cc.gatech.edu:8080/mediaComp-plan/81'
HW_COWEB_ADDRESS_URL = 'http://coweb.cc.gatech.edu:8080/mediaComp-plan/113'# DEBUG
HW_COWEB_PORT = 8080
HW_COWEB_ATTACH_SUFFIX = '.attach'

COWEB_HOST = 'coweb.cc.gatech.edu:8080'
BUG_COWEB_ADDRESS = '/mediaComp-plan/124.append'

TAB = '  '
APPLICATION_TITLE = 'JES - Jython Environment for Students - %s'
INITIAL_WINDOW_SIZE = (1000, 600)
KEYWORD_COLOR = awt.Color(50, 50, 150)
ENVIRONMENT_WORD_COLOR = awt.Color(150,50,150)
COMMENT_COLOR = awt.Color(50, 120, 50)
STRING_COLOR = awt.Color(150, 90, 90)
LPAREN_COLOR = awt.Color(150, 0, 0)
RPAREN_COLOR = awt.Color(150, 0, 0)
LOAD_BUTTON_DIFF_COLOR = awt.Color(200, 50, 50)
LOAD_BUTTON_SAME_COLOR = awt.Color(50, 200, 50)
FONT_SIZE = 12

COMMAND_FROM_CONSOLE = '<input>'
STACK_MSG = ' in file %s, on line %d, in function %s\n'
NAME_OF_EXC_MSG = 'The error "%s" had occurred\n'
LINE_NUM_MSG = 'Please check line %d of %s\n'

PRE_PROCESSING_FILE = 'JESPreprocessing.py'
# SHOW_VARS_FILTER_FILE = 'JESShowVarsFilter.py'
NO_PRE_PROCESSING_FILE_ERR_MSG = '\nThe file ' + PRE_PROCESSING_FILE + \
                                 ' could not be loaded.  You program '\
                                 ' will not run until this is addressed.\n'
JESPROGRAM_ERROR_LOADING_FILE = '\nThere was an error loading the file.  ' \
                                + 'It may not be present.  FILENAME: '
JESPROGRAM_NO_FILE = '\nNo file has been selected.\n' + \
                     'You must open a saved file, or save the opened file,\n' +\
                     'before clicking LOAD\n'
JES_CONFIG_FILE_NAME= "JESConfig.txt"
JES_API_HELP_FILE = "JESAPIHelp.html"
EDITOR_LOAD_WARNING = "WARNING: Current code has not been loaded.\n"
HELP_START_PAGE = 'http://coweb.cc.gatech.edu/mediaComp-teach/25'

# The EXCEPTION_MESSAGES array contains a list of user-friendly exceptions
# messages.  Messages can also contain values that will be replaced by JES
# before displaying the message.  These values can be any attribute of the
# exception type that is being raised.
# For example, the RuntimeError exception has an attribute called 'lineno'; if
# the RuntimeError message contained '%(lineno)s', then that text would be
# replaced with the actual value of the lineno attribute.
# Example message:  "Runtime error occurred on line '%(lineno)s'"
EXCEPTION_MESSAGES = {
    'AssertionError'       : 'An "assert" statement has failed.',
    'AttributeError'       : 'You are trying to access a part of the object that doesn\'t exist.',
    'EOFError'             : 'The build-in read function failed because the end  of the file has been reached. This happens when you leave a statement or function unfinished or do not match up all of your parentheses.',
    'FloatingPointError'   : 'A floating point operation has failed.',
    'IOError'              : 'I tried to read a file, and couldn\'t.  Are you sure that file exists? If it does exist, did you specify the correct directory/folder?',     
    'ImportError'          : 'An import statement failed to find the module that was defined. You need to find the correct name of the module you want to use.',
    'IndexError'           : 'The index you\'re using goes beyond the size of that data (too low or high). For instance, maybe you tried to access OurArray[10] and OurArray only has 5 elements in it.',
    'IndentationError'     : 'A line of code contains bad indentation. Make sure all of your lines match up inside your functions.',
    'KeyError'             : 'Attempt to access a key that is not in a dictionary.',
    'KeyboardInterrupt'    : 'The user pressed the interrupt key.',
    'NameError'            : 'A local or global name could not be found. You need to define the function or variable before you try to use it in any way.',
    'NotImplementedError'  : 'A method that was called must be implemented in a sub-class. You need to define this method yourself before you use it, jython or JES will not do it for you.',
    'OSError'              : 'An error occurred while making an operating system call. Please tell a TA what you were doing when this happened, so we may correct it.',
    'OverflowError'        : 'An arithmetic result is outside the range of acceptable values. This means that the answer is either too large or too small to be represented.',
    'RuntimeError'         : 'I wasn\'t able to do what you wanted on line %(lineno)s',
    'StackOverflowError'   : 'You have overrun the stack. This means that way too many functions were called before they ever had a chance to return.',
    'SyntaxError'          : 'Your code contains at least one syntax error, meaning it is not legal jython. This error is located on %(lineno)s. Please correct it.',     
    'SystemError'          : 'An internal system error has occurred.  Please tell a TA what you were doing when this happened so that we may correct it. ',
    'SystemExit'           : 'A call of the sys.exit() function has been made. Normally this would exit JES entirely, but we don\'t want you doing this. If you want to exit JES, use the exit option in the file menu.',
    'TypeError'            : 'An attempt was made to call a function with a parameter of an invalid type. This means that you did something such as trying to pass a string to a method that is expecting an integer.', 
    'UnboundLocalError'    : 'A local name was used before it was created. You need to define the method or variable before you try to use it.',
    'UnicodeError'         : 'An error occurred while encoding or decoding Unicode characters.',
    'ValueError'           : 'An error occurred attempting to pass an argument to a function.',
    'WindowsError'         : 'An error occurred while making a Windows system call. Please let your TA know what you were doing when this happened, so we can fix it.',
    'ZeroDivisionError'    : 'You have attempted to divide a number by zero. In mathematics (and in computing), this gives an undefined result. JES cannot deal with this and you should never be attempting to do it.',
    'java.lang.ThreadDeath': 'The code has been stopped due to you hitting the stop button.',
    'TokenError'           : 'There is something wrong with the text of the file you had me try to load.\nYou may have not have as many closing parenthesis as opening parenthesis, or you may have tried to use a jython keyword (if, def, etc...) as a function. This cannot be done.'}

# Error messages that we can't actually catch:

#   'MemoryError'          : 'The system does not have enough memory to allocate an object.',

GENERIC_EXCEPTION_MESSAGE = 'I wasn\'t able to do what you wanted.\n'
TAB_ERROR_MESSAGE = "There was a spacing error in the program.\nIt might be from a previous line, but I think the error is in line "


