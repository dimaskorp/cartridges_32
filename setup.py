# coding: utf-8
# python setup.py bdist_msi
from cx_Freeze import setup, Executable

# shortcut_table = [
#     ("DesktopShortcut",                                             # Shortcut
#      "DesktopFolder",                                               # Directory_
#      "Учет картриджей",                                            # Name
#      "TARGETDIR",                                                   # Component_
#      "[TARGETDIR]main.exe",                                 # Target
#      None,                                                          # Arguments
#      None,                                                          # Description
#      None,                                                          # Hotkey
#      None,                                                          # Icon
#      None,                                                          # IconIndex
#      None,                                                          # ShowCmd
#      "TARGETDIR",                                                   # WkDir
#      )
# ]
#
# msi_data = {"Shortcut": shortcut_table}
#
# bdist_msi_options = {'data': msi_data}

executables = [Executable('main.py', base='Win32GUI', icon='i2.ico', shortcut_name='Учет картриджей', shortcut_dir='DesktopFolder')]

build_exe_options = ["images", "fonts"]

#options = {'build_exe': {"include_files": build_exe_options}}
options = {'build_exe': {"include_files": build_exe_options}}

setup(name='Учет картриджей',
      version='1.2',
      description='Демо версия',
      executables=executables,
      options=options)

