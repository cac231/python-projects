# -*- mode: python ; coding: utf-8 -*-
import os

pasta_projeto = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    [os.path.join(pasta_projeto, 'jogo_cobra_lesk.py')],
    pathex=[pasta_projeto],
    binaries=[],
    datas=[
        # Adiciona a pasta assets inteira
        (os.path.join(pasta_projeto, 'assets'), 'assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Hora do Lesk',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets\images\icon\icon.ico"
)
