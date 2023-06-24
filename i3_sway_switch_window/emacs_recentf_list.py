#!/usr/bin/env python3
# Get current recentf (recently opened files) list from emacs.
# The list is sorted case insensitive.

# Note to developer: All error messages are to be presented to the user in one (well known) place.

import subprocess
import i3_sway_switch_window.display_error_message

def _emacs_recentf_list():
    """Return recentf (recently opened files) list from emacs.

    The list is in the same order as in emacs: from most recently accessed file, to least recently accessed file.
    """
    try:
        subprocess_result = subprocess.run(['emacs','--batch',
                                            '--eval',"(require 'server)",
                                            '--eval',"(mapc #'princ (read (server-eval-at \"server\" '(prin1-to-string (mapcar (lambda (buffer) (format \"%s\\n\" buffer)) recentf-list)))))"],
                                           capture_output=True, encoding="utf-8", check=True, timeout=5)
    except FileNotFoundError as exc:
        error_message = f"Process failed because the executable could not be found.\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
        return []
    except subprocess.CalledProcessError as exc:
        error_message = f"Process failed because did not return a successful return code: {exc.returncode}\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
        return []
    except subprocess.TimeoutExpired as exc:
        error_message = f"Process timed out.\n{exc}"
        i3_sway_switch_window.display_error_message._display_error_message(error_message)
        return []

    # print(subprocess_result.stdout)
    recentf_list = list(subprocess_result.stdout.split("\n"))
    recentf_list = [token for token in recentf_list if len(token) > 0]
    # recentf_list.sort(key=str.casefold)
    return recentf_list
