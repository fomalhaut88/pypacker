# Pypacker

This program helps to distribute a python program as a debian package or a windows installer.
Pypacker works for Python 3 strictly.

## Dependences

Pypacker requires following programs to be installed:
* pyinstaller (Python 3)
* dpkg (for Linux only)
* inno setup (for Windows only)

## Installation

1. Download this source
2. Run ```python setup.py install```

## Usage

1. Navigate to the root of your project
2. Run ```pypacker-apply.py```
3. Follow the suggested steps
4. Edit created files as you actually need (in some cases it's not necessary)
5. Build your project via the created build scripts
6. Find your files to distribute in dist-directory
