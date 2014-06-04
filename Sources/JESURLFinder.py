#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines
#See JESCopyright.txt for full licensing information
#This class, Copyright 2003  Adam Wilson, Yu Cheung Ho, Larry Olson, Eric Mickley

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
#     assignment name to find the appropraiate turnin URL.
##################################################################
class JESURLFinder:
    def __init__(self):
	self.splitarray = []
	self.studentGT = ''
	self.hw = ''
	self.taGT = ''
	self.targetAddress = ''
	self.text = self.grabFile()
	self.gtData = []
	self.addressData = []

##################################################################
# Method: getTargetURL
# Parameters:
#     -gt The student's GT number as a string
#     -hw The Homework assigment name as a string
# Description:
#     Reads the downloaded turnin descriptions and decides where
#     the turnin URL is for this particular student and assignment
##################################################################
    def getTargetURL(self, gt, hw):
	self.studentGT = string.strip(gt)
	self.hw =  string.strip(hw)
        if self.parseDataFile() == 0:
	    raise StandardError, "Error parsing Turnin Definitions"
	self.taGT = self.getTaGT()
	self.targetAddress = self.getURL()
	return self.targetAddress

##################################################################
# Method: getTaGT
# Description:
#     Looks at the downloaded definitions tables to find the gt
#     number of the student's TA.  Returns the TA's gt num.
##################################################################
    def getTaGT(self):
	try:
	    for element in self.gtData:
		if string.strip(element[0]) == string.strip(self.studentGT):
		    return string.strip(element[1])
	    return -1
	except:
	    raise StandardError, "Error parsing TA list"

##################################################################
# Method: getURL
# Description:
#     Looks at the downloaded turnin definitions to find the URL
#     of submission for the assignment.  Returns the selector part
#     of the URL ideally (Depends on what's in the turnin 
#     definitions).
##################################################################
    def getURL(self):
        print "Student number:" + self.taGT
        print "assignment: " + self.hw 
        
	try:
	    for element in self.addressData:
		if string.strip(element[0]) == string.strip(self.taGT):
		    if string.strip(element[1]) == string.strip(self.hw):
			return string.strip(element[2])
	    return -1
	except:
	    raise StandardError, "Error parsing turnin URL list"

##################################################################
# Method: grabFile
# Description:
#     Goes to the server and URL listed in the JESConstants to get
#     tunrin and TA information.  Downloads the turnin definitions
#     page and returns it.
##################################################################
    def grabFile(self):
	try:
            url = net.URL(JESConstants.HW_COWEB_ADDRESS_URL)
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
            h.close()
            return data
        except:
	    raise StandardError,("Error: Could not get target web address for submission\n" + \
				 "Make sure you are connected to the internet.")

##################################################################
# Method: parseDataFile
# Description:
#     Takes a plain text version of the web page, and reads the
#     various definitions sections.  It puts the gt number ta
#     assignments as an array in self.gtData, and the assignment
#     turnin URLs in self.addressData.
##################################################################
    def parseDataFile(self):
	try:
	    #Get the TA assignments:        
	    beg = self.text.find("#BEGIN_TA_ASSIGNMENTS")
	    end = self.text.find("#END_TA_ASSIGNMENTS")
	    if (beg == -1) or (end == -1):
	    	return 0
	    talist = self.text[beg:end]
	    talist = talist.split("\n")
	    self.gtData =  []
	    for entry in talist:
	        self.gtData.append(entry.split("|"))
	
	    #Get the Turnin Locations
	    beg = self.text.find("#BEGIN_TURNIN_LOCATIONS")
	    end = self.text.find("#END_TURNIN_LOCATIONS")
	    if (beg == -1) or (end == -1):
	        return 0

	    loclist = self.text[beg:end]
	    loclist = loclist.split("\n")
	    self.addressData = []
	    for entry in loclist:
	        self.addressData.append(entry.split("|"))
	    return 1
	except:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
	    raise StandardError, "Error parsing data file."
