REM usually I create the venv in PyCharm but this should work too
REM c:\Python34\python c:\Python34\Tools\Scripts\pyvenv.py --system-site-packages venv
pushd .
call venv\Scripts\activate.bat
c:\python34\scripts\pip.exe install psutil
c:\python34\scripts\pip.exe install py2exe
c:\python34\scripts\pip.exe install redis
c:\python34\scripts\pip.exe install pytest
c:\python34\scripts\pip.exe install requests
c:\python34\scripts\pip.exe install uptime
c:\python34\scripts\pip.exe install Shiboken
REM you may have to do a 2to3 on winstats
c:\python34\scripts\pip.exe install winstats
REM
REM packages not in pypi (can not be installed with pip)
REM
REM lately these are not working with venv so I put them in the base python installation prior to making the venv
REM
REM easy_install.exe third_party_installers\pywin32-219.win-amd64-py3.4.exe
REM
REM PySide not installing this way so use PySide-1.2.2.win-amd64-py3.4.exe
REM pip.exe install PySide
REM easy_install.exe third_party_installers\PySide-1.2.2-py3.4-win-amd64.egg
popd
