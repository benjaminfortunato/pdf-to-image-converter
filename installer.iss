[Setup]
AppName=PDF to Image Converter
AppVersion=1.0.0
AppPublisher=Your Name
AppPublisherURL=https://github.com/yourusername/pdf-to-image
DefaultDirName={autopf}\PDF to Image Converter
DefaultGroupName=PDF to Image Converter
OutputDir=installer
OutputBaseFilename=PDF-to-Image-Converter-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\PDF-to-Image-Converter.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\PDF-to-Image-Converter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PDF to Image Converter"; Filename: "{app}\PDF-to-Image-Converter.exe"
Name: "{group}\{cm:UninstallProgram,PDF to Image Converter}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PDF to Image Converter"; Filename: "{app}\PDF-to-Image-Converter.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\PDF-to-Image-Converter.exe"; Description: "{cm:LaunchProgram,PDF to Image Converter}"; Flags: nowait postinstall skipifsilent
