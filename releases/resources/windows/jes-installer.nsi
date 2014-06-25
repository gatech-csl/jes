#!Nsis Installer Command Script
#
# This is an NSIS Installer Command Script, which was originally
# generated automatically by the Fedora nsiswrapper program,
# and subsequently modified.  For more information see:
#
#   http://fedoraproject.org/wiki/MinGW
#
# Additional fragments were obtained from:
#
#   http://nsis.sourceforge.net/A_simple_installer_with_start_menu_shortcut_and_uninstaller
#
# To build an installer from the script you would normally do:
#
#   makensis jes-installer.nsi
#
# which will generate the output file 'jes-@version@-windows.exe'.

!addplugindir ..\..\resources\windows\nsis-plugins
!addincludedir ..\..\resources\windows\nsis-plugins

!include MUI2.nsh
!include zipdll.nsh

!define APPNAME "JES"
!define APPFULLNAME "JES - Jython Environment for Students"
!define APPVERSION "@version@"
!define APPGUID "{AE72B60E-47B2-46FE-AC9E-0436A26DAD7D}"
!define PUBLISHERNAME "Georgia Institute of Technology"

!define REQUIREDJAVA "1.5"

!define INSTALLSUBTITLE "JES: Jython Environment for Students (version @version@)"

!define UNINSTALLNAME "Uninstall JES"
!define UNINSTALLREGKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPGUID}"

Name "${APPNAME}"
OutFile "jes-@version@-windows.exe"

RequestExecutionLevel admin

InstallDir "$ProgramFiles\JES"
InstallDirRegKey HKLM "Software\JES" "InstallDir"

ShowInstDetails hide
ShowUninstDetails hide

Var TotalInstalledSize


# Modern UI Interface Settings

!define MUI_ABORTWARNING
!define MUI_ICON "jes/images/jesicon.ico"


# Modern UI Pages

!define MUI_WELCOMEPAGE_TITLE "JES: Jython Environment for Students"
!define MUI_WELCOMEPAGE_TEXT "This program will install JES version @version@ on your computer. It won't take long; just follow the instructions."
!insertmacro MUI_PAGE_WELCOME

!define MUI_PAGE_HEADER_TEXT "License"
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_LICENSEPAGE_TEXT_TOP "JES is Free Software, released under the GNU General Public License."
!define MUI_LICENSEPAGE_TEXT_BOTTOM "This means that everyone may use JES, free of charge, and share it with anyone. Everyone can also make changes to JES and share those changes."
!insertmacro MUI_PAGE_LICENSE "JESCopyright.txt"

!define MUI_PAGE_HEADER_TEXT "Installation Options"
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_COMPONENTSPAGE_TEXT_TOP "This lets you customize how JES is installed. (The defaults are usually fine.)"
!define MUI_COMPONENTSPAGE_TEXT_COMPLIST "Select options:"
!insertmacro MUI_PAGE_COMPONENTS

!define MUI_PAGE_HEADER_TEXT "Select Install Location"
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_DIRECTORYPAGE_TEXT_TOP "Where would you like to install JES? (The default is usually fine.)"
!insertmacro MUI_PAGE_DIRECTORY

!define MUI_PAGE_HEADER_TEXT "Installing..."
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_INSTFILESPAGE_FINISHHEADER_TEXT "Installation complete!"
!define MUI_INSTFILESPAGE_FINISHHEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_INSTFILESPAGE_ABORTHEADER_TEXT "Installation stopped..."
!define MUI_INSTFILESPAGE_ABORTHEADER_SUBTEXT "${INSTALLSUBTITLE}"
!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_TITLE "JES installation complete"
!define MUI_FINISHPAGE_TEXT "Now you can write your own programs for working with media! Have fun!"
!define MUI_FINISHPAGE_RUN "$INSTDIR\JES.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Run JES now"
!define MUI_FINISHPAGE_NOREBOOTSUPPORT
!define MUI_FINISHPAGE_BUTTON "Finish"
!insertmacro MUI_PAGE_FINISH


!define MUI_PAGE_HEADER_TEXT "Uninstall JES?"
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_UNCONFIRMPAGE_TEXT_TOP "This program will remove JES from your computer. Any programs you wrote will remain, but you won't be able to run them."
!insertmacro MUI_UNPAGE_CONFIRM

!define MUI_PAGE_HEADER_TEXT "Uninstalling..."
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_UNINSTFILESPAGE_FINISHHEADER_TEXT "Uninstallation complete!"
!define MUI_UNINSTFILESPAGE_FINISHHEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_UNINSTFILESPAGE_ABORTHEADER_TEXT "Uninstallation stopped..."
!define MUI_UNINSTFILESPAGE_ABORTHEADER_SUBTEXT "${INSTALLSUBTITLE}"
!insertmacro MUI_UNPAGE_INSTFILES

