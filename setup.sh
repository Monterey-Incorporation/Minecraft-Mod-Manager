rm -rf dist
rm -rf build
rm -rf src
mkdir src
pyinstaller main.py --name="Minecraft Mod Manager" --onefile --windowed
rm "./dist/Minecraft Mod Manager"
create-dmg \
    --volname "Minecraft Mod Manager"\
    --add-drop-link \
    "./src/Minecraft Mod Manager.dmg"