import PyInstaller.__main__

ICON_PATH = 'icon.ico'

PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    f'--icon={ICON_PATH}',
    './main.py',
])
