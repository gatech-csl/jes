@echo off
setlocal EnableDelayedExpansion

rem Launches JES in place on Windows.
rem This will keep a Command Prompt window open,
rem so it's suitable for debugging weird issues.
rem JES.exe just launches this file without the Command Prompt,
rem so end users should use that file.

rem Where are we?

set jes_base=%~dp0
set jes_base=%jes_base:~0,-1%
set jes_home=%jes_base%\jes


rem Is there a user configuration file?

if EXIST "%APPDATA%\JES\JESEnvironment.bat" (
    call "%APPDATA%\JES\JESEnvironment.bat"
)


rem What Java should we use?

set java_exe=java.exe

set "java_bundled=%jes_base%\dependencies\jre-win32"

if DEFINED JES_JAVA_HOME (
    set "java=%JES_JAVA_HOME%\bin\%java_exe%"
) else (
    if EXIST "%java_bundled%" (
        set "java=%java_bundled%\bin\%java_exe%"
    ) else (
        if DEFINED JAVA_HOME (
            set "java=%JAVA_HOME%\bin\%java_exe%"
        ) else (
            set "java=%java_exe%"
        )
    )
)


rem Where's our Java code?

set jars=%jes_base%\dependencies\jars

set classpath=%jes_home%\classes.jar

for %%J IN ("%jars%\*.jar") DO set classpath=!classpath!;%%~fJ


rem Where's our Python code?

set pythonhome=%jes_base%\dependencies\jython

set pythonpath=%jes_home%\python;%jes_base%\dependencies\python


rem Do we have any plugins to load?
rem User plugins:

set jes_user_plugins=%APPDATA%\JES\Plugins

if NOT EXIST "%jes_user_plugins%" GOTO :nouserplugins
for %%J IN ("%jes_user_plugins%\*.jar") DO set "classpath=!classpath!;%%~fJ"
:nouserplugins

rem System plugins:

set jes_system_plugins=%jes_base%\plugins

if NOT EXIST "%jes_system_plugins%" GOTO :nosystemplugins
for %%J IN ("%jes_system_plugins%\*.jar") DO set "classpath=!classpath!;%%~fJ"
:nosystemplugins

rem Built-in plugins:

set jes_builtin_plugins=%jes_home%\builtin-plugins

if NOT EXIST "%jes_builtin_plugins%" GOTO :nobuiltinplugins
for %%J IN ("%jes_builtin_plugins%\*.jar") DO SET "classpath=!classpath!,%%~fJ"
:nobuiltinplugins


rem Where should the Jython cache live?

set pythoncache=%LOCALAPPDATA%\JES\jython-cache

if NOT EXIST "%pythoncache%" (
    md "%pythoncache%"
)


rem What about JESConfig.properties?

set jesconfig=%APPDATA%\JES\JESConfig.properties

if NOT EXIST "%APPDATA%\JES" (
    md "%APPDATA%\JES"
)


rem All right, time to actually run it!

if NOT DEFINED JES_JAVA_MEMORY (
    set JES_JAVA_MEMORY=-Xmx512m
)

"%java%" -classpath "%classpath%" ^
    -Dfile.encoding="UTF-8" ^
    -Djes.home="%jes_home%" ^
    -Djes.configfile="%jesconfig%" ^
    -Djes.plugins.user="%jes_user_plugins%" ^
    -Djes.plugins.system="%jes_system_plugins%" ^
    -Djes.plugins.builtin="%jes_builtin_plugins%" ^
    -Dpython.home="%pythonhome%" ^
    -Dpython.path="%pythonpath%" ^
    -Dpython.cachedir="%pythoncache%" ^
    %JES_JAVA_MEMORY% %JES_JAVA_OPTIONS% ^
    JESstartup %*

