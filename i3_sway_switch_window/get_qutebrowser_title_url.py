# Try to get a list of titles and URLs from qutebrowser.

import os
import psutil
import re
import subprocess
import yaml

import i3_sway_switch_window.display_error_message

timeout_seconds = 5
session_path = "~/.local/share/qutebrowser/sessions/default.yml"

def _checkIfProcessRunning(processName):
    '''Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the running process's
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def _get_qutebrowser_title_url():
    """Try to get a list of titles and URLs from qutebrowser.

    This function does nothing, if qutebrowser is not running.
    The list is returned formated similarly to brotab command "bt list", but without the first column.
    """
    if not _checkIfProcessRunning('qutebrowser'):
        return []

    success = 1
    try:
        # Try to save default qutebrowser session to a file.
        subprocess_load_result = subprocess.run(['qutebrowser', '--nowindow', ':session-save'],
                                                capture_output=True,
                                                encoding="utf-8", check=True, timeout=timeout_seconds)
    except FileNotFoundError as exc:
        success = 0
        error_message = f"Process failed because the executable could not be found.\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
    except subprocess.CalledProcessError as exc:
        success = 0
        error_message = f"Process failed because did not return a successful return code: {exc.returncode}\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
    except subprocess.TimeoutExpired as exc:
        success = 0
        error_message = f"Process timed out.\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)

    if success:
        default_session_path = os.path.expanduser(session_path)
        if not os.path.exists(default_session_path):
            return []
        title_list = []
        with open(default_session_path, 'r') as file:
            qutebrowser_windows = yaml.safe_load(file)
            for key, value in qutebrowser_windows.items():
                for window in value:
                    for tab in window['tabs']:
                        if 'history' in tab:
                            for hist_item in tab['history']:
                                if 'active' in hist_item and 'title' in hist_item and 'url' in hist_item and hist_item['url'].find('https://') == 0:
                                    title_list.append(hist_item['title'] + '  ' + hist_item['url'])

        # Make a sorted list, without duplicates
        set_res = set(title_list)
        title_list = sorted(list(set_res), key=str.casefold)
        return title_list
    else:
        return []
