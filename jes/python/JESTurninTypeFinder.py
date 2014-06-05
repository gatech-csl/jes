#JES- Jython Environment for Students
#See JESCopyright.txt for full licensing information
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines
#This class, Copyright 2004  Ryan Connelly, Patrick Carnahan, Aron Giles, Adam Poncz


import java.io as io
import string
import httplib
import java.net as net
import JESConstants

##################################################################
# Class: JESURLFinder
# Description:
#     A Class for JES which connects to a Web server to find out
#     turnin information.  Supplies student's GT number and 
#     assignment name to find the appropraiate turnin URL and turnin type.
##################################################################
class JESTurninTypeFinder:
    def __init__(self, hw):
        self.turninTypeData = []
        self.hw = ''
        self.hw = hw
        self.text = self.grabFile()




##################################################################
# Method: parseDataFile
# Description:
#     Takes a plain text version of the web page, and reads the
#     various definitions sections.  It puts the gt number ta
#     information for assignments into an array called self.turninData.
# pre:
#     Valid file must be downloaded 
##################################################################
    def parseDataFile(self):
	try:
            #Get the assignment turnin information
	    beg = self.text.find("#BEGIN_TURNIN_TYPE_TABLE")
	    end = self.text.find("#END_TURNIN_TYPE_TABLE")
	    if (beg == -1) or (end == -1):
	    	return 0
	    talist = self.text[beg:end]
	    talist = talist.split("\n")
            self.turninTypeData = []
	    for entry in talist:
	        self.turninTypeData.append(entry.split("|")) # add a 2 element list to array
            return 1
        
	except:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
	    raise StandardError, "Error parsing data file. Most likely an invalid parse "
        
##################################################################
# Method: getTurninType
# Description:
#     gets the turnin type d
# pre:
#     turnin table has been downloaded, parsed, and stored in an
#     array with the followign format.
#     <homework type> | <turnin type>\n
#
#     Returns EMAIL or COWEB (or -1 on failure)
#
##################################################################
    def getTurninType(self):
        if(self.parseDataFile() == 0):
            return -1        
	try:
            for element in self.turninTypeData:
                if string.strip(element[0]) == string.strip(self.hw):
                    return string.strip(element[1]) # return the type            
	    raise StandardError, "Could not find valid turnin type."
	except:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
	    raise StandardError, "Error parsing turnin URL list"

##################################################################
#
##################################################################
    def grabFile(self):
        try:
            url = net.URL(JESConstants.HW_TABLE_LINK)
            if url.getPort() != -1:
                h = httplib.HTTP(url.getHost(), url.getPort())
            else:
                h = httplib.HTTP(url.getHost())
            h.putrequest('GET', url.getFile())
            h.putheader('Accept', 'text/html')
            h.putheader('Accept', 'text/plain')
            h.endheaders()
            errcode, errmsg, headers = h.getreply()
            f = h.getfile()
            data = f.read() # Get the raw HTML
            f.close()
            return data
        except Exception:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            print "Error in JESAddressFinder.grabFile, could not get target mail address for submission"
            return None
