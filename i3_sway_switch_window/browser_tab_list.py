#!/usr/bin/env python3
# Get current list of web browser tab titles and URLs.
# The list is filtered for items containing string 'https://''
#   To support other tabs we have to ensure we use the same web browser the tab comes from.
# The list is sorted case insensitive.

# Note to developer: All error messages are to be presented to the user in one (well known) place.

import re
import subprocess
import i3_sway_switch_window.get_nyxt_title_url
import i3_sway_switch_window.get_qutebrowser_title_url
import i3_sway_switch_window.display_error_message

def _browser_tab_list(get_urls_from_nyxt, get_urls_from_qutebrowser):
    """Return list of web browser tab titles and URLs.

    If get_urls_from_nyxt is True then also try to get titles and URLs from nyxt browser.
    If get_urls_from_qutebrowser is True then also try to get titles and URLs from qutebrowser.
    The first column (tab ID), of each list item, is removed. The list is sorted case insensitive.
    """
    success = 1
    try:
        subprocess_result = subprocess.run(['bt','list'],
                                           capture_output=True, encoding="utf-8", check=True, timeout=5)
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
        all_tabs = list(subprocess_result.stdout.split("\n"))
        all_tabs = [re.sub(r'^\S+\s', '', token) for token in all_tabs] # Remove tab ID column
        # Filter out internal URIs
        web_tabs = [token for token in all_tabs if 'https://' in token]
        # Standardise number of spaces before https://
        web_tabs = [re.sub(r'\s+https://', r'  https://', token) for token in web_tabs]
        if get_urls_from_nyxt:
            web_tabs = web_tabs + i3_sway_switch_window.get_nyxt_title_url._get_nyxt_title_url()
        if get_urls_from_qutebrowser:
            web_tabs = web_tabs + i3_sway_switch_window.get_qutebrowser_title_url._get_qutebrowser_title_url()
        # Make a sorted list, without duplicates
        set_res = set(web_tabs)
        web_tabs = sorted(list(set_res), key=str.casefold)
        return web_tabs
    else:
        return []
