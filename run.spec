# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


added_files = [
    ( 'cfg/anon.session', 'cfg/' ),
    ( 'gender_computer/', '.' ),
    ( 'py_hardware_binding/license.txt', 'py_hardware_binding/' ),
]

a = Analysis(['run.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='AMOS_Telegram_Parser',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          icon='baddrip.ico',
          entitlements_file=None )
