#!/usr/bin/env python3

import configparser
import os

import i3_sway_switch_window.__version__

parser = configparser.ConfigParser()

def _read_config_file(config_file_path):
    """Read and parse config file. config_file_path is uesed, if non empty.
    """
    file_path = ''
    if len(config_file_path) > 0:
        file_path = config_file_path
    else:
        config_path_suffix = os.path.join(i3_sway_switch_window.__version__.__title__, 'config.ini')
        possible_config_paths = []
        if 'APPDATA' in os.environ:
            path = os.path.join(os.environ['APPDATA'], config_path_suffix)
            possible_config_paths.append(path)

        if 'XDG_CONFIG_HOME' in os.environ:
            path = os.path.join(os.environ['XDG_CONFIG_HOME'], config_path_suffix)
            possible_config_paths.append(path)

        if 'HOME' in os.environ:
            path = os.path.join(os.environ['HOME'], ".config", config_path_suffix)
            possible_config_paths.append(path)

        if 'XDG_CONFIG_DIRS' in os.environ:
            path_list = os.environ['XDG_CONFIG_DIRS'].split(':')
            for path in path_list:
                possible_config_paths.append(os.path.join(path, config_path_suffix))

        for path in possible_config_paths:
            if os.path.exists(path):
                file_path = path
                break

    if len(file_path) == 0:
        i3_sway_switch_window.display_error_message._display_error_message('Config file ' + config_path_suffix + ' not found')
        return False
    elif not os.path.exists(file_path):
        i3_sway_switch_window.display_error_message._display_error_message('Config file ' + file_path + ' not found')
        return False

    return len(parser.read(file_path)) > 0

def _get_value(section, key):
    """Try to get a value from config file. If not found, the empty string is returned.
    """
    if parser.has_option(section, key):
        return parser[section][key]
    else:
        return ''
