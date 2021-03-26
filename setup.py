# coding: utf-8
# python setup.py bdist_msi
from cx_Freeze import setup, Executable

#executables = [Executable('main.py', base='Win32GUI', icon='i2.ico', shortcut_name='Учет картриджей', shortcut_dir='DesktopFolder')]
executables = [Executable('main.py', base='Win32GUI')]

build_exe_options = ["images", "fonts"]

options = {'build_exe': {"include_files": build_exe_options}}

setup(name='Cartridges',
      version='1.2',
      description='Демо версия',
      executables=executables,
      options=options)

