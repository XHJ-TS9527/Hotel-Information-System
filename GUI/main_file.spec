# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis([
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\main_file.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\multiprocessing_win.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\main_window_package.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\city_select_package.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\date_select_package.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\consult_progress_package.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI\setting_package.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\spiders\crawl_ctrip.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\spiders\crawl_qunar.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\spiders\hotel_classes.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\spiders\simulation_explorer_driver.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\operations\comment_judge.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\exception_classes.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\global_manager.py',
r'C:\Users\SCUTEEXHJ\Desktop\类代码\qunar_city_map_dictionary.py'],
             pathex=[r'C:\Users\SCUTEEXHJ\Desktop\类代码\GUI'],
             binaries=[],
             datas=[(r'C:\Users\SCUTEEXHJ\Desktop\类代码\operations\model','.')],
             hiddenimports=['main_window_package','multiprocessing_win','city_select_package','date_select_package','date_select_package',
'consult_progress_package','setting_package','crawl_ctrip','crawl_qunar','hotel_classes','simulation_explorer_driver',
'comment_judge','exception_classes','global_manager','qunar_city_map_dictionary'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main_file',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='华南理工大学logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main_file')
