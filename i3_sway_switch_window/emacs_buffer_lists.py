#!/usr/bin/env python3
# Get current list of buffers from emacs. Save buffer names into lists:
# - All interesting buffers (files and internal buffers)
# - All file buffers
# - All interesting internal buffers
# All lists are sorted case insensitive.

# Note to developer: All error messages are to be presented to the user in one (well known) place.

import subprocess
import i3_sway_switch_window.display_error_message

def _emacs_buffer_lists():
    """Return tree lists of the buffer names in emacs: All interesting buffers, file buffers, internal buffers.

    The lists are sorted case insensitive. Buffer names starting with a space character, are excluded.
    """
    try:
        # Command copied from https://blog.lambda.cx/posts/emacs-buffers-to-stdout/
        subprocess_result = subprocess.run(['emacs','--batch',
                                            '--eval',"(require 'server)",
                                            '--eval',"(mapc #'princ (read (server-eval-at \"server\" '(prin1-to-string (mapcar (lambda (buffer) (format \"%s\\n\" buffer)) (buffer-list))))))"],
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
    all_buffers = list(subprocess_result.stdout.split("\n"))
    interesting_buffers = [token for token in all_buffers if len(token) > 0 and token[0] != ' ']
    interesting_buffers.sort(key=str.casefold)
    file_buffers = [token for token in interesting_buffers if token[0] != '*']
    internal_buffers = [token for token in interesting_buffers if token[0] == '*']
    return [interesting_buffers, file_buffers, internal_buffers]
