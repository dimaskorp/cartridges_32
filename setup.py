# coding: utf-8
# python setup.py bdist_msi
from cx_Freeze import setup, Executable


#executables = [Executable('main.py', base='Win32GUI', icon='iconc.ico', shortcutName='Учет картриджей', shortcutDir='ProgramMenuFolder')]
executables = [Executable('main.py', base='Win32GUI')]

#build_exe_options = ['CART_DB.db', 'images', 'fonts']
build_exe_options = ['images', 'fonts']

#zip_include_packages = ['lib']

#options = {'build_exe': {"include_files": build_exe_options, 'include_msvcr': True}}
options = {'build_exe': {"include_files": build_exe_options}}

setup(name='main',
      version='1.0',
      description='Демо версия',
      executables=executables,
      options=options)

