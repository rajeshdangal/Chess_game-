# game.spec
a = Analysis(['game/main.py'],
             pathex=[],
             binaries=[],
             datas=[
                 ('assets', 'assets'),  # Copy assets folder
                 ('game', 'game'),      # Copy game folder if needed
             ],
             hiddenimports=['pygame'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)
pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          [],
          name='ChessGame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,  # Remove console window
          icon='assets/icon.ico')  # Optional icon