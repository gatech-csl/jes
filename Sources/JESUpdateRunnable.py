from java.lang import Runnable

class JESUpdateRunnable( Runnable ):

    def __init__(self,interpreter,text):
        self.interpreter = interpreter

        self.text = text

    def run(self):
        import sys

        self.interpreter.program.gui.commandWindow.printNowUpdate(self.text)
