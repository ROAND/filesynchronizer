#-*- coding: UTF-8 -*-
import sys
from distutils.core import setup

setup(name='SynchroniZerD',
      version='1.0.0',
      description='A simple folder synchronizer application that uses rsync.',
      long_description='SynchroniZeRD is a folder synchronizer application that uses rsync to synchronize and wxWidgets for the UI',
      author='Ronnie Andrew',
      author_email='ronnieandrew92@gmail.com',
      url='http://www.launchpad.net/synchronizerd',
      license="GNU GPLv3",
      # py_modules=['synchronizerd'],
      scripts=['synchronizerd'],
      #packages=['synchronizerd'],
      data_files=[('/opt/synchronizerd',
                   ['synchronizerd.py', 'synchronizer-rd.png', 'paypal_logo.jpg', 'synchronizerd', 'COPYING',
                    'GNU_HTML']), (
                      'share/applications', ['synchronizerd.desktop']), ('/opt/synchronizerd/views',
                                                                         ['views/synchronizerd_ui.py',
                                                                          'views/__init__.py', 'views/synchronizerd.ui',
                                                                          'views/synchronizerd_ui_pyside.py',
                                                                          'views/feedback_ui.py',
                                                                          'views/feedback_ui_pyside.py',
                                                                          'views/paypal_ui.py',
                                                                          'views/paypal_ui_pyside.py']),
                  ('share/icons/hicolor/256x256/apps', ['synchronizer-rd.png']),
                  ('share/synchronizerd', ['synchronizer-rd.png', 'paypal_logo.jpg', 'COPYING', 'GNU_HTML'])],
      requires=['PyQt4', 'PySide', 'paypalrestsdk']
)
