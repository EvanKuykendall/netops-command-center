Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 1. Get the folder where this script file lives
CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)

' 2. Build the path to server.py dynamically
ServerPath = fso.BuildPath(CurrentDirectory, "server.py")

' 3. Run Python hidden (windowless)
' Note: This assumes 'python' is in the Windows PATH (Standard install)
WshShell.Run "python """ & ServerPath & """", 0