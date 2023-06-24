# i3-sway-switch-window

<div align="center">

[![Build status](https://github.com/johanwiden/i3-sway-switch-window/workflows/build/badge.svg?branch=master&event=push)](https://github.com/johanwiden/i3-sway-switch-window/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/i3-sway-switch-window.svg)](https://pypi.org/project/i3-sway-switch-window/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/johanwiden/i3-sway-switch-window/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/johanwiden/i3-sway-switch-window/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/johanwiden/i3-sway-switch-window/releases)
[![License](https://img.shields.io/github/license/johanwiden/i3-sway-switch-window)](https://github.com/johanwiden/i3-sway-switch-window/blob/master/LICENSE)

In i3wm, or sway, replace currently focused window with emacs buffer, file from emacs recentf, browser window showing URL from a browser tab, or another window.
Can also place selected buffer window, recentf window, browser tab, or another window, adjacent to currently focused window.
Emacs buffer and file from emacs recentf are displayed with emacsclient. Currently only tested under Ubuntu 23.04.

</div>

## Installation

```bash
pipx install -U i3-sway-switch-window
```

It is necessary to install with 'pipx' rather than 'pip', as a number of command line entry points are included in the package.

Then you can run

```bash
browser_tab -h
emacs_buffers -h
emacs_recentf -h
wm_window_switch -h
```

To uninstall the package run:
```bash
pipx uninstall i3-sway-switch-window
```

Install requirements:

To use commands emacs_buffers and emacs_recentf, emacs must be running in server (daemon) mode. emacsclient must be available.

To use browser_tab, brotab must be installed. See https://github.com/balta2ar/brotab for how to install the command line application.
You must also have the brotab browser extensiom installed in your browser, and enabled.

Note that the brotab command line application 'bt', is currently unable to communicate with browsers installed via flatpak and snap.
On Ubuntu I have had success with the vivaldi browser. It is still possible to open the URLs with for example chrome.
Note 2023-06-22: bt now works also with chrome on Ubuntu.

The i3-sway-switch-window applications expect to find a configuration file in "i3_sway_switch_window/config.ini" in your config directory.
The file can be empty.

A sample config.ini is:
```bash
[roficommand]
# Default is "rofi -dmenu"
roficommand = /usr/local/bin/rofi -dmenu

[webbrowser]
# Default is "vivaldi"
webbrowser = google-chrome

[workspace]
# i3, or sway, workspace to which focused window will be swapped
# Default is "2"
swap_workspace = 9
```

## How to use
The commands can be run from the command line. They can also be part of the i3, or sway, configuration.
Here are some sample lines from my i3 configuration file:
```bash
# get wm window names, select one, display at current desktop window
bindsym $mod+w exec ~/.local/bin/wm_window_switch swap

# get wm window names, select one, display next to current desktop window
bindsym $mod+Shift+w exec ~/.local/bin/wm_window_switch add

# get web browser tab titles and URLs, select one, display at current desktop window
bindsym $mod+u exec ~/.local/bin/browser_tab swap

# get web browser tab titles and URLs, select one, display next to current desktop window
bindsym $mod+Shift+u exec ~/.local/bin/browser_tab add

# get current buffers from emacs, select one, display at current desktop window
bindsym $mod+b exec ~/.local/bin/emacs_buffers swap

# get current buffers from emacs, select one, display next to current desktop window
bindsym $mod+Shift+b exec ~/.local/bin/emacs_buffers add

# get recentf list from emacs, select one, display at current desktop window
bindsym $mod+r exec ~/.local/bin/emacs_recentf swap

# get recentf list from emacs, select one, display next to current desktop window
bindsym $mod+Shift+r exec ~/.local/bin/emacs_recentf add
```

Note for sway: An alternative to wm_window_switch is to use swayr command 'swap-focused-with', see https://sr.ht/~tsdh/swayr

## Developer info

To build the package:
- Download the repo. E.g. git clone https://github.com/johanwiden/i3-sway-switch-window.git
- Create a virtual environment, for development. E.g. with conda
  - conda create --name i3env
  - conda activate i3env
  - conda install -c anaconda pip
  - pip install i3ipc
    This is a package dependency
  - pip install build
    This is the tool to build the package.
- Change directory to the downloaded repo
- python3 -m build
    This should build the package, the result is stored in subdirectory 'dist'

### Running the applications
One can execute the entry points directly in the development environment, from the repo directory, without installing the package:
- python3 -c "import i3_sway_switch_window.main; import sys; sys.argv = [sys.argv[0]] + ['swap']; i3_sway_switch_window.main.cli_browser_tab()"
- python3 -c "import i3_sway_switch_window.main; import sys; sys.argv = [sys.argv[0]] + ['--browser','google-chrome','add']; i3_sway_switch_window.main.cli_browser_tab()"
- python3 -c "import i3_sway_switch_window.main; import sys; sys.argv = [sys.argv[0]] + ['--config','foo']; i3_sway_switch_window.main.cli_browser_tab()"
- python3 -c "import i3_sway_switch_window.main; import sys; sys.argv = [sys.argv[0]] + ['--version']; i3_sway_switch_window.main.cli_browser_tab()"

To test installation of the package:
- From outside the virtual environment, or in a different virtual environment:
  - Install pipx, if it is not already installed.
  - pipx ensurepath
    Ensure directories necessary for pipx operation are in your PATH environment variable.
  - pipx install --force PATH-TO-REPO/dist/i3_sway_switch_window-0.1.0.tar.gz
  - One should now be able to execute the apps. They are usually stored in ~/.local/bin.

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/johanwiden/i3-sway-switch-window/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/johanwiden/i3-sway-switch-window/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/johanwiden/i3-sway-switch-window)](https://github.com/johanwiden/i3-sway-switch-window/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/johanwiden/i3-sway-switch-window/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{i3-sway-switch-window,
  author = {Johan Widén},
  title = {In i3wm replace current window with emacs buffer, emacs recentf file, or browser tab},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/johanwiden/i3-sway-switch-window}}
}
```
