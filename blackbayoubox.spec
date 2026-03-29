# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['blackBayouBox.py'],
    pathex=[],
    binaries=[],
    datas=[('beam area no beam.png', '.'), ('beam area with beam.png', '.'), ('bruce afraid.png', '.'), ('bruce disappointed.png', '.'), ('bruce.png', '.'), ('chop_animation_f1.png', '.'), ('chop_animation_f2.png', '.'), ('chop_animation_f3.png', '.'), ('chop_animation_f4.png', '.'), ('chop_animation_f5.png', '.'), ('chop_animation_f6.png', '.'), ('chop_animation_f7.png', '.'), ('chop_animation_f8.png', '.'), ('chop_animation_f9.png', '.'), ('Courtyard Discussions.wav', '.'), ('craig.png', '.'), ('end image bedpar.png', '.'), ('end image pilpar.png', '.'), ('Escaped.wav', '.'), ('Escaping.wav', '.'), ('fishing animation f1.png', '.'), ('fishing animation f2.png', '.'), ('fishing animation f3.png', '.'), ('fishing animation f4.png', '.'), ('fishing animation f5.png', '.'), ('fishing animation f6.png', '.'), ('fishing animation f7.png', '.'), ('fishing animation f8.png', '.'), ('fishing animation f9.png', '.'), ('fishing animation f10.png', '.'), ('fishing animation f11.png', '.'), ('fishing animation f12.png', '.'), ('fishing animation f13.png', '.'), ('In Your Cell.wav', '.'), ('kitchen animation f1.png', '.'), ('kitchen animation f2.png', '.'), ('kitchen animation f3.png', '.'), ('kitchen animation f4.png', '.'), ('kitchen animation f5.png', '.'), ('kitchen animation f6.png', '.'), ('kitchen animation f7.png', '.'), ('kitchen animation f8.png', '.'), ('laundry - bedsheet.png', '.'), ('laundry - officers coat.png', '.'), ('laundry - officers hat.png', '.'), ('laundry - pillowcase.png', '.'), ('laundry - prisoner jumpsuit.png', '.'), ('Manual Labour 1.wav', '.'), ('Manual Labour 2.wav', '.'), ('Manual Labour 3.wav', '.'), ('Manual Labour 4.wav', '.'), ('mine_animation_f1.png', '.'), ('mine_animation_f2.png', '.'), ('mine_animation_f3.png', '.'), ('mine_animation_f4.png', '.'), ('mine_animation_f5.png', '.'), ('mine_animation_f6.png', '.'), ('mine_animation_f7.png', '.'), ('mine_animation_f8.png', '.'), ('mine_animation_f9.png', '.'), ('mine_animation_f10.png', '.'), ('mine_animation_f11.png', '.'), ('mine_animation_f12.png', '.'), ('mine_animation_f13.png', '.'), ('mine_animation_f14.png', '.'), ('mine_animation_f15.png', '.'), ('prison_cell.png', '.'), ('prison_cell_escape.png', '.'), ('rooftop.png', '.'), ('SFX Cast Net 1.wav', '.'), ('SFX Cast Net 2.wav', '.'), ('SFX Cast Net 3.wav', '.'), ('SFX Chopping 1.wav', '.'), ('SFX Chopping 2.wav', '.'), ('SFX Chopping 3.wav', '.'), ('SFX Cutlery 1.wav', '.'), ('SFX Cutlery 2.wav', '.'), ('SFX Exit Vent.wav', '.'), ('SFX Inside Vent.wav', '.'), ('SFX Laundry 1.wav', '.'), ('SFX Laundry 2.wav', '.'), ('SFX Laundry 3.wav', '.'), ('SFX Mining 1.wav', '.'), ('SFX Mining 2.wav', '.'), ('SFX Mining 3.wav', '.'), ('SFX Reel Net 1.wav', '.'), ('SFX Reel Net 2.wav', '.'), ('SFX Reel Net 3.wav', '.'), ('SFX Serve Dish 1.wav', '.'), ('SFX Serve Dish 2.wav', '.'), ('SFX Serve Dish 3.wav', '.'), ('SFX Torch.wav', '.'), ('SFX Vent Falling.wav', '.'), ('SFX Warehouse Box 1.wav', '.'), ('SFX Warehouse Box 2.wav', '.'), ('SFX Warehouse Lumber 1.wav', '.'), ('SFX Warehouse Lumber 2.wav', '.'), ('sid.png', '.'), ('Spotted.wav', '.'), ('stunned walter no coat or hat.png', '.'), ('stunned walter no coat.png', '.'), ('stunned walter no hat.png', '.'), ('stunned walter.png', '.'), ('theo.png', '.'), ('Title Theme.wav', '.'), ('title_screen.png', '.'), ('vents no light.png', '.'), ('vents with light.png', '.'), ('walter with no coat or hat.png', '.'), ('walter with no coat.png', '.'), ('walter with no hat.png', '.'), ('walter.png', '.'), ('warehouse - box of goods.png', '.'), ('warehouse - lumber.png', '.')],
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
    name='blackBayouBox',
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
    icon=['gameicon.ico'],
)
