#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import javax.swing as swing
import java
import java.lang as lang

ACTIVATED = swing.event.HyperlinkEvent.EventType.ACTIVATED
ENTERED = swing.event.HyperlinkEvent.EventType.ENTERED
EXITED = swing.event.HyperlinkEvent.EventType.EXITED
DEFAULT_HELP_LINK = "http://www.jython.org"

class Html_Browser(swing.JPanel):#swing.JFrame):
################################################################################
# Function name: __init__
# Parameters:
#     -urlString: urlString to open in the browser
# Return:
#     An instance of the Html_Browser class.
# Description:
#     Creates a new instance of the Html_Browser.
################################################################################
    def __init__(self, urlString = DEFAULT_HELP_LINK):
        self.urlList=[urlString]
        self.curUrl=0
        self.endURL=0
#        swing.JFrame.__init__(self, title="JESHelp Browser", size=(800, 600))
        swing.JPanel.__init__(self)
        self.setLayout(java.awt.BorderLayout())
        self.add(self.buildTopPane(urlString), java.awt.BorderLayout.NORTH)
        # don't init this with a URL
        self.htmlPane = swing.JEditorPane('text/html', 'Welcome to JES',#urlString,
                                          editable=0,
                hyperlinkUpdate=self.followHyperlink, size=(lang.Short.MAX_VALUE,lang.Short.MAX_VALUE))
        self.add(swing.JScrollPane(self.htmlPane, size=(lang.Short.MAX_VALUE,lang.Short.MAX_VALUE)),
                 java.awt.BorderLayout.CENTER)
        self.status = swing.JLabel(" ", preferredSize=(200,20))
        self.add(self.status, java.awt.BorderLayout.SOUTH)
        self.back.enabled=0
        self.forward.enabled=0
################################################################################
# Function name: buildTopPane
# Parameters:
#     -startUrl: Will build the top pane of the web browser
# Return: JPane
#
# Description:
#       Builds the top pane.
################################################################################
    def buildTopPane(self, startUrl):
        label = swing.JLabel("Go To:")
        self.field = swing.JTextField(preferredSize=(200,20),
                text=startUrl, actionPerformed=self.goToUrl)
        go = swing.JButton("Go", size=(40,100), 
                actionPerformed=self.goToUrl)
        self.back = swing.JButton("Back", size=(60,100), 
                actionPerformed=self.goBack)
        self.forward = swing.JButton("Forward", size=(60,100), 
                actionPerformed=self.goForward)
        topPane = swing.JPanel()
        topPane.add(self.back)
        topPane.add(self.forward)
        topPane.add(label)
        topPane.add(self.field)
        topPane.add(go)
        return topPane

################################################################################
# Function name: goToUrl
# Parameters:
#     -event:
# Description: 
#        Sets the page displayed by the browser to the new page.
################################################################################
    def goToUrl(self, event):
        self.urlList.append(self.field.text)
        self.curUrl+=1
        self.htmlPane.setPage(self.field.text)
        #print self.curUrl, len(self.urlList)
        self.enableButtons()

################################################################################
# Function name: goBack
# Parameters:
#     -event:
# Description: 
#        Sets the page displayed by the browser to the previous page.
################################################################################
    def goBack(self, event):
        if self.curUrl > 0:
            self.curUrl -= 1
            self.htmlPane.setPage(self.urlList[self.curUrl])
            self.field.text=self.urlList[self.curUrl]
            self.enableButtons()

################################################################################
# Function name: goForward
# Parameters:
#     -event:
# Description: 
#        Sets the page displayed by the browser to the new page.
################################################################################
    def goForward(self, event):
        if self.curUrl < (len(self.urlList)-1):
            self.curUrl += 1
            self.htmlPane.setPage(self.urlList[self.curUrl])
            self.field.text=self.urlList[self.curUrl]
            self.enableButtons()
            

################################################################################
# Function name: followHyperlink
# Parameters:
#     -hlEvent:
# Description: Sends the web browser to Hyper Links when the user clicks on them
#
################################################################################
    def followHyperlink(self, hlEvent):
        try:
            if hlEvent.eventType == ACTIVATED:
                self.htmlPane.setPage(hlEvent.URL)
                self.field.text = hlEvent.URL.toString()
                if len(self.urlList) > self.curUrl+1:
                    self.urlList= self.urlList[0:self.curUrl+1]
                self.urlList.append(self.field.text)
                self.curUrl+=1
                self.enableButtons()
            elif hlEvent.eventType == ENTERED:
                self.status.text = hlEvent.URL.toString()
            elif hlEvent.eventType == EXITED:
                self.status.text = " "
        except:
            pass


    def enableButtons(self):
        if self.curUrl > 0:
            self.back.enabled=1
        else:
            self.back.enabled=0
        if self.curUrl+1 < len(self.urlList):
            self.forward.enabled=1
        else:
            self.forward.enabled=0
