# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller fredus.spec --noconfirm
# (depuis la racine du projet, avec le venv activé)

from pathlib import Path

from PyInstaller.building.build_main import Analysis, COLLECT, EXE, PYZ

block_cipher = None

_root = Path(SPEC).resolve().parent

# Fichiers de données (assets + paquets avec bytecode dans __pycache__)
datas = []
for _sub in ("assets", "data", "entities", "game", "objects", "rooms", "systems", "ui", "__pycache__"):
    _base = _root / _sub
    if not _base.is_dir():
        continue
    for _f in _base.rglob("*"):
        if _f.is_file():
            _rel = _f.relative_to(_root)
            _dest = str(_rel.parent).replace("\\", "/")
            datas.append((str(_f), _dest))

a = Analysis(
    [str(_root / "main.py")],
    pathex=[str(_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "_pyc_hook",
        "pygame",
        "runtime_patches",
        "net_assets",
        "json",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FredusJonesAdventures",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="FredusJonesAdventures",
)
