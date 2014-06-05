#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines
#See JESCopyright.txt for full licensing information
#This class, Copyright 2003  Adam Wilson, Yu Cheung Ho, Larry Olson, Eric Mickley
# 5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import smtplib
import JESConstants
import JESAddressFinder
import JESURLFinder
import JESTurninTypeFinder
import MimeWriter
import base64
import quopri
import StringIO
import mimetypes
import httplib
import os
import string
import java.io as io
import java.net as net
import urlparse
import java.lang.System as system


####################################################################
####################################################################
# Class: JESHomeworkSubmission
# Parameters:
#     -hwTitle: The title of the homework being turned in
#     -fileName: The name of the .py file the homework is in
#     -zipFile: The local path to the zip archive of the homework
# Description:
#     Holds and provides functionality for homeworks.  Holds & sends  
#     a zip file with all the submission materials.  Lets the user 
#     turnin the submission via the preferred method (email or coweb
#     posting).
####################################################################
class JESHomeworkSubmission:
    def __init__(self, hwTitle, fileName, zipFile):
#       config = self.readFromConfigFile()
        self.studentName =  JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_NAME)
        self.gtNumber = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_GT)
        self.mailServer = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MAIL)
        self.studentEmail = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_EMAIL_ADDR)
        self.cowebPort = 80
        self.hwTitle = hwTitle
        self.fileName = fileName
        self.zipFile = zipFile



####################################################################
# Method: turnin
# Description
#     Decides which method(s) to use to turnin the homework.  Looks
#     At the constants file EMAIL_TURNIN sends the hw as an email to 
#     The TA's email address.  COWEB_TURNIN posts the hw zip file to 
#     a coweb page.  The turnin information and definitions should
#     be on a web page defined in JESConstants.
####################################################################
    def turnin(self):
        emailError = 0
        cowebError = 0
        doEmail = 0
        doCoWeb = 0
        turninType = ''

        
        #USE Turnin Type Table check
        if(JESConstants.TURNIN_TYPE_TABLE):
            try:
                turnTypeFinder = JESTurninTypeFinder.JESTurninTypeFinder(string.strip(self.hwTitle))
                turninType = turnTypeFinder.getTurninType()
            except Exception:
                import sys
                a,b,c=sys.exc_info()
                print a,b,c
                
            if( turninType == 'EMAIL' or turninType == 'BOTH'):
                doEmail = 1
            if( turninType == 'COWEB' or turninType == 'BOTH'):
                doCoWeb = 1
        else:
            if JESConstants.EMAIL_TURNIN:
                doEmail = 1
            if JESConstants.COWEB_TURNIN:
                doCoWeb = 1
        
        try:
            if doEmail:
                self.emailTurnin()
        except Exception:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            emailError = 1
        try:
            if doCoWeb:
                self.cowebTurnin()
        except Exception:
            cowebError = 1

        if emailError and cowebError:
            raise StandardError, "Error emailing and uploading submission."
        elif emailError:
            raise StandardError, "Error emailing submission."
        elif cowebError:
            raise StandardError, "Error uploading submission to coweb."


