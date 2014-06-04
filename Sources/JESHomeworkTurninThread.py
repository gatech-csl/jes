import java.lang.Thread
import JESHomeworkTurninRunnable
import javax.swing as swing
import os
import java.lang.System as System

class JESHomeworkTurninThread( java.lang.Thread):
    def __init__(self,homeworkSub,gui,zipName):
        self.gui = gui
        self.homeworkSub = homeworkSub
        self.zipName=zipName

    def run(self):
        # in the main thread, call:
        # j = JESHomeworkTurninThread()
        # then:
        # j.start()
        # Java will create a seperate thread.  That thread will
        # call this method's run method
        
        # do stuff here
        try:

            update = JESHomeworkTurninRunnable.JESHomeworkTurninRunnable('Submitting Assignment ....',self.gui)
            self.gui.swing.SwingUtilities.invokeLater( update )            
            self.homeworkSub.turnin()
            update = JESHomeworkTurninRunnable.JESHomeworkTurninRunnable('Done',self.gui)
            self.gui.swing.SwingUtilities.invokeLater( update )

            import user
            if System.getProperty('os.name').find('Mac') <> -1:
                DIRECTORY = user.home
            else:
                DIRECTORY = os.getcwd()

            MESSAGE="""The assignment has been submitted. A file named 
%s was created in the submission.
This file is an archive containing all of the files that 
you just submitted.  JES can delete the file for you, 
or JES can leave the file alone. If you choose to keep
the file, it will be located at %s. 
Would you like JES to delete %s for you? """%(self.zipName,DIRECTORY,self.zipName)

            options = ["Delete the File","Leave the File"]
            n = swing.JOptionPane.showOptionDialog(self.gui,
                     MESSAGE,
                     "Assignment Submission has completed",
                     swing.JOptionPane.YES_NO_OPTION,
                     swing.JOptionPane.QUESTION_MESSAGE,
                     None,     #don't use a custom Icon
                     options,  #the titles of buttons
                     options[0]) #default button title
            if n == 0:
                try:                
                    os.remove(self.zipName)
                except:
                    import sys
                    a,b,c=sys.exc_info()
                    print a,b,c
        except Exception, target:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            update = JESHomeworkTurninRunnable.JESHomeworkTurninRunnable('Exception',self.gui)
            self.gui.swing.SwingUtilities.invokeLater( update )
