; Inno Setup Script
; Gera instalador Setup_Conversor_SIPROQUIM.exe a partir da pasta dist/Conversor_SIPROQUIM

#define MyAppName "SIPROQUIM Converter"
#define MyAppVersion "6.0.0"
#define MyAppPublisher "Rodogarcia"
#define MyAppExeName "Conversor_SIPROQUIM.exe"

[Setup]
AppId={{53B8A0CB-8E20-4F70-9B63-C1A24D2FC97C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=Setup_Conversor_SIPROQUIM
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\public\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Files]
; Inclui somente artefatos de runtime da pasta dist.
; Exclui backups explicitamente (defesa adicional).
Source: "..\dist\Conversor_SIPROQUIM\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "backups\*"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent
