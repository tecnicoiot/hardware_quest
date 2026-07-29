APP_NAME = HardwareQuest
APP_ID = hardwarequest
SRC = main.py

.PHONY: all clean windows-x64 windows-arm linux-x64 linux-arm

all: linux-x64 windows-x64

windows-x64:
	pyinstaller --onefile --noconsole --name $(APP_NAME)-win-x64.exe --icon=assets/img/logo_iot.ico --add-data "assets:assets" $(SRC)

windows-arm:
	pyinstaller --onefile --noconsole --name $(APP_NAME)-win-arm.exe --icon=assets/img/logo_iot.ico --add-data "assets:assets" $(SRC)

linux-x64:
	pyinstaller --onefile --name $(APP_ID) --icon=assets/img/logo_iot.ico --add-data "assets:assets" $(SRC)
	mkdir -p dist/AppDir-x64/usr/bin
	cp dist/$(APP_ID) dist/AppDir-x64/usr/bin/
	cp -r assets dist/AppDir-x64/usr/bin/
	echo '#!/bin/sh' > dist/AppDir-x64/AppRun
	echo 'SELF=$$(dirname "$$(readlink -f "$$0")")' >> dist/AppDir-x64/AppRun
	echo 'exec "$$SELF/usr/bin/$(APP_ID)" "$$@"' >> dist/AppDir-x64/AppRun
	chmod +x dist/AppDir-x64/AppRun
	echo '[Desktop Entry]' > dist/AppDir-x64/$(APP_ID).desktop
	echo 'Type=Application' >> dist/AppDir-x64/$(APP_ID).desktop
	echo 'Name=$(APP_NAME)' >> dist/AppDir-x64/$(APP_ID).desktop
	echo 'Exec=$(APP_ID)' >> dist/AppDir-x64/$(APP_ID).desktop
	echo 'Icon=$(APP_ID)' >> dist/AppDir-x64/$(APP_ID).desktop
	echo 'Categories=Game;' >> dist/AppDir-x64/$(APP_ID).desktop
	cp assets/img/logo_iot.png dist/AppDir-x64/$(APP_ID).png
	test -f appimagetool-x86_64 || (curl -Lo appimagetool-x86_64 https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage && chmod +x appimagetool-x86_64)
	rm -rf squashfs-root-x64
	./appimagetool-x86_64 --appimage-extract
	mv squashfs-root squashfs-root-x64
	ARCH=x86_64 ./squashfs-root-x64/AppRun dist/AppDir-x64 dist/$(APP_NAME)-x86_64.AppImage

linux-arm:
	pyinstaller --onefile --name $(APP_ID) --icon=assets/img/logo_iot.png --add-data "assets:assets" $(SRC)
	mkdir -p dist/AppDir-arm/usr/bin
	cp dist/$(APP_ID) dist/AppDir-arm/usr/bin/
	cp -r assets dist/AppDir-arm/usr/bin/
	echo '#!/bin/sh' > dist/AppDir-arm/AppRun
	echo 'SELF=$$(dirname "$$(readlink -f "$$0")")' >> dist/AppDir-arm/AppRun
	echo 'exec "$$SELF/usr/bin/$(APP_ID)" "$$@"' >> dist/AppDir-arm/AppRun
	chmod +x dist/AppDir-arm/AppRun
	echo '[Desktop Entry]' > dist/AppDir-arm/$(APP_ID).desktop
	echo 'Type=Application' >> dist/AppDir-arm/$(APP_ID).desktop
	echo 'Name=$(APP_NAME)' >> dist/AppDir-arm/$(APP_ID).desktop
	echo 'Exec=$(APP_ID)' >> dist/AppDir-arm/$(APP_ID).desktop
	echo 'Icon=$(APP_ID)' >> dist/AppDir-arm/$(APP_ID).desktop
	echo 'Categories=Game;' >> dist/AppDir-arm/$(APP_ID).desktop
	cp assets/img/logo_iot.png dist/AppDir-arm/$(APP_ID).png
	test -f appimagetool-aarch64 || (curl -Lo appimagetool-aarch64 https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-aarch64.AppImage && chmod +x appimagetool-aarch64)
	rm -rf squashfs-root-arm
	./appimagetool-aarch64 --appimage-extract
	mv squashfs-root squashfs-root-arm
	ARCH=aarch64 ./squashfs-root-arm/AppRun dist/AppDir-arm dist/$(APP_NAME)-aarch64.AppImage

clean:
	rm -rf build dist *.spec appimagetool-x86_64 appimagetool-aarch64 squashfs-root-x64 squashfs-root-arm
