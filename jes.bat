@echo off
setlocal

rem Launches JES in place on Windows.

rem Where are we?
set jes_base=%~dp0
set jes_base=%jes_base:~0,-1%
set jes_home=%jes_base%\jes


rem What Java should we use?
if DEFINED JAVA_HOME (
    set java=%JAVA_HOME%\bin\java
) else (
    set java=java
)


rem Where's our Java code?
set jars=%jes_base%\dependencies\jars

set classpath=%jes_home%\classes

set classpath=%classpath%;%jars%\jython-2.5.3.jar
set classpath=%classpath%;%jars%\junit.jar
set classpath=%classpath%;%jars%\jmf.jar
set classpath=%classpath%;%jars%\jl1.0.jar
set classpath=%classpath%;%jars%\AVIDemo.jar


rem Where's our Python code?
set pythonhome=%jes_base%\dependencies\jython

set pythonpath=%jes_home%\python


rem Where should the Jython cache live?
set pythoncache=%LOCALAPPDATA%\JES\jython-cache

if NOT EXIST %pythoncache% (
    md %pythoncache%
)


rem What about JESConfig.txt?
set jesconfig=%APPDATA%\JES\JESConfig.txt

if NOT EXIST %APPDATA%\JES (
    md %APPDATA%\JES
)


rem All right, time to actually run it!

if NOT DEFINED JAVA_MEMORY (
    set JAVA_MEMORY=-Xmx512m
)

"%java%" -classpath %classpath% %JAVA_MEMORY% ^
    -Djes.home="%jes_home%" ^
    -Djes.configfile="%jesconfig%" ^
    -Dpython.home="%pythonhome%" ^
    -Dpython.path="%pythonpath%" ^
    -Dpython.cachedir="%pythoncache%" ^
    JESstartup %*
