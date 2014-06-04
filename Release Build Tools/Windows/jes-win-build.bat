@echo off

rem This batch script will create a distributable version of JES from 
rem the local SVN project workspace.  The destination directory can be
rem compressed and distributed as the Windows no-java and Linux versions.
rem Created by: Brian Dorn (10-5-09)



if "%1" == "" goto ERROR
if "%2" == "" goto ERROR

if exist %2 goto ERROR2

if not exist make.exclude goto ERROR3

rem ---Ensure that the dest path ends with a backslash---
set destpath=%~2
set endchar=%destpath:~-1%  
if not  %endchar% == \  set destpath=%destpath%\

ECHO Copying Files....

xcopy %1 "%destpath%" /e /EXCLUDE:make.exclude

ECHO Compiling Java Classes...

set WD=%CD%
cd %2\Sources
CALL jesCompile.bat

cd %WD%

ECHO Build of JES Complete!
ECHO.
ECHO The target directory may now be compressed and distributed as the "no-java" version of JES for both Windows and Linux.

goto END

:ERROR
echo ERROR! Please provide two arguments to jes-win-build.bat.  The first argument is the path to the jes subdirectory of your local svn workspace.  The second argument should be the destination path where you'd like the build copy to be placed.  For example:

echo.

echo    [path]\jes-win-build.bat c:\mediacomp-jes\jes c:\jes-4-3-nojava
goto END

:ERROR2
echo ERROR! Destination directory already exists.  Please delete %2 and try again or specify a new destination directory.
goto END

:ERROR3
echo ERROR! This script must be executed from the directory containing the file make.exclude.  Please check your working directory and try again.
goto END

:END
