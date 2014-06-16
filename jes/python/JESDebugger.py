import sys
import cmd
import bdb
import pdb
import threading
import linecache
import time
import math
import JESDBVariableWatcher
from java.lang import Thread
from java.lang import Long
from java.lang import Runnable
import javax.swing as swing


SPEED_FACTOR = 20.0


class JESDebugger(pdb.Pdb):

    def __init__(self, interpreter):
        pdb.Pdb.__init__(self)
        self.running = 0
        self.speed = int(2 * SPEED_FACTOR)
        self.speed_factor = SPEED_FACTOR
        self.MAX_SPEED = int(3 * SPEED_FACTOR)
        self.text_mode = 0
        self.last_time = -1

        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

        #self.history = JESExecHistoryModel()
        self.watcher = JESDBVariableWatcher.JESDBVariableWatcher(self)
        self.history = self.watcher.history

        self.controlPanel = self.watcher.controlPanel
        self.interpreter = interpreter
        self.cmd = None

    def setSpeed(self, speed):
        self.speed = speed
        # notify control panel
        self.controlPanel.refreshSlider()

    def endExecution(self):
        self.watcher.endExecution()
        self.controlPanel.stop()  # this sets the button states

    def runCommand(self, cmd):
        self.cmd = cmd
        self.lock.acquire()
        self.cond.notifyAll()
        self.lock.release()

    # Overrides pdb.interaction
    def interaction(self, frame, traceback):
        # print "JESDebugger, interaction: " + Thread.currentThread().getName()
        if self.text_mode:
            cmd = ''
            stop = 0
            self.print_frame(frame)
            while not stop:
                self.setup(frame, traceback)
                self.interpreter.jesThread.threadCleanup()
                self.lock.acquire()
                self.cond.wait()     # wait for the program to signal
                self.lock.release()
                self.interpreter.jesThread.initialize()
                stop = self.onecmd(self.cmd)
        else:
            # if we're not in stop mode then we're in...
            # unique to JESDB...the running debug mode!!
            self.setup(frame, traceback)
            self.handle_each_step(frame)

    # Chose an intentionally obtuse name to minimize the likelihood of
    # name conflicts with Pdb.
    def handle_each_step(self, frame):
        actual_filename = frame.f_code.co_filename
        target_filename = self.interpreter.program.filename

        if actual_filename == target_filename:
            lineno = frame.f_lineno
            filename = self.interpreter.program.filename
            line = linecache.getline(filename, lineno)

            values = []
            for var in self.history.getVars():
                try:
                    value = eval(
                        var, self.curframe.f_locals, self.curframe.f_globals)
                    values.append(value)
                except:
                    values.append('-')  # add dummy

            # Append the row to the table.
            runnableSnapshot = snapShotRunner()
            runnableSnapshot.history = self.history
            runnableSnapshot.lineno = lineno
            runnableSnapshot.line = line
            runnableSnapshot.values = values
            swing.SwingUtilities.invokeLater(runnableSnapshot)

            if self.speed < self.MAX_SPEED:
                if self.speed == 0:
                    self.lock.acquire()
                    self.cond.wait()
                    self.lock.release()
                    pass
                else:
                    period = SPEED_FACTOR / self.speed
                    time.sleep(period)


    # Overrides pdb.user_line
    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        self.interaction(frame, None)

    # Overrides pdb.user_return
    def user_return(self, frame, return_value):
        pass

    # Overrides pdb.user_return
    def user_exception(self, frame, (exc_type, exc_value, exc_traceback)):
        pass

    # Overrides pdb.user_call
    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self._wait_for_mainpyfile:
            return
        if self.stop_here(frame):
            # Only overridden just to remove this line:
            #print >>self.stdout, '--Call--'
            self.interaction(frame, None)

    def run(self, cmd, globals=None, locals=None):
        self.running = 0
        self.clearHistory()
        self.controlPanel.run()
        self.last_time = time.time()
        # print "debug run: " +  Thread.currentThread().getName()
        pdb.Pdb.run(self, cmd, globals, locals)
        self.running = 0

    def runeval(self, cmd, globals=None, locals=None):
        self.running = 0
        self.clearHistory()
        self.controlPanel.run()
        self.last_time = time.time()
        pdb.Pdb.runeval(self, cmd, globals, locals)
        self.running = 0

    def stopThread(self):
        self.running = 0
        # self.step()
        self.interpreter.jesThread.stop()

    def step(self):
        self.lock.acquire()
        self.cond.notifyAll()
        self.lock.release()

    def clearHistory(self):
        clearHist = clearRunner()
        clearHist.history = self.history
        swing.SwingUtilities.invokeLater(clearHist)


class snapShotRunner(Runnable):
    history = None
    lineno = 0
    line = None
    values = None

    def run(self):
        self.history.addLine(self.lineno, self.line, self.values)


class clearRunner(Runnable):
    history = None

    def run(self):
        self.history.clear()
