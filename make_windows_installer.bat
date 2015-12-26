echo on
del /Q mops_installers\*.*
REM create the nsis installer
"C:\Program Files (x86)\NSIS\makensis" mops.nsi
venv\scripts\python.exe make_windows_installer.py
