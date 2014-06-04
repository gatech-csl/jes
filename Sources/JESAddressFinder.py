#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines
#See JESCopyright.txt for full licensing information

import java.io as io
import string
import httplib
import java.net as net
import JESConstants

class JESAddressFinder:
    def __init__(self):
        self.splitarray=[]
        self.targetGt=None
        self.targetHw=None
        self.targetMail=None
        self.data=self.grabFile()
    
    def getTargetAddress(self,gt,hw):
        self.targetGt=string.strip(gt)
        self.targetHw=string.strip(hw)
        self.parseDataFile(self.data)
        return self.findAddress()

    def grabFile(self):
        try:
            url = net.URL(JESConstants.HW_ADDRESS_URL)
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
        except:
            import sys
            a,b,c = sys.exc_info()
            print a,b,c
            print "Error in JESAddressFinder.grabFile, could not get target mail address for submission"
            return None

    def parseDataFile(self,text):
        #Get the TA assignments:        
        beg = text.find("#BEGIN")
        end = text.find("#END")
        if (beg == -1) or (end == -1):
            return 0
        text = text[beg+6:end]
        self.splitarray=[]
        array=text.split("\n")
        for x in array:
            self.splitarray.append(x.split("|"))

  
    def findAddress(self):
        try:
            for x in self.splitarray:
                if string.strip(x[0]) == self.targetGt:
                    if string.strip(x[1]) == self.targetHw:
                        return string.strip(x[2])
        except:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            print "Error in JESAddressFinder.findAddress"
