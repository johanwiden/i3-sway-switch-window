#!/usr/bin/env python3

import sys
import os.path
import argparse
import re
import stat
import subprocess
import tempfile

import i3_sway_switch_window.config
import i3_sway_switch_window.display_error_message
import i3_sway_switch_window.browser_tab_list
import i3_sway_switch_window.emacs_buffer_lists
import i3_sway_switch_window.emacs_recentf_list
import i3_sway_switch_window.wm_window_list
import i3_sway_switch_window.i3_do_add
import i3_sway_switch_window.i3_do_switch
import i3_sway_switch_window.__version__

# Possible to change in config file
roficommand = 'rofi -dmenu'
webbrowser = 'vivaldi' # Default value
swap_workspace = '2'

def _select_item_and_switch(add_or_swap_window, focused_window_id, window_name_list):
    """Call 'rofi' to select an item from 'window_name_list'. Swap in or move window at focused window.

    Parameters:
    - add_or_swap_window:
      - add: The selected window is displayed next to currently focused window.
      - swap: The window is displayed instead of the currently focused window.
              The currently focused window is moved to a different workspace.
    - focused_window_id: The wm window id for the currently focused window.
    - window_name_list: List of window names. Each item in the list has the wm window id appended.
    """
    if len(window_name_list) > 0:
        success = 1
        with tempfile.TemporaryFile() as temp_fp:
            for item in window_name_list:
                line = item + "\n"
                temp_fp.write(bytes(line,'utf-8'))
            temp_fp.seek(0)
            try:
                subprocess_result = subprocess.run(roficommand.split(), stdin=temp_fp, capture_output=True, encoding="utf-8", check=True)
            except FileNotFoundError as exc:
                success = 0
                error_message = f"Process failed because the executable could not be found.\n{exc}"
                i3_sway_switch_window.display_error_message._display_error_message(error_message)
            except subprocess.CalledProcessError as exc:
                success = 0
                if exc.returncode != 1:
                    error_message = f"Process failed because did not return a successful return code: {exc.returncode}\n{exc}"
                    i3_sway_switch_window.display_error_message._display_error_message(error_message)
            except subprocess.TimeoutExpired as exc:
                success = 0
                error_message = f"Process timed out.\n{exc}"
                i3_sway_switch_window.display_error_message._display_error_message(error_message)

        if success:
            name_selected = list(subprocess_result.stdout.split("\n"))
            name_selected = [token for token in name_selected if len(token) > 0]
            if len(name_selected) == 1:
                selected_window_id_str = re.sub(r'.* (\d+)$', r'\1', name_selected[0])
                selected_window_id = int(selected_window_id_str)
                if add_or_swap_window == 'add':
                    i3_sway_switch_window.i3_do_add._do_move(focused_window_id, selected_window_id)
                else:
                    i3_sway_switch_window.i3_do_switch._do_switch(focused_window_id, selected_window_id,
                                                                  swap_workspace)

def _select_item_execute_and_switch(add_or_swap_window, item_list,
                                    command_prefix, command_suffix,
                                    match_expr,
                                    substitution_expr):
    """Call 'rofi' to select an item from 'item_list'. Execute command with selected item.

    The command is supposed to create a new desktop window. Parameters:
    - add_or_swap_window:
      - add: The new window is displayed next to currently focused window.
      - swap: The window is displayed instead of the currently focused window.
              The currently focused window is moved to a different workspace.
    - item_list: List of strings, from which rofi shall select one string.
    - command_prefix, command_suffix: The command to be executed is the concatenation of
      command_prefix, selected item, command suffix
    - match_expr, substitution_expr: Regular expressions to clean selected string. Can be the empty string.
    """
    if len(item_list) > 0:
        success = 1
        with tempfile.TemporaryFile() as temp_fp:
            for item in item_list:
                line = item + "\n"
                temp_fp.write(bytes(line,'utf-8'))
            temp_fp.seek(0)
            try:
                subprocess_result = subprocess.run(roficommand.split(), stdin=temp_fp, capture_output=True, encoding="utf-8", check=True)
            except FileNotFoundError as exc:
                success = 0
                error_message = f"Process failed because the executable could not be found.\n{exc}"
                i3_sway_switch_window.display_error_message._display_error_message(error_message)
            except subprocess.CalledProcessError as exc:
                success = 0
                if exc.returncode != 1:
                    error_message = f"Process failed because did not return a successful return code: {exc.returncode}\n{exc}"
                    i3_sway_switch_window.display_error_message._display_error_message(error_message)
            except subprocess.TimeoutExpired as exc:
                success = 0
                error_message = f"Process timed out.\n{exc}"
                i3_sway_switch_window.display_error_message._display_error_message(error_message)

        if success:
            file_selected = list(subprocess_result.stdout.split("\n"))
            if match_expr != '':
                file_selected = [re.sub(match_expr, substitution_expr, token) for token in file_selected]
            file_selected = [token for token in file_selected if len(token) > 0 and token[0] != ' ']
            if len(file_selected) == 1:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file_name = os.path.join(temp_dir, 'open-command.sh')
                    with open(temp_file_name, 'w') as file_handle:
                        line = "#/usr/bin/env/bash\n"
                        file_handle.write(line)
                        file_handle.write(command_prefix)
                        file_handle.write(file_selected[0])
                        file_handle.write(command_suffix)
                    os.chmod(temp_file_name, stat.S_IXUSR | stat.S_IRUSR)
                    if add_or_swap_window == 'add':
                        i3_sway_switch_window.i3_do_add._do_execute_and_add(temp_file_name)
                    else:
                        i3_sway_switch_window.i3_do_switch._do_execute_and_switch(temp_file_name, swap_workspace)

