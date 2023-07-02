# Try to get a list of titles and URLs from the nyxt web browser.

import psutil
import re
import subprocess

import i3_sway_switch_window.display_error_message

timeout_seconds = 5

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

def _get_nyxt_title_url():
    """Try to get a list of titles and URLs from nyxt.

    This function does nothing, if nyxt is not running.
    The list is returned formated similarly to brotab command "bt list", but without the first column.

    Requires tha emacs runs as a daemon, and that https://github.com/ag91/emacs-with-nyxt is loaded in
    emacs, or can be loaded with elisp function 'load-emacs-with-nyxt'.
    Requires that nyxt is configured to start a slynk server. In nyxt config.lisp add: (start-slynk)
    """
    if not _checkIfProcessRunning('nyxt'):
        return []

    success = 1
    try:
        # Try to load emacs-with-nyxt into emacs. Does nothing if function not defined, or if emacs-with-nyxt is
        # already loaded.
        subprocess_load_result = subprocess.run(['emacsclient', '-e',
                                                 "(if (fboundp 'load-emacs-with-nyxt) (load-emacs-with-nyxt))"],
                                                capture_output=True,
                                                encoding="utf-8", check=True, timeout=timeout_seconds)
        # Ensure that emacs has a slynk connection to nyxt.
        subprocess_connect_result = subprocess.run(['emacsclient', '-e',
                                                    '(unless (emacs-with-nyxt-connected-p) (emacs-with-nyxt-start-and-connect-to-nyxt))'],
                                                   capture_output=True,
                                                   encoding="utf-8", check=True, timeout=timeout_seconds)
        # Get list of buffer titles and URLs, from nyxt.
        subprocess_result = subprocess.run(['emacsclient', '-e',
                                            "(emacs-with-nyxt-send-sexps '(map 'list (lambda (el) (list (slot-value el 'title) (slot-value el 'url))) (buffer-list)))"],
                                           capture_output=True, encoding="utf-8", check=True, timeout=timeout_seconds)
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
        title_url_list = subprocess_result.stdout.split(")\\n")

        # Clean first and last item in list
        if len(title_url_list) > 0 and len(title_url_list[0]) > 2:
            item = title_url_list[0]
            title_url_list[0] = " " + item[2:]
            title_url_list[-1] = title_url_list[-1][:-4]
        # Filter out internal URIs
        title_url_list = [token for token in title_url_list if '#<QURI.URI:URI' not in token]
        # Create a list of 'tile  URL' formatted similarly to brotab command 'bt list'
        title_list = []
        for item in title_url_list:
            title = re.sub(r'^....(.+)\\"\\n\s+#<QURI.*$', r'\1', item)
            title = re.sub(r'\\\\\\"', r'"', title)
            url = re.sub(r'^.*:URI-HTTPS (.*)>$', r'\1', item)
            title_list.append(title + '  ' + url)

        # Make a sorted list, without duplicates
        set_res = set(title_list)
        title_list = sorted(list(set_res), key=str.casefold)
        return title_list
    else:
        return []
