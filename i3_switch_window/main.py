#!/usr/bin/env python3

import sys
import os.path
import stat
import subprocess
import tempfile

import i3_switch_window.display_error_message
import i3_switch_window.emacs_buffer_lists
import i3_switch_window.emacs_recentf_list
import i3_switch_window.i3_do_add
import i3_switch_window.i3_do_switch
import i3_switch_window.__version__

def _select_item_and_switch(add_or_swap_window, item_list, command_prefix, command_suffix):
    if len(item_list) > 0:
        success = 1
        with tempfile.TemporaryFile() as temp_fp:
            for item in item_list:
                line = item + "\n"
                temp_fp.write(bytes(line,'utf-8'))
            temp_fp.seek(0)
            try:
                subprocess_result = subprocess.run(['rofi', '-dmenu'], stdin=temp_fp, capture_output=True, encoding="utf-8", check=True)
            except FileNotFoundError as exc:
                success = 0
                error_message = f"Process failed because the executable could not be found.\n{exc}"
                i3_switch_window.display_error_message._display_error_message(error_message)
            except subprocess.CalledProcessError as exc:
                success = 0
                error_message = f"Process failed because did not return a successful return code: {exc.returncode}\n{exc}"
                i3_switch_window.display_error_message._display_error_message(error_message)
            except subprocess.TimeoutExpired as exc:
                success = 0
                error_message = f"Process timed out.\n{exc}"
                i3_switch_window.display_error_message._display_error_message(error_message)

        if success:
            file_selected = list(subprocess_result.stdout.split("\n"))
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
                        i3_switch_window.i3_do_add._do_add(temp_file_name)
                    else:
                        i3_switch_window.i3_do_switch._do_switch(temp_file_name)

def switch_in_emacs_buffer(add_or_swap_window):
    """Get current buffers from emacs (files and internal buffers). Select one, display it in desktop window.

    Use rofi to select buffer. The window is displayed instead of the currently focused window.
    The currently focused window is moved to a different workspace.
    """
    [interesting_buffers, file_buffers, internal_buffers] = i3_switch_window.emacs_buffer_lists._emacs_buffer_lists()
    command_prefix = "emacsclient -nc -e '(let ((display-buffer-alist '\\''((\".*\" display-buffer-same-window)))) (pop-to-buffer \""
    command_suffix = "\" nil t))'\n"
    _select_item_and_switch(add_or_swap_window, interesting_buffers, command_prefix, command_suffix)

def switch_in_emacs_recentf(add_or_swap_window):
    """Get current recentf filepaths from emacs. Select one, display it in desktop window.

    Use rofi to select buffer. The window is displayed instead of the currently focused window.
    The currently focused window is moved to a different workspace.
    """
    recentf_list = i3_switch_window.emacs_recentf_list._emacs_recentf_list()
    command_prefix = "emacsclient -nc "
    command_suffix = "\n"
    _select_item_and_switch(add_or_swap_window, recentf_list, command_prefix, command_suffix)

def cli_emacs_buffers():
    """Called from commandline: See section [project.scripts] in pyproject.toml.
    """
    if '--version' in sys.argv[1:]:
        print(i3_switch_window.__version__.__version__)
        exit(0)
    elif 'add' in sys.argv[1:]:
        switch_in_emacs_buffer('add')
    else:
        switch_in_emacs_buffer('swap')

def cli_emacs_recentf():
    """Called from commandline: See section [project.scripts] in pyproject.toml.
    """
    if '--version' in sys.argv[1:]:
        print(i3_switch_window.__version__.__version__)
        exit(0)
    elif 'add' in sys.argv[1:]:
        switch_in_emacs_recentf('add')
    else:
        switch_in_emacs_recentf('swap')
