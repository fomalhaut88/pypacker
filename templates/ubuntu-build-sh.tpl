#!/bin/bash

version=`cat version`

echo "Removing old build and dist..."
rm -rf build
rm -rf dist

echo "Pyinstaller packing..."
pyinstaller %(name)s.spec --log-level WARN

echo "Compressing into .tar.gz format..."
tar -czvf dist/%(name)s-ubuntu64-$version.tar.gz -C dist %(name)s

echo "Creating .deb package..."
deb_pkg_dir=dist/%(name)s-ubuntu64-$version
mkdir $deb_pkg_dir
mkdir $deb_pkg_dir/usr
mkdir $deb_pkg_dir/usr/bin
mkdir $deb_pkg_dir/usr/share
mkdir $deb_pkg_dir/usr/share/applications
mkdir $deb_pkg_dir/usr/share/pixmaps
mkdir $deb_pkg_dir/DEBIAN
cp dist/%(name)s $deb_pkg_dir/usr/bin/
cp linux/control $deb_pkg_dir/DEBIAN/
cp linux/%(name)s.desktop $deb_pkg_dir/usr/share/applications
cp %(icon)s $deb_pkg_dir/usr/share/pixmaps
sed -i "s/Version:.*/Version: $version/" $deb_pkg_dir/DEBIAN/control
dpkg-deb --build $deb_pkg_dir
rm -r $deb_pkg_dir

echo "Completed."
