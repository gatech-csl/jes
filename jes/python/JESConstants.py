# JES- Jython Environment for Students
# Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
# See JESCopyright.txt for full licensing information

import java.awt as awt

BEGINNER_MODE = 'Normal'
EXPERT_MODE = 'Expert'

LOW_FONT = 8
MID_FONT = 32
HIGH_FONT = 72


FONT_MODE_LOW = [LOW_FONT, MID_FONT, HIGH_FONT]
FONT_MODE_MID = [MID_FONT, LOW_FONT, HIGH_FONT]
FONT_MODE_HIGH = [HIGH_FONT, MID_FONT, LOW_FONT]

USER_MODES = [BEGINNER_MODE, EXPERT_MODE]
USER_MODES_2 = [EXPERT_MODE, BEGINNER_MODE]

TAB = '  '
APPLICATION_TITLE = 'JES - Jython Environment for Students - %s'
INITIAL_WINDOW_SIZE = (1000, 600)
KEYWORD_COLOR = awt.Color(50, 50, 150)
ENVIRONMENT_WORD_COLOR = awt.Color(150, 50, 150)
COMMENT_COLOR = awt.Color(50, 120, 50)
STRING_COLOR = awt.Color(150, 90, 90)
LPAREN_COLOR = awt.Color(150, 0, 0)
RPAREN_COLOR = awt.Color(150, 0, 0)
LOAD_BUTTON_DIFF_COLOR = awt.Color(200, 50, 50)
LOAD_BUTTON_SAME_COLOR = awt.Color(50, 200, 50)
FONT_SIZE = 12

JESPROGRAM_ERROR_LOADING_FILE = '\nThere was an error loading the file.  ' \
                                + 'It may not be present.  FILENAME: '
JESPROGRAM_NO_FILE = '\nNo file has been selected.\n' + \
                     'You must open a saved file, or save the opened file,\n' +\
                     'before clicking LOAD\n'

EDITOR_LOAD_WARNING = "WARNING: Current code has not been loaded.\n"
HELP_START_PAGE = 'http://coweb.cc.gatech.edu/mediaComp-teach/25'

