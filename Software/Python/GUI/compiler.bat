@echo off
echo ---------------------------------------------------------------------------
echo Compile all .ui files from Qt Designer.
forfiles /c "cmd /c (if @ext==\"ui\" pyuic5 --from-imports @file -o @fname_ui.py & echo @file)"
echo.
echo Done.
echo.
echo ---------------------------------------------------------------------------
echo Compile resource file (icons, etc..)
forfiles /c "cmd /c (if @ext==\"qrc\" pyrcc5 @file -o @fname_rc.py & echo @file)"
echo.
echo Done.
echo.
echo ---------------------------------------------------------------------------
pause