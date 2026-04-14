# chat_app.spec
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['server.py', 'client/client.py', 'client/chat_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('protocol', 'protocol'),  # Copy toàn bộ thư mục protocol
        ('client', 'client'),      # Copy toàn bộ thư mục client
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Tạo EXE cho Server
exe_server = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='chat_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Server cần console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Thêm icon nếu có: icon='server.ico'
)

# Tạo EXE cho CLI Client
exe_client = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='chat_client_cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,  # CLI client cần console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Tạo EXE cho GUI Client
exe_gui = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='chat_client_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,  # GUI không cần console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Thêm icon nếu có: icon='chat.ico'
)

# Gom tất cả vào collection
coll = COLLECT(
    exe_server,
    exe_client,
    exe_gui,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ChatApp'
)