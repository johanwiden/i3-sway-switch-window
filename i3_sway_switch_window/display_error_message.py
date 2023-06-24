#!/usr/bin/env python3
# Display an error message in i3 or sway

import os
import subprocess

def _display_error_message(error_message):
    if os.environ.get('XDG_SESSION_TYPE') and os.environ['XDG_SESSION_TYPE'] == 'wayland':
        subprocess_result = subprocess.run(['swaynag','-t','error','-m',error_message], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    else:
        subprocess_result = subprocess.run(['i3-nagbar','-t','error','-m',error_message], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
