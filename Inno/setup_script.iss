; setup_script.iss
[Setup]
AppName=HAC Archiver
AppVersion=1.0
DefaultDirName={pf}\HACArchiver
DefaultGroupName=HACArchiver
OutputBaseFilename=HACArchiver_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\maksv\Desktop\4-Hybrid Adaptive Compression (HAC)\dist\HACArchiver.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\maksv\Desktop\4-Hybrid Adaptive Compression (HAC)\ui\hac_icon.ico"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\HACArchiver"; Filename: "{app}\HACArchiver.exe"

[Registry]
; Расширение .hac
Root: HKCR; Subkey: ".hac"; ValueType: string; ValueName: ""; ValueData: "HACFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "HACFile"; ValueType: string; ValueData: "HAC Archive File"
Root: HKCR; Subkey: "HACFile\DefaultIcon"; ValueType: string; ValueData: "{app}\hac_icon.ico"
Root: HKCR; Subkey: "HACFile\shell\open\command"; ValueType: string; ValueData: """{app}\HACArchiver.exe"" ""%1"""
