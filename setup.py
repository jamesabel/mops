
from distutils.core import setup
import py2exe

setup(console=['mops.py'],

      # single executable doesn't seem to work
      #options = {'py2exe': {'bundle_files': 1}},
      #zipfile = None,

      )
