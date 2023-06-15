#!/usr/bin/env python3
# Display an error message in i3

import subprocess

def _display_error_message(error_message):
    subprocess_result = subprocess.run(['i3-nagbar','-t','error','-m',error_message], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# display_error_message("hej hopp")