####################################################################
# Method: emailTurnin
# Description:
#     Constructs an email message for the turnin.  Attaches the zip
#     file of the homework as a base64 encoded attachment.  Finally,
#     it sends the email through the defined SMTP server.
####################################################################
    def emailTurnin(self):
        #Get email information
        try:
            addr = JESAddressFinder.JESAddressFinder()
            taEmail = addr.getTargetAddress(self.gtNumber, self.hwTitle)
            if(taEmail == None):
                raise StandardError, "Could not find an e-mail to send assignment."
                return            
            
            filehandle = open(self.zipFile,"rb")
           #CONSTRUCT EMAIL
           #Build the email from all the parts of information:
            subject = "%s : %s : %s : %s" % \
                      (self.hwTitle, self.studentName, self.gtNumber, self.fileName)  
            msgBody = 'From: %s\n' % self.studentEmail
            msgBody += 'Subject: %s\n' % subject
            file = StringIO.StringIO()
            mime = MimeWriter.MimeWriter(file)
            mime.addheader("Mime-Version","1.0")
            mime.startmultipartbody("mixed")
            part=mime.nextpart()
            part.addheader("Content-Transfer-Encoding","quoted-printable")
            part.startbody("text/plain")
            quopri.encode(StringIO.StringIO("An Assignment Submission from "+self.studentName),file,0)
            quopri.encode(StringIO.StringIO("Notes to TA: "),file,0)
            #quopri.encode(StringIO.StringIO(notes),file,0)
            part = mime.nextpart()
            part.addheader("Content-Transfer-Encoding","base64")
            part.startbody('application/x-zip-compressed; name='+self.zipFile) 
            base64.encode(filehandle, file)
            mime.lastpart()
            msgBody += file.getvalue()
            filehandle.close()
           #END CONSTRUCT EMAIL
            #SEND EMAIL:
            servObj = smtplib.SMTP(self.mailServer)
            servObj.sendmail(self.studentEmail, taEmail, msgBody)
        except:
            print "Student E-mail: " + self.studentEmail + "\n"
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            raise StandardError, "Error emailing assignment."




####################################################################
# Method: cowebTurnin
# Description:
#     Constructs a zip file with the assignment submission materials
#     inside.  It then posts it to the coweb page defined in the
#     turnin definitions via the .attach script.
####################################################################
    def cowebTurnin(self):
        try:
            filehandle = open(self.zipFile,"rb")
            url = net.URL(JESConstants.HW_COWEB_ADDRESS_URL)
            host = url.getHost()
            port = url.getPort()
            finder = JESURLFinder.JESURLFinder()
            turninURL = finder.getTargetURL(self.gtNumber, string.strip(self.hwTitle))
            if(turninURL == -1): # check if url is not found - RJC
                raise StandardError, "Unable to find a valid upload url for assignment."           
            
            selector = string.strip(turninURL[turninURL.find("/"):]) + JESConstants.HW_COWEB_ATTACH_SUFFIX
            fields = [['specific', 'true'], ['reference', 'true']]
            files = [['filestuff', os.path.basename(self.zipFile), filehandle.read()]]
            response = self.post_multipart(host, port, selector, fields, files)
            if response.status < 200 or response.status > 399:
                system.out.println("Server resonded with unsuccessful message")
                raise StandardError
            return response
        except:
            import sys
            a,b,c = sys.exc_info()
            print a,b,c
            raise StandardError, "Error turning in to the Coweb."

################################################################################
# Function name: readFromConfigFile
# Parameters: self
# Description: Attempts to open the Configfile.  If it exists, it is opened and
#       read into an array.  Each line of the file will get its spot in the array
#       and newline characters will be removed.  The array is returned.  The 
#       configfile should exist before this function is called.  If an IO Error 
#       occurs, a message will be printed to the transcript. 
#
################################################################################
    def readFromConfigFile(self):
        try:
            homedir=os.path.expanduser("~")
            f=open(homedir+io.File.separator+JESConstants.JES_CONFIG_FILE_NAME,'r')
            text=f.read()
            f.close()
            array=text.splitlines()
            return array
        except:
            raise StandardError, "Error reading configuration file."

#All of the following code is:
#Written by: Wade Leftwich
#Date: 8/23/2002
#URL: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
    def post_multipart(self, host, port, selector, fields, files):
        #Post fields and files to an http host as multipart/form-data.
        #fields is a sequence of (name, value) elements for regular form fields.
        #files is a sequence of (name, filename, value) elements for data to be uploaded as files
        #Return the server's response page.
        array = self.encode_multipart_formdata(fields, files)
        h = httplib.HTTPConnection(host, port)
        h.putrequest('POST', selector)
        h.putheader('content-type', array[0])
        h.putheader('content-length', str(len(array[1])))
        h.endheaders()
        h.send(array[1])
        response = h.getresponse()
        h.close()
        return response

    def encode_multipart_formdata(self, fields, files):
        #fields is a sequence of (name, value) elements for regular form fields.
        #files is a sequence of (name, filename, value) elements for data to be uploaded as files
        #Return (content_type, body) ready for httplib.HTTP instance
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return [content_type, body]

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

      
