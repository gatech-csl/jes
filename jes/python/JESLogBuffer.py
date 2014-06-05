#JES- Jython Environment for Students
#Copyright (C) 2004 Aron Giles, Ryan Connelly, Adam Poncz, Patrick Carnahan

import sys
import java
import java.lang.System as System
import java.util.Date as Date
import java.lang.StringBuffer as StringBuffer
import org.python.core


# workaround to support java 1.5 jython bug
if sys.registry.getProperty('java.version') >= '1.5.0':
    for n,f in java.lang.AbstractStringBuilder.__dict__.items():
        x = org.python.core.PyReflectedFunction(n)
        for a in f.argslist:
            if a is None: continue
            m = StringBuffer.getMethod(n,a.args)
            x.addMethod(m)
        StringBuffer.__dict__[n] = x


class JESLogBuffer:

################################################################################
# Function name: __init__
# Return:
#     An instance of the JESLogBuffer class.
# Description:
#     Creates a new instance of the JESLogBuffer.
################################################################################
    def __init__(self, program):
        self.saveBoolean = (1 == 1);
	self.CurrentBuffer=StringBuffer();
        self.CurrentBuffer.append("<file_created time=\"");
        self.CurrentBuffer.append((Date(System.currentTimeMillis())).toString());
        self.CurrentBuffer.append("\">\n");
        
################################################################################
# Function name: resetBuffer
# Parameters:
#           None.
# Description:
#     This function clears the log buffer.
################################################################################
    def resetBuffer(self):
        self.CurrentBuffer=StringBuffer();
        self.CurrentBuffer.append("<file_created time=\"");
        self.CurrentBuffer.append((Date(System.currentTimeMillis())).toString());
        self.CurrentBuffer.append("\">\n");

################################################################################
# Function name: addCommand
# Parameters:
#           newString: the command that is to be added into the log
# Description:
#     This function adds a command into the log file
################################################################################
    def addCommand(self, newString):
        self.CurrentBuffer.append("<command_run time=\"");
        self.CurrentBuffer.append((Date(System.currentTimeMillis())).toString());
        self.CurrentBuffer.append("\">");
        self.CurrentBuffer.append(newString);
	self.CurrentBuffer.setCharAt(self.CurrentBuffer.length()-1, '>');
        self.CurrentBuffer.append("</command_run>\n");

################################################################################
# Function name: addMenuOption
# Parameters:
#           newString: the name of the menu option to be added to the log
# Description:
#     This function adds a menu option into the log
################################################################################
    def addMenuOption(self, newString):
        self.CurrentBuffer.append("<menu_button time=\"");
        self.CurrentBuffer.append((Date(System.currentTimeMillis())).toString());
        self.CurrentBuffer.append("\">");
        self.CurrentBuffer.append(newString);
        self.CurrentBuffer.append("</menu_button>\n");

################################################################################
# Function name: openLogFile
# Parameters:
#           fileName: the file name to open
# Description:
#     This function clears the log buffer and replaces it with the logfile that
# is in the filename specified.
################################################################################

    def openLogFile(self, fileName):
	self.CurrentBuffer= StringBuffer();
	try:
	    file=open(fileName+"log", "rt");
	    self.CurrentBuffer.append(file.read());
            if self.CurrentBuffer.length()>16:
                self.CurrentBuffer=StringBuffer(self.CurrentBuffer.substring(0,
                                                     self.CurrentBuffer.length()-16));
	    self.CurrentBuffer.append("<file_opened time=\"");
            self.CurrentBuffer.append((Date(System.currentTimeMillis())).toString());
            self.CurrentBuffer.append("\">");
	    self.CurrentBuffer.append(fileName);
	    self.CurrentBuffer.append("</file_opened>");
	    self.CurrentBuffer.append("\n");
	except:
            self.resetBuffer();
	    self.CurrentBuffer.append("<Could not find "+fileName+ "log,");
	    self.CurrentBuffer.append(" creating a new logfile>\n");

################################################################################
# Function name: saveLogFile
# Parameters:
#           fileName: the filename to save to
# Description:
#     This function dumps the log buffer into the specified file
################################################################################

    def saveLogFile(self, fileName):
        if self.saveBoolean==(1==0):
            return;
	logfile=open(fileName+"log", "wt");
	self.CurrentBuffer.append("<file_saved time=\"");
    	self.CurrentBuffer.append((Date(System.currentTimeMillis())).toString());
        self.CurrentBuffer.append("\">");
	self.CurrentBuffer.append(fileName);
	self.CurrentBuffer.append("</file_saved>");
	self.CurrentBuffer.append("\n");
        self.CurrentBuffer.append("</file_created>\n");
	logfile.write(self.CurrentBuffer.toString());
	logfile.close();

################################################################################
# Function name: dumpLogToTerm
# Parameters:
#           None.
# Description:
#     This funcion dumps the log buffer to the terminal. Intended for debugging
# use primarily.
################################################################################

    def dumpLogToTerm(self):
        System.out.println(self.CurrentBuffer.toString());
        

