set java="win-jre\bin\java.exe"
set classpath=".\jars\jython.jar;.\jars\jmf.jar;.\jars\jl1.0.jar;.\jars\junit.jar;.\Sources"

echo maybe we should pop up a readme file if the program has not been run before
echo %java% -Dpython.home="jython-2.2.1" -classpath %classpath% org.python.util.jython .\Sources\JESProgram.py

