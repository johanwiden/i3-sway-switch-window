#!/usr/bin/env python3
# Get current list of top level windows, from window manager.
# The list is sorted case insensitive.

# Note to developer: All error messages are to be presented to the user in one (well known) place.

import i3ipc

def _wm_window_list():
    """Return [focused_window.id, filtered_window_names].

    filtered_window_names is a list of top level window names, from window manager.
    The currently focused window is not included in the list.
    Each list element has the window id appended.
    The list is sorted case insensitive.
    """
    i3 = i3ipc.Connection()
    i3_tree = i3.get_tree()
    if not i3_tree:
        return []
    # Find currently focused window, in currently focused workspace
    focused_window = i3_tree.find_focused()
    if not focused_window:
        return []
    # print('Focused window %s %d is on workspace %s' %
    #       (focused_window.name, focused_window.id, focused_window.workspace().name))
    containers = i3_tree.leaves()
    # Do not include focused container
    filtered_containers = [c for c in containers if c.id != focused_window.id]
    filtered_names = [c.name + ' ' + str(c.id) for c in filtered_containers]
    if len(filtered_names) == 0:
        return []
    filtered_names.sort(key=str.casefold)
    return [focused_window.id, filtered_names]
