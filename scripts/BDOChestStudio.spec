# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import os

ROOT = Path(SPECPATH).parent

a = Analysis(
    [str(ROOT / 'src' / 'launcher.py')],
    pathex=[str(ROOT / 'src')],
    binaries=[],
    datas=[(str(ROOT / 'src/bdo_sim/assets'), 'bdo_sim/assets'),
           (str(ROOT / 'LICENSE'), 'licenses'),
           (str(ROOT / 'THIRD_PARTY_NOTICES.md'), 'licenses')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# Qt 6 uses the Windows 10+ ICU API. Unrelated tools on PATH (for example
# Poppler) can expose an icuuc.dll with version-suffixed, incompatible exports.
# These OS components must be provided by Windows, never shadowed by a bundle.
def is_os_component(destination):
    name = Path(destination).name.lower()
    return (name in {'icuuc.dll', 'icuin.dll', 'ucrtbase.dll'}
            or name.startswith(('api-ms-win-', 'ext-ms-win-', 'icudt')))

a.binaries = [entry for entry in a.binaries if not is_os_component(entry[0])]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=os.environ.get('BDO_BUILD_NAME', 'BDOChestStudio'),
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
)
