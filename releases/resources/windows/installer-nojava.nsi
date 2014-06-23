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
#   makensis installer-nojava.nsi
#
# which will generate the output file 'jes-@version@-windows-nojava.exe'.

!include MUI2.nsh

!define APPNAME "JES"
!define APPFULLNAME "JES - Jython Environment for Students"
!define APPVERSION "@version@"
!define APPGUID "{AE72B60E-47B2-46FE-AC9E-0436A26DAD7D}"
!define PUBLISHERNAME "Georgia Institute of Technology"

!define INSTALLSUBTITLE "JES: Jython Environment for Students (version @version@)"

!define UNINSTALLNAME "Uninstall JES"
!define UNINSTALLREGKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPGUID}"

# The size in KB of everything copied into Program Files.
# This is a super-estimate.
!define INSTALLSIZE 28332

Name "${APPNAME}"
OutFile "jes-@version@-windows-nojava.exe"

RequestExecutionLevel admin

InstallDir "$ProgramFiles\JES"
InstallDirRegKey HKLM "Software\JES" "InstallDir"

ShowInstDetails hide
ShowUninstDetails hide


# Modern UI Interface Settings

!define MUI_ABORTWARNING
!define MUI_ICON "jes/images/jesicon.ico"
!define MUI_COMPONENTSPAGE_NODESC


# Modern UI Pages

!define MUI_WELCOMEPAGE_TITLE "JES: Jython Environment for Students"
!define MUI_WELCOMEPAGE_TEXT "This program will install JES version @version@ on your computer. This version of JES requires a Java Runtime Environment, so ensure that you have one installed before continuing. Everything else JES needs is included, though."
!insertmacro MUI_PAGE_WELCOME

!define MUI_PAGE_HEADER_TEXT "License"
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_LICENSEPAGE_TEXT_TOP "JES is Free Software, released under the GNU General Public License."
!define MUI_LICENSEPAGE_TEXT_BOTTOM "This means that everyone may use JES, free of charge, and share it with anyone. Everyone can also make changes to JES and share those changes."
!insertmacro MUI_PAGE_LICENSE "JESCopyright.txt"

!define MUI_PAGE_HEADER_TEXT "Select Shortcuts"
!define MUI_PAGE_HEADER_SUBTEXT "${INSTALLSUBTITLE}"
!define MUI_COMPONENTSPAGE_TEXT_TOP "Where would you like to have shortcuts to JES?"
!define MUI_COMPONENTSPAGE_TEXT_COMPLIST "Select locations:"
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

Section -JES
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
  WriteRegDWORD HKLM "${UNINSTALLREGKEY}" "EstimatedSize" ${INSTALLSIZE}
SectionEnd

Section "Start Menu Shortcuts"
  CreateDirectory "$SMPROGRAMS\JES"
  CreateShortCut "$SMPROGRAMS\JES\${UNINSTALLNAME}.lnk" "$INSTDIR\${UNINSTALLNAME}.exe" "" "$INSTDIR\${UNINSTALLNAME}.exe" 0
  CreateShortCut "$SMPROGRAMS\JES\JES.lnk" "$INSTDIR\.\JES.exe" "" "$INSTDIR\.\JES.exe" 0
SectionEnd

Section "Desktop Icons"
  CreateShortCut "$DESKTOP\JES.lnk" "$INSTDIR\.\JES.exe" "" "$INSTDIR\.\JES.exe" 0
SectionEnd


# Uninstall Sections

Section "Uninstall"
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