!define MUI_FINISHPAGE_TITLE "JES uninstallation complete"
!define MUI_FINISHPAGE_NOREBOOTSUPPORT
!define MUI_FINISHPAGE_BUTTON "Finish"
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"


# Install Sections

Section -JES SecJES
  SectionIn RO

  SetOutPath "$INSTDIR\."
  File "JES.exe"
  File "jes.bat"
  File "JESCopyright.txt"

  File /r "jes"
  File /r "dependencies"
  File /r "demos"

  # Add an uninstaller
  WriteUninstaller "$INSTDIR\${UNINSTALLNAME}.exe"

  # Provide an entry in Add/Remove Programs
  WriteRegStr HKLM "${UNINSTALLREGKEY}" "DisplayName" "${APPFULLNAME}"
  WriteRegStr HKLM "${UNINSTALLREGKEY}" "DisplayVersion" "${APPVERSION}"
  WriteRegStr HKLM "${UNINSTALLREGKEY}" "Publisher" "${PUBLISHERNAME}"
  WriteRegStr HKLM "${UNINSTALLREGKEY}" "DisplayIcon" "$\"$INSTDIR\JES.exe$\""

  WriteRegStr HKLM "${UNINSTALLREGKEY}" "InstallLocation" "$\"$INSTDIR$\""
  WriteRegStr HKLM "${UNINSTALLREGKEY}" "UninstallString" "$\"$INSTDIR\${UNINSTALLNAME}.exe$\""
  WriteRegStr HKLM "${UNINSTALLREGKEY}" "QuietUninstallString" "$\"$INSTDIR\${UNINSTALLNAME}.exe$\" /S"

  # We don't have "Modify" or "Repair" options for A/R Programs
  WriteRegDWORD HKLM "${UNINSTALLREGKEY}" "NoModify" 1
  WriteRegDWORD HKLM "${UNINSTALLREGKEY}" "NoRepair" 1

  # This is what the size is for
  Call ComputeTotalInstalledSize
  WriteRegDWORD HKLM "${UNINSTALLREGKEY}" "EstimatedSize" $TotalInstalledSize
SectionEnd

Section "Java Runtime Environment" SecJRE
  ; When I computed this, the JRE was 44764K zipped and 126759K unzipped
  AddSize 81815

  ; We keep the JRE in a ZIP file because it's really huge
  ; (Even the ZIP file is 45 MB, unpacked it's like 120 MB)
  GetTempFileName $3
  File /oname=$3 "..\..\resources\windows\jre-win32-1.7.0_60.zip"
  !insertmacro ZIPDLL_EXTRACT "$3" "$INSTDIR\dependencies\jre-win32" "<ALL>"
  Delete $3
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
  CreateDirectory "$SMPROGRAMS\JES"
  CreateShortCut "$SMPROGRAMS\JES\${UNINSTALLNAME}.lnk" "$INSTDIR\${UNINSTALLNAME}.exe" "" "$INSTDIR\${UNINSTALLNAME}.exe" 0
  CreateShortCut "$SMPROGRAMS\JES\JES.lnk" "$INSTDIR\.\JES.exe" "" "$INSTDIR\.\JES.exe" 0
SectionEnd

Section "Desktop Icon" SecDesktop
  CreateShortCut "$DESKTOP\JES.lnk" "$INSTDIR\.\JES.exe" "" "$INSTDIR\.\JES.exe" 0
SectionEnd


# Section descriptions

LangString DESC_JRE ${LANG_ENGLISH} "This installs a Java Runtime Environment for JES to use. If you don't have a JRE installed already, the installer will select this for you."

LangString DESC_StartMenu ${LANG_ENGLISH} "This will add a shortcut to JES (and its uninstaller) in the Start Menu."

LangString DESC_Desktop ${LANG_ENGLISH} "This will place a JES icon on your Desktop, so you can launch it quickly."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecJRE} $(DESC_JRE)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_StartMenu)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_Desktop)
!insertmacro MUI_FUNCTION_DESCRIPTION_END


# Uninstall Sections

Section "Uninstall" UnsecJES
  Delete "$DESKTOP\JES.lnk"
  RMDir /r "$SMPROGRAMS\JES"

  RMDir /r "$INSTDIR\jes"
  RMDir /r "$INSTDIR\dependencies"
  RMDir /r "$INSTDIR\demos"

  Delete "$INSTDIR\JESCopyright.txt"
  Delete "$INSTDIR\jes.bat"
  Delete "$INSTDIR\JES.exe"

  Delete "$INSTDIR\${UNINSTALLNAME}.exe"

  RMDir "$INSTDIR"

  # Remove the uninstaller registry key
  DeleteRegKey HKLM "${UNINSTALLREGKEY}"
