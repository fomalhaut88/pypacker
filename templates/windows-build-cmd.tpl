@echo off

SET /P version=<version

echo Removing old build and dist...
RMDIR /S /Q build
RMDIR /S /Q dist

echo Pyinstaller packing...
pyinstaller %(name)s.spec --log-level WARN

echo Creating setup exe...
POWERSHELL -COMMAND "(GC windows\%(name)s-setup.iss) -REPLACE '#define MyAppVersion \"1.0\"', '#define MyAppVersion \"%%version%%\"' | OUT-FILE dist\%(name)s-setup.iss -Encoding ASCII"
ISCC windows\%(name)s-setup.iss
DEL dist\%(name)s-setup.iss

echo Completed.
