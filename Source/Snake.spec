# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Christian Ransom\\Desktop\\Python\\Snake Game\\Source'],
             binaries=[],
             datas=[('SnakeIcon.jpg', '.'),
					('103336__fawfulgrox__low-bloop.wav', '.'),
					('341695__projectsu012__coins-1.wav', '.'),
					('Mario_Jumping-Mike_Koenig-989896458.wav', '.'),
					('GUI Sound Effects_038.wav', '.'),
					('Computer_Error_Alert.wav', '.'),
					('146726__leszek-szary__jumping.wav', '.'),
             		],             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Snake',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
