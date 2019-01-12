# ClipCommander
## Clipboard selection monitor youtube-dl GUI front-end

- License: MIT License
- Author: Matteljay
- Language: Python (>= 3.5)
- Homepage: https://github.com/Matteljay


## Screenshots

![](https://github.com/Matteljay/labelpush/blob/master/screenshots/01_selected.png)
![](https://github.com/Matteljay/labelpush/blob/master/screenshots/02_edit_modus.png)
![](https://github.com/Matteljay/labelpush/blob/master/screenshots/03_button_edit.png)
![](https://github.com/Matteljay/labelpush/blob/master/screenshots/04_settings.png)


## Introduction

ClipCommander is a clipboard selection monitor. It is a productivity tool pre-configured
to work as a GUI/front-end for [youtube-dl](https://rg3.github.io/youtube-dl/).
It can be considered a Firefox Plug-in without requiring integration into the add-on menu.
Simply copy a YouTube video link to the clipboard and ClipCommander will pop-up with several download format options.

ClipCommander is highly configurable to execute any terminal/shell
command based on a clipboard selection using [Python RegEx](https://docs.python.org/3/howto/regex.html)
string magic (Regular expressions). The actions are highly customizable.

For example text-to-speech [festival](http://www.cstr.ed.ac.uk/projects/festival/),
BitTorrent client [transmission](https://transmissionbt.com/), custom clipboard logging operations and more.
On Linux based systems you will get instant feedback based on your text selections (no Ctrl+c required!)


## Installation

Package dependencies are kept to a minimum. The proper installation guides
for your system can be found via these links:

- [Kivy](https://kivy.org/doc/stable/installation/installation.html) & [Pillow](https://python-pillow.org/)
Version 1.10.1 with SDL2 window provider are required! (NOT 1.9 with PyGame).
An updated Python Imaging Library is always recommended with a graphical Python program.

- [pip3](https://github.com/pypa/pip) & [setuptools](https://github.com/pypa/setuptools)
These are Python 3 installation tools. Universally useful!

- [xclip](https://github.com/astrand/xclip) & [xterm](https://invisible-island.net/xterm/)
Handy tools that work on almost all Linux flavors.

- [youtube-dl](https://rg3.github.io/youtube-dl/) & [ffmpeg](https://ffmpeg.org/)
All the magic required to get videos cleanly from YouTube. Must be very up-to-date to work!

### Debian Linux

For most up-to-date Debian based systems like Ubuntu Linux and Linux Mint this should work *as root*:

    add-apt-repository ppa:kivy-team/kivy
    apt-get install python3-kivy python3-pip python3-setuptools xterm xclip ffmpeg
    pip3 install --upgrade youtube-dl pillow clipcommander

### Arch Linux

For the more up-to-date Arch Linux (Manjaro) simply run *as root*:

    pacman -S python-kivy python-pillow python-pip python-setuptools xclip xterm youtube-dl ffmpeg
    pip3 install clipcommander

### Daemonize

It is easy to daemonize ClipCommander. That means it can run silently in the background. It can pop up
only when the clipboard selection is matched against one of the user defined conditions.
To accomplish this hidden modus, enable the option in the app (see screenshot above).

When in hidden modus, you can force showing the GUI by selecting the text **!showyourself**

To make ClipCommander start at system boot, simply add this app to the **Startup Applications**
list on your desktop (e.g. Cinnamon).


## How to launch

When finished, the shortcut icon can be found from your menu-bar in the **Office** category.
If the icon does not show up, you may need to restart your desktop.
Alternatively, open your graphical user terminal and type **clipcommander.py**


## For developers, hackers and testers

Other ways to install are explained below. The above dependencies are still required!
Only use the info below if you know what you are doing.

### Option 1

You can install from tar.gz or the GitHub master tree.
First, download and extract the archive from the [releases](https://github.com/Matteljay/clipcommander/releases) page.
Then run from within the extracted folder:

    sudo pip3 install .

### Option 2

Alternatively, you can run it without installing to the root
filesystem. Again, extract the downloaded archive. Then run:

    pip3 install --user -r requirements.txt
    ./clipcommander.py


## More platforms

### Other UNIX

Other flavors of Linux are untested but there is no reason for them
not to work. Slackware, Gentoo, openSUSE, Fedora, Red Hat, Mandriva, CentOS, macOS,...

### Android, iPhone and Windows

These platforms probably won't work as they feature different clipboard
mechanisms and terminal emulators. If a strong desire exists, find a way to
motivate me :-)


## Contact info & donations

See the [contact](https://github.com/Matteljay/labelpush/blob/master/CONTACT.md) file.


