c:\Python34\python c:\Python34\Tools\Scripts\pyvenv.py --clear venv
call venv\Scripts\activate.bat
pip.exe install psutil
pip.exe install py2exe
pip.exe install pysdie
pip.exe install redis
pip.exe install pytest
pip.exe install requests
REM packages not in pypi (can not be installed with pip):
easy_install.exe third_party_installers\pywin32-219.win-amd64-py3.4.exe
REM
REM PySide not installing this way so use PySide-1.2.2.win-amd64-py3.4.exe
REM pip.exe install PySide
easy_install.exe third_party_installers\PySide-1.2.2-py3.4-win-amd64.egg
