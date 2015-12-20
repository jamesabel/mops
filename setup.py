
from distutils.core import setup
import py2exe

setup(windows=['mops.py'],
      packages=['mops'],
      options={"py2exe":
          {
              "includes": ['redis', 'win32api', 'win32con', 'requests', 'psutil' ]
          }
      }

      # single executable doesn't seem to work
      #options = {'py2exe': {'bundle_files': 1}},
      #zipfile = None,

      )
