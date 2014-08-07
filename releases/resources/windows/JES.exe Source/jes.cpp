#include <cstdlib>
#include <windows.h>
#include <string>

int WinMain( HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd )
{
	std::string command = "cmd.exe /c jes.bat ";

	command.append( lpCmdLine );

	char *commandString = new char[ command.length() + 1 ];
	strncpy( commandString, command.c_str(), command.length() );
	commandString[ command.length() ] = '\0';

    STARTUPINFO StartupInfo;
    PROCESS_INFORMATION ProcessInfo;

    memset( &StartupInfo, 0, sizeof( StartupInfo ) );
    StartupInfo.cb = sizeof( STARTUPINFO );
    StartupInfo.dwFlags = STARTF_USESHOWWINDOW;
    StartupInfo.wShowWindow = SW_HIDE;

	char *cwd = new char[ MAX_PATH ];
	GetModuleFileName( NULL, cwd, MAX_PATH );

	int lastSlash = 0;

	for ( int i = 0; i < MAX_PATH; ++i )
	{
		if ( cwd[i] == '\\' )
		{
			lastSlash = i;
		}
		else if ( cwd[i] == '\0' )
		{
			break;
		}
	}

	cwd[lastSlash + 1] = '\0';

    if ( !CreateProcess( NULL, commandString, NULL, NULL, FALSE, CREATE_NEW_CONSOLE, NULL, cwd, &StartupInfo, &ProcessInfo ) )
    {
    	return GetLastError();		
    }

	DWORD rc = 0;

    WaitForSingleObject( ProcessInfo.hProcess, INFINITE );

    GetExitCodeProcess( ProcessInfo.hProcess, &rc );

    CloseHandle( ProcessInfo.hThread );
    CloseHandle( ProcessInfo.hProcess );

	return ( int )rc;
}
