#!/usr/bin/env python3
# Get current list of web browser tab titles and URLs.
# The list is filtered for items containing string 'https://''
#   To support other tabs we have to ensure we use the same web browser the tab comes from.
# The list is sorted case insensitive.

# Note to developer: All error messages are to be presented to the user in one (well known) place.

import re
import subprocess
import i3_sway_switch_window.display_error_message

def _browser_tab_list():
    """Return list of web browser tab titles and URLs.

    The first column (tab ID), of each list item, is removed. The list is sorted case insensitive.
    """
    try:
        subprocess_result = subprocess.run(['bt','list'],
                                           capture_output=True, encoding="utf-8", check=True, timeout=5)
    except FileNotFoundError as exc:
        error_message = f"Process failed because the executable could not be found.\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
        return [[],[],[]]
    except subprocess.CalledProcessError as exc:
        error_message = f"Process failed because did not return a successful return code: {exc.returncode}\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
        return [[],[],[]]
    except subprocess.TimeoutExpired as exc:
        error_message = f"Process timed out.\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
        return [[],[],[]]

    # print(subprocess_result.stdout)
    all_tabs = list(subprocess_result.stdout.split("\n"))
    all_tabs = [re.sub(r'^\S+\s', '', token) for token in all_tabs] # Remove tab ID column
    web_tabs = [token for token in all_tabs if 'https://' in token]
    web_tabs.sort(key=str.casefold)
    return web_tabs
