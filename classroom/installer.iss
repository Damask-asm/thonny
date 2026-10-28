[Setup]
AppId={{B8B3E505-2451-41A4-9324-760884648D70}
AppName=Thonny Classroom
AppVersion=5.0.0.1
AppVerName=Thonny Classroom 5.0.0.1 (unofficial)
AppPublisher=Thonny Classroom contributors
AppPublisherURL=https://github.com/Damask-asm/thonny
AppSupportURL=https://github.com/Damask-asm/thonny/issues
AppUpdatesURL=https://github.com/Damask-asm/thonny/releases/latest
DefaultDirName={localappdata}\Programs\Thonny-Classroom
DefaultGroupName=Thonny Classroom
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
DisableDirPage=no
DisableProgramGroupPage=yes
WizardStyle=modern
LicenseFile=..\packaging\windows\license-for-win-installer.txt
SetupIconFile=..\thonny\res\thonny.ico
UninstallDisplayIcon={app}\thonny.exe
OutputDir=..\dist
OutputBaseFilename=Thonny-Classroom-5.0.0-x64-Setup
Compression=lzma2
SolidCompression=yes
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\build\bundle\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Thonny Classroom"; Filename: "{app}\thonny.exe"; WorkingDir: "{userdocs}"
Name: "{autodesktop}\Thonny Classroom"; Filename: "{app}\thonny.exe"; WorkingDir: "{userdocs}"; Tasks: desktopicon

[Run]
Filename: "{app}\thonny.exe"; Description: "Launch Thonny Classroom"; Flags: nowait postinstall skipifsilent
