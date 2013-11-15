import sys
print('freeze')
import sys
from cx_Freeze import setup, Executable
files = ["synchronizer-rd.png", "COPYING", "synchronizerd.desktop", "install","uninstall","synchronizerd-bin", "paypal_logo.jpg"]

buildOptions = dict(packages=[], excludes=[], include_files=files, includes=[])

executables = [
Executable(script='synchronizerd.py', targetName='synchronizerd', shortcutName='SynchroniZeRD', shortcutDir='DesktopFolder', icon='synchronizer-rd.png')
]
setup(name='SynchroniZeRD',
      version='1.0.0',
      license='GPL-3',
      author='Ronnie Andrew',
      author_email='ronnieandrew92@gmail.com',
      description='A simple folder synchronizer application that uses rsync.',
      long_description='SynchroniZeRD is a folder synchronizer application that uses rsync to synchronize and wxWidgets for the UI',
      url="http://www.roandigital.com/applications/synchronizerd",
      options=dict(build_exe=buildOptions),
      executables=executables, requires=['PyQt4', 'rsync', 'PySide','paypalrestsdk'])
