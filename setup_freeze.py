import sys
print 'freeze'
import sys
from cx_Freeze import setup, Executable
files = ["synchronize-rd.png", "COPYING", "synchronizerd.desktop", "install","uninstall","synchronizerd-bin", "paypal_logo.jpg"]

buildOptions = dict(packages=['wx.lib.pubsub'], excludes=[], include_files=files, includes=[])

executables = [
Executable(script='synchronizerd.py', targetName='synchronizerd', shortcutName='SynchroniZeRD', shortcutDir='DesktopFolder', icon='synchronize-rd.png')
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
      executables=executables, requires=['wx', 'rsync'])

#print 'distutils'
#from distutils.core import setup
#
#setup(name='SynchroniZerD',
#      version='1.0.0',
#      description='A simple folder synchronizer application that uses rsync.',
#      long_description='SynchroniZeRD is a folder synchronizer application that uses rsync to synchronize and wxWidgets for the UI',
#      author='Ronnie Andrew',
#      author_email='ronnieandrew92@gmail.com',
#      url='http://www.launchpad.net/synchronizerd',
#      license="GNU GPLv3",
#      # py_modules=['synchronizerd'],
#      scripts=['synchronizerd/synchronizerd'],
#      #packages=['synchronizerd'],
#      data_files=[('/opt/synchronizerd', ['synchronizerd/synchronizerd_UI.py', 'synchronizerd/synchronizerd.py']), ('/opt/synchronizerd', ['synchronizerd/synchronize-rd.png']), (
#          'share/applications', ['synchronizerd/synchronizerd.desktop']), ('/opt/synchronizerd', ['synchronizerd/COPYING'])]
#      )
