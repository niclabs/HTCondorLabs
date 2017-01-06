# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable


include_files = ['doc']
includes = []
excludes = [
    'matplotlib', 
    'numpy', 
    'PyQt4',
    'scipy', 
    'six'
    ]
    
packages = []  # modules

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'  # no console
    #base = 'Console'  # get console

options = { 'build_exe': { 'include_files': include_files,
                           'includes': includes,
                           'excludes': excludes,
                           'packages': packages
                         }
          }

executables = [
    Executable(
        script = 'condor_gui.py',
        base = base,
        icon='icon_condor_gui.ico'
        )
    ]

setup(name = 'Condor GUI',
      version = '0.1',
      description = 'Condor GUI for managing and working with one or more Condor pools.',
      options = options,
      executables = executables
      )

      
#setup(
#    name = 'myapp',
#    version = '0.1',
#    description = 'A general enhancement utility',
#    author = 'lenin',
#    author_email = 'le...@null.com',
#    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
#    executables = [Executable('janitor.py')]
#)