def switch_in_emacs_buffer(add_or_swap_window):
    """Get current buffers from emacs (files and internal buffers). Select one, display it in desktop window.

    Use rofi to select buffer. Display with emacsclient. Parameter 'add_or_swap_window':
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.
    """
    [interesting_buffers, file_buffers, internal_buffers] = i3_sway_switch_window.emacs_buffer_lists._emacs_buffer_lists()
    command_prefix = "emacsclient -nc -e '(let ((display-buffer-alist '\\''((\".*\" display-buffer-same-window)))) (pop-to-buffer \""
    command_suffix = "\" nil t))'\n"
    _select_item_execute_and_switch(add_or_swap_window, interesting_buffers,
                                    command_prefix, command_suffix,
                                    r'', r'')

def switch_in_emacs_recentf(add_or_swap_window):
    """Get current recentf filepaths from emacs. Select one, display it in desktop window.

    Use rofi to select file. Display with emacsclient. Parameter 'add_or_swap_window':
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.
    """
    recentf_list = i3_sway_switch_window.emacs_recentf_list._emacs_recentf_list()
    command_prefix = "emacsclient -nc "
    command_suffix = "\n"
    _select_item_execute_and_switch(add_or_swap_window, recentf_list,
                                    command_prefix, command_suffix,
                                    r'', r'')

# TODO: Optionally close original tab
def switch_in_browser_tab(add_or_swap_window):
    """Get browser tab titles and URLs. Select one, display it in desktop window.

    Use rofi to select URL. Display with web browser. Parameter 'add_or_swap_window':
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.
    """
    tab_list = i3_sway_switch_window.browser_tab_list._browser_tab_list()
    command_prefix = webbrowser + " --new-window "
    command_suffix = "\n"
    _select_item_execute_and_switch(add_or_swap_window, tab_list,
                                    command_prefix, command_suffix,
                                    r'.*h(ttps://\S+)\s*$', r"'h\1'")

def switch_in_wm_window(add_or_swap_window):
    """Use rofi to select a top level wm window (container) from a list. Move window to/near focused window.

    Parameter 'add_or_swap_window':
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.
    """
    list_focused_names = i3_sway_switch_window.wm_window_list._wm_window_list()
    if len(list_focused_names) > 0:
        focused_window_id = list_focused_names[0]
        # print('focused window id: ', focused_window_id)
        filtered_names = list_focused_names[1]
        # for name in filtered_names:
        #     print(name)
        _select_item_and_switch(add_or_swap_window, focused_window_id, filtered_names)

def _parse_command_line_and_read_config():
    """Parse command line and get values from config file.
    """
    parser = argparse.ArgumentParser(
                    prog = i3_sway_switch_window.__version__.__title__,
                    description = i3_sway_switch_window.__version__.__description__)
    parser.add_argument('--version', required = False, action="store_true")
    parser.add_argument('--config', required = False, type=str)
    parser.add_argument('--browser', required = False, type=str)
    parser.add_argument('action', nargs='?', choices = ['add', 'swap'], default = 'swap')
    args = parser.parse_args()
    if args.version:
        print("Python package: ", i3_sway_switch_window.__version__.__title__, " ",
              i3_sway_switch_window.__version__.__version__)
        exit(0)
    config_path = ''
    if args.config:
        config_path = args.config
    if not i3_sway_switch_window.config._read_config_file(config_path):
        exit(1)
    config_roficommand = i3_sway_switch_window.config._get_value('roficommand', 'roficommand')
    config_webbrowser = i3_sway_switch_window.config._get_value('webbrowser', 'webbrowser')
    config_swap_workspace = i3_sway_switch_window.config._get_value('workspace', 'swap_workspace')
    global roficommand
    global webbrowser
    global swap_workspace
    if len(config_roficommand) > 0:
        roficommand = config_roficommand
    if args.browser:
        webbrowser = args.browser
    elif len(config_webbrowser) > 0:
        webbrowser = config_webbrowser
    if len(config_swap_workspace) > 0:
        swap_workspace = config_swap_workspace
    return args.action

def cli_emacs_buffers():
    """Use rofi to select an emacs buffer. Open emacsclient with selected buffer.

    Command line arguments:
    - --version: Display package version.
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.

    Called from command line: See section [project.scripts] in pyproject.toml.
    """
    action = _parse_command_line_and_read_config()
    switch_in_emacs_buffer(action)

def cli_emacs_recentf():
    """Use rofi to select path from emacs recentf. Open emacsclient with selected file.

    recentf is emacs list of recently opened files. Command line arguments:
    - --version: Display package version.
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.

    Called from command line: See section [project.scripts] in pyproject.toml.
    """
    action = _parse_command_line_and_read_config()
    switch_in_emacs_recentf(action)

def cli_browser_tab():
    """Use rofi to select a URL from list of web browser tabs. Open a browser window with URL.

    Command line arguments:
    - --version: Display package version.
    - add: Show the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.

    Called from command line: See section [project.scripts] in pyproject.toml.
    """
    action = _parse_command_line_and_read_config()
    switch_in_browser_tab(action)

def cli_wm_window_switch():
    """Use rofi to select a top level wm window (container) from a list. Move window to/near focused window.

    Command line arguments:
    - --version: Display package version.
    - add: Move the window next to the currently focused window.
    - swap: The window is displayed instead of the currently focused window.
            The currently focused window is moved to a different workspace.

    Called from command line: See section [project.scripts] in pyproject.toml.
    """
    action = _parse_command_line_and_read_config()
    switch_in_wm_window(action)