SectionEnd


# Java version detector

Function .onInit
  Push "${REQUIREDJAVA}"
  Call DetectJava
  Pop $0    # The return value from DetectJava

  StrCmp $0 "!" RequireJRE
  StrCmp $0 "<" RequireJRE
  Goto DontRequireJRE

  RequireJRE:
    # MessageBox MB_OK "We have not found a JRE. You are required to install one. :-/"
    !insertmacro SetSectionFlag ${SecJRE} ${SF_SELECTED}
    !insertmacro SetSectionFlag ${SecJRE} ${SF_RO}
    Return

  DontRequireJRE:
    # MessageBox MB_OK "We have found a JRE in $0 for JES to use."
    !insertmacro ClearSectionFlag ${SecJRE} ${SF_SELECTED}
    Return
FunctionEnd


Function DetectJava
  # NSIS wiki: New installer with JRE check ...
  # Stack input: Requested JRE version
  # Stack output: Java home if Java found,
  # "<" if Java is old, "!" if Java does not exist

  Exch $0   # Save the current $0
            # $0: Requested JRE version (input from stack)
  Push $1   # $1: Found Java version
  Push $2   # $2: Found JAVA_HOME
  Push $3   # $3: Requested major/minor version
  Push $4   # $4: Found major/minor version

  #DetectJavaJRE:
    # See if the version is in the Registry
    ReadRegStr $1 HKLM "SOFTWARE\JavaSoft\Java Runtime Environment" "CurrentVersion"
    StrCmp $1 "" DetectJavaJDK
    # Now get the JAVA_HOME
    ReadRegStr $2 HKLM "SOFTWARE\JavaSoft\Java Runtime Environment\$1" "JavaHome"
    StrCmp $2 "" DetectJavaJDK
    # See if there's a java EXE there
    IfFileExists "$2\bin\java.exe" 0 DetectJavaJDK
    # Sweet, check its version
    Goto DetectJavaCheckVersion

  DetectJavaJDK:
    # See if the version is in the Registry
    ReadRegStr $1 HKLM "SOFTWARE\JavaSoft\Java Development Kit" "CurrentVersion"
    StrCmp $1 "" DetectJavaNone
    # Now get the JAVA_HOME
    ReadRegStr $2 HKLM "SOFTWARE\JavaSoft\Java Development Kit\$1" "JavaHome"
    StrCmp $2 "" DetectJavaNone
    # See if there's a java EXE there
    IfFileExists "$2\bin\java.exe" 0 DetectJavaNone
    # Sweet, check its version
    Goto DetectJavaCheckVersion

  DetectJavaCheckVersion:
    # Compare the major versions
    StrCpy $3 $0 1    # Copy character 0 of the requested JRE version to $3
    StrCpy $4 $1 1    # Copy character 0 of the found JRE version to $4
    IntCmp $4 $3 0 DetectJavaOld DetectJavaNew
    
    # Compare the minor versions
    StrCpy $3 $0 1 2  # Copy character 2 of the requested JRE version to $3
    StrCpy $4 $1 1 2  # Copy character 2 of the found JRE version to $4
    IntCmp $4 $3 DetectJavaNew DetectJavaOld DetectJavaNew

  DetectJavaNew:
    Push $2
    Goto DetectJavaEnd

  DetectJavaOld:
    Push "<"
    Goto DetectJavaEnd

  DetectJavaNone:
    Push "!"
    Goto DetectJavaEnd

  DetectJavaEnd:
    # The return value is on top of the stack.
    # The Exch instructions move it to the second position on the stack
    # before we pop each of the registers.
    Exch
    Pop $4
    Exch
    Pop $3
    Exch
    Pop $2
    Exch
    Pop $1
    Exch
    Pop $0
FunctionEnd


Function ComputeTotalInstalledSize
  # NSIS wiki: Add uninstall information to Add/Remove Programs
  Push $0
  Push $1

  StrCpy $TotalInstalledSize 0
  
  ${ForEach} $1 0 256 + 1
    ${if} ${SectionIsSelected} $1
      SectionGetSize $1 $0
      IntOp $TotalInstalledSize $TotalInstalledSize + $0
    ${Endif}
    
    ${if} ${errors}
      ${break}
    ${Endif}
  ${Next}
  ClearErrors

  Pop $1
  Pop $0
  Return
FunctionEnd
