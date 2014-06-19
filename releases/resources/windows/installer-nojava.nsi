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

!define APPNAME "JES"
!define APPFULLNAME "JES - Jython Environment for Students"
!define APPVERSION "@version@"
!define PUBLISHERNAME "Georgia Institute of Technology"

!define UNINSTALLNAME "Uninstall JES"
!define UNINSTALLREGKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

# The size in KB of everything copied into Program Files.
# This is a super-estimate.
!define INSTALLSIZE 28332

Name "${APPNAME}"
OutFile "jes-@version@-windows-nojava.exe"

InstallDir "$ProgramFiles\JES"
InstallDirRegKey HKLM "Software\JES" "InstallDir"

ShowInstDetails hide
ShowUninstDetails hide

XPStyle on

Page license
Page directory
Page components
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

LicenseData "JESCopyright.txt"

ComponentText "Where would you like to have shortcuts to JES?"

DirText "Please select the installation folder."

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


Section "Uninstall"
  Delete "$DESKTOP\JES.lnk"
  Delete "$SMPROGRAMS\JES\JES.lnk"
  Delete "$SMPROGRAMS\JES\${UNINSTALLNAME}.lnk"
  RMDir "$SMPROGRAMS\JES"

  RMDir /r "$INSTDIR\.\jes"
  RMDir /r "$INSTDIR\.\dependencies"
  RMDir /r "$INSTDIR\.\demos"

  Delete "$INSTDIR\.\JESCopyright.txt"
  Delete "$INSTDIR\.\jes.bat"
  Delete "$INSTDIR\.\JES.exe"

  Delete "$INSTDIR\${UNINSTALLNAME}.exe"

  RMDir "$INSTDIR"

  # Remove the uninstaller registry key
  DeleteRegKey HKLM "${UNINSTALLREGKEY}"
SectionEnd

