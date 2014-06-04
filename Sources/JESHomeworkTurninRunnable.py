import java.lang.Runnable
import javax.swing as swing
class JESHomeworkTurninRunnable( java.lang.Runnable ):
    def __init__(self,text,gui):
        self.text = text
        self.gui = gui

    def run(self):
        # the second thread will create this object.
        # it will be queued for execution in the main UI
        # thread.  When it gets executed, this method will be
        # called.
	if self.text == 'Done':
		self.gui.turninstatuswindow.dispose()
        elif self.text == 'Exception':
                self.gui.turninstatuswindow.dispose()
                a="An unexpected error has occurred in the turnin process.\n"
                b="It is likely that the program turnin has failed.  Please \n"
                c="check JES's settings and resubmit the assignment."
                self.errorWindow=swing.JFrame()
                swing.JOptionPane.showMessageDialog(self.gui,
                                        a+b+c,
                                        "Error - Turnin has failed",
                                         swing.JOptionPane.WARNING_MESSAGE)
	else:
		self.gui.turninstatuslabel.setText(self.text)

