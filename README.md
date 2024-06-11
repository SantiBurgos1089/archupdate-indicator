# Arch Update Indicator
> Creates a XApp StatusIcon that indicates if updates are available and provides a context menu to inspect and install them

This is a fork of the original [archupdate-indicator](https://github.com/epsilontheta/archupdate-indicator) created by epsilontheta, this fork uses Gtk, XApp and associated technologies from both instead of wxpython, the final task continues the same at its core: create a taskbar icon that visually indicates if updates are available using `checkupdates` from the pacman-contrib package.

Regarding the original code, the same instructions given below still applies to the corresponding environment variables:

* `UPDATE_CMD` is used to configure the command that will be executed to update (By default is `sudo pacman -Syu`).

* `ICONS_FOLDER` is used to configure the path where the icons are stored (By default is `/usr/share/pixmaps/archupdate-indicator`. Credits to the icons used goes to [mintupdate package](https://github.com/linuxmint/mintupdate)).

* `UPDATE_PERIOD` is used to configure time between checking for updates, this one is set in ms. (By default is 1h).

* `TERMINAL` is used to change the terminal emulator (By default `xterm` is used, although you can use other terminal program as long as it supports the `-e` parameter).

## Installation

### Manual installation

```sh
# install dependencies
pacman -S pacman-contrib xapp gtk3
git clone 'https://github.com/SantiBurgos1089/archupdate-indicator'
cd archupdate-indicator/
cp archupdate-indicator.py /usr/local/bin/
cp -r /usr/share/pixmaps/ /usr/share/pixmaps/archupdate-indicator
```

### AUR

## Release History

* 1.0.1
    * Migrated code to XApps and GTK instead of using wxpython
* 1.0.0
    * Add return code 2 handling of checkupdates
* 0.0.2
    * Add additional environment variables
* 0.0.1
    * Initial release

## TODO (?)
* Add AUR helpers as an option alongside pacman
* Configure the update period to check
* Create an AUR package