#!/usr/bin/python -tt

""" Setup """

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PKG = open('debian/changelog').readline().split(' ')[0]

setup(name=PKG,
    description='Learning tool based on spaced repetition technique',
    version=open('debian/changelog').readline().split(' ')[1][1:-1],
    author="Pomni Development team",
    author_email="pomni@googlegroups.com",
    license='GPL 2',
    packages=["mnemosyne.maemo_ui", "mnemosyne.maemo_ui.widgets"],
    package_dir={'mnemosyne.maemo_ui': ''},
    data_files = [(os.path.join('share/%s/' % PKG, path), \
        [os.path.join(path, fname) for fname in files]) \
        #for path, dirs, files in os.walk('hildon-UI/rainbow')] + \
        #[(os.path.join('share/%s/' % PKG, path), \
        #    [os.path.join(path, fname) for fname in files]) \
        for path, dirs, files in os.walk('hildon-UI/dark')] + \
       [('share/dbus-1/services', ['maemo/%s.service' % PKG]),
        ('share/applications/hildon', ['maemo/%s.desktop' % PKG]),
        #('share/%s/demo' % PKG, [".%s/default.db" % PKG]),
        ('share/%s/html' % PKG, ['help.html']),
        ('share/icons/hicolor/26x26/apps/',
         ['./maemo/icons/26x26/%s.png' % PKG]),
        ('share/icons/hicolor/64x64/apps/',
         ['./maemo/icons/64x64/%s.png' % PKG])],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries',
    ])
