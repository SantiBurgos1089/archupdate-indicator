#!/usr/bin/env python3

import subprocess
import os
import gi
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Gtk','3.0')
gi.require_version('Notify', '0.7')
gi.require_version('XApp','1.0')
from gi.repository import GdkPixbuf, GLib, Gtk, Notify, XApp

# update period in ms
UPDATE_PERIOD = int (os.getenv('UPDATE_PERIOD', 60 * 60 * 1000))

# terminal has to support `-e` parameter
TERMINAL = os.getenv('TERMINAL', "xterm")

# the cmd to execute when clicking update
UPDATE_CMD = os.getenv('UPDATE_CMD', "sudo pacman -Syu")

# the folder used to search the icons
ICONS_FOLDER = os.getenv('ICONS_FOLDER', "/usr/share/pixmaps/archupdate-indicator")

ARCHUPDATE_INDICATOR_VERSION = "1.0.1"

APPLICATION_ID = "org.x.archupdate-indicator"

class Icons:
	def __getPath(x):
		return os.path.join (ICONS_FOLDER, x)

	NO_UPDATES = __getPath("archupdate-up-to-date.svg")
	UPDATES_AVAILABLE = __getPath("archupdate-updates-available.svg")
	CHECK_UPDATES_FAILED = __getPath("archupdate-updates-failed.svg")

class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__(application_id=APPLICATION_ID)
        
        self.Terminal = TERMINAL
        self.UpdateCmd = UPDATE_CMD
        self.TimerApplication
        
    def CreatePopupMenu(self):
        self.status_icon = XApp.StatusIcon()
        self.status_icon.set_icon_name(Icons.NO_UPDATES)
        self.status_icon.set_tooltip_text("Everything is up to date")
        self.status_icon.set_visible(True)
        self.status_icon.connect("button-release-event", self.do_statusicon)
       
    def SetStatusIcon(self, path):
        self.status_icon = XApp.StatusIcon()
        
        if path == Icons.NO_UPDATES:
            self.status_icon.set_icon_name(Icons.NO_UPDATES)
            self.status_icon.set_tooltip_text("Everything is up to date")
            self.status_icon.set_visible(True)
            self.status_icon.connect("button-release-event", self.do_statusicon)
        elif path == Icons.UPDATES_AVAILABLE:
            self.status_icon.set_icon_name(Icons.UPDATES_AVAILABLE)
            self.status_icon.set_tooltip_text("Updates available")
            self.status_icon.set_visible(True)
            self.status_icon.connect("button-release-event", self.do_statusicon)
        elif path == Icons.CHECK_UPDATES_FAILED:
            self.status_icon.set_icon_name(Icons.CHECK_UPDATES_FAILED)
            self.status_icon.set_tooltip_text("checkupdates command failed")
            self.status_icon.set_visible(True)
            self.status_icon.connect("button-release-event", self.do_statusicon)   
        
    def CheckUpdates(self, data = None):
        PacmanCheckUpdates = subprocess.run(["checkupdates"], capture_output=True, text=True, encoding='utf-8')
        
        # Updates available
        if PacmanCheckUpdates.returncode == 0:
            self.Updates = PacmanCheckUpdates.stdout.splitlines()
            self.TotalUpdates = len(self.Updates)
            
            if self.TotalUpdates > 1:
                icon = Icons.UPDATES_AVAILABLE
                Notify.init("Updates available")
                NotificationTotalUpdates = Notify.Notification.new("Updates available", "{} updates available".format (self.TotalUpdates), icon)
                NotificationTotalUpdates.show()
            elif self.TotalUpdates == 1:
                icon = Icons.UPDATES_AVAILABLE
                Notify.init("Updates available")
                NotificationTotalUpdates = Notify.Notification.new("Update available", "1 update available", icon)
                NotificationTotalUpdates.show()
            else:
                icon = Icons.NO_UPDATES
                Notify.init("No updates found")
                NotificationTotalUpdates = Notify.Notification.new("No updates found", "No updates found", icon)
                NotificationTotalUpdates.show()
                
        # No updates found
        elif PacmanCheckUpdates.returncode == 2:
            icon = Icons.NO_UPDATES
            Notify.init("No updates found")
            NotificationTotalUpdates = Notify.Notification.new("No updates found", "No updates found", icon)
            NotificationTotalUpdates.show()
            
        # Treat everything else as an error
        else:
            icon = Icons.CHECK_UPDATES_FAILED
            Notify.init("checkupdates command failed")
            NotificationTotalUpdates = Notify.Notification.new("checkupdates command failed", "checkupdates command failed", icon)
            NotificationTotalUpdates.show()
            
        self.SetStatusIcon(icon)
        
    def InstallUpdates(self, data = None):
        os.system("{} -e 'bash -c \"{}; read -p \\\"Press enter to close terminal\\\"\"'".format(self.Terminal, self.UpdateCmd))
        self.CheckUpdates()
    
    def do_activate(self):
        Gtk.Application.do_activate(self)
        self.hold()
        self.CreatePopupMenu()
        
    def do_statusicon(self, icon, x, y, button, time, panel_position):
        
        menu = Gtk.Menu()
        
        item = Gtk.MenuItem(label="Check now")
        item.connect("activate", self.CheckUpdates)
        menu.append(item)
        
        item = Gtk.MenuItem(label="Install")
        item.connect("activate", self.InstallUpdates)
        menu.append(item)
        
        item = Gtk.MenuItem(label="About")
        item.connect("activate", self.AboutDialog)
        menu.append(item)
        
        item = Gtk.MenuItem(label="Quit")
        item.connect("activate", self.QuitApplication)
        menu.append(item)
        
        menu.show_all()
        icon.popup_menu(menu, x, y, button, time, panel_position)

    def QuitApplication(self, window = None, data = None):
        self.quit()
        
    def AboutDialog(self, data = None):
        self.dialog = Gtk.AboutDialog()
        self.dialog.set_title("AboutDialog")
        self.dialog.set_program_name("Arch Update Indicator")
        self.dialog.set_version(ARCHUPDATE_INDICATOR_VERSION)
        self.dialog.set_comments("Creates a XApp StatusIcon that indicates if updates are available and provides a context menu to inspect and install them")
        self.dialog.set_website("https://github.com/SantiBurgos1089/archupdate-indicator")
        self.dialog.set_website_label("Arch Update Indicator")
        self.dialog.set_authors(["Santiago Burgos","epsilontheta"])
        self.dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(Icons.NO_UPDATES, 64, 64))
        self.dialog.connect('response', lambda dialog, data: dialog.destroy())
        self.dialog.show()
        
    def TimerApplication(self, data = None):
        GLib.timeout_add_seconds(UPDATE_PERIOD, self.CheckUpdates)
        return GLib.SOURCE_CONTINUE

if __name__ == '__main__':
    archtray = Application()
    archtray.run()