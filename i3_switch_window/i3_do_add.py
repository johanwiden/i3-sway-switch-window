#!/usr/bin/env python3
# Create a new window adjacent to the currently focused window.

from i3ipc import Connection, Event

i3 = Connection()

# A callback for when a new window has been reparented in i3
def __on_new_window(self, e):
    # The first parameter is the connection to the ipc and the second is an object
    # with the data of the event sent from i3.
    # i3.command('focus prev')
    # i3.command('move container to workspace 2')
    i3.main_quit()

def _do_add(command_file_name):
    i3.on(Event.WINDOW_NEW, __on_new_window)
    i3.command('exec ' + command_file_name)
    # main event loop, with timeout 3 seconds
    i3.main(3.0)
