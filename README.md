# BGArmor

## Introduction
BGArmor is a Blender Game Engine and UPBGE tool that allows you to encrypt your
game source files and run them separated from the blenderplayer executable. 
It's currently a work in progress, but available on Windows and Linux.

This project was inspired by BPPlayer, but at the same it's not as reliable as 
it (due to its simplistic concept behind the curtains), it aims to be more
compatible and portable. It also features a project development structure to 
aid the game development workflow and ease the release process.

## Additional Features

BGArmor also aims to provide a toolchain of scripts to automate the process of 
game release, including scripts to create the encrypted data files (using 7-Zip), a blenderplayer icon changer (on Windows) and other.

## Wishlist
Some intended features include:

- Windows installer automated packaging
- Linux .desktop files generator and automated .deb packaging