# i3-switch-window

<div align="center">

[![Build status](https://github.com/johanwiden/i3-switch-window/workflows/build/badge.svg?branch=master&event=push)](https://github.com/johanwiden/i3-switch-window/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/i3-switch-window.svg)](https://pypi.org/project/i3-switch-window/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/johanwiden/i3-switch-window/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/johanwiden/i3-switch-window/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/johanwiden/i3-switch-window/releases)
[![License](https://img.shields.io/github/license/johanwiden/i3-switch-window)](https://github.com/johanwiden/i3-switch-window/blob/master/LICENSE)

In i3wm replace current window with emacs buffer, file from emacs recentf, or browser window showing URL from a browser tab.
Emacs buffer and file from emacs recentf are displayed with emacsclient. Currently only tested under Ubuntu 23.04. 

</div>

5. Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/johanwiden/i3-switch-window.git
git push -u origin main
```

## Installation

```bash
pipx install -U i3-switch-window
```

It is necessary to install with 'pipx' rather than 'pip', as a number of command line entry points are included in the package.

Then you can run

```bash
browser_tab -h
emacs_buffers -h
emacs_recentf -h
```

To unistall the package run:
```bash
pipx uninstall i3-switch-window
```

Install requirements:

To use commands emacs_buffers and emacs_recentf, emacs must be running in server (daemon) mode. emacsclient must be available.

To use browser_tab, brotab must be installed. See https://github.com/balta2ar/brotab for how to install the command line application.
You must also have the brotab browser extensiom installed in your browser, and enabled.

Note that the brotab command line application 'bt', is currently unable to communicate with browsers installed via flatpak and snap.
On Ubuntu I have had success with the vivaldi browser. It is still possible to open the URLs with for example chrome.

The i3-switch-window applications expect to find a configuration file in "i3_switch_window/config.ini" in your config directory.
The file can be empty.

A sample config.ini is:
```bash
[webbrowser]
webbrowser = google-chrome

[workspace]
# i3 workspace to which focused window will be swapped
swap_workspace = 9
```

## How to use
The commands can be run from the command line. They can also be part of the i3 configuration.
Here are some sample lines from my i3 configuration file:
```bash
# %%hotkey: get web browser tab titles and URLs, select one, display at current desktop window %%
bindsym $mod+u exec ~/.local/bin/browser_tab swap

# %%hotkey: get web browser tab titles and URLs, select one, display next to current desktop window %%
bindsym $mod+Shift+u exec ~/.local/bin/browser_tab add

# %%hotkey: get current buffers from emacs, select one, display at current desktop window %%
bindsym $mod+b exec ~/.local/bin/emacs_buffers swap

# %%hotkey: get current buffers from emacs, select one, display next to current desktop window %%
bindsym $mod+Shift+b exec ~/.local/bin/emacs_buffers add

# %%hotkey: get recentf list from emacs, select one, display at current desktop window %%
bindsym $mod+r exec ~/.local/bin/emacs_recentf swap

# %%hotkey: get recentf list from emacs, select one, display next to current desktop window %%
bindsym $mod+Shift+r exec ~/.local/bin/emacs_recentf add
```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/johanwiden/i3-switch-window/releases) page.

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

You can update it in [`release-drafter.yml`](https://github.com/johanwiden/i3-switch-window/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/johanwiden/i3-switch-window)](https://github.com/johanwiden/i3-switch-window/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/johanwiden/i3-switch-window/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{i3-switch-window,
  author = {Johan Widén},
  title = {In i3wm replace current window with emacs buffer, emacs recentf file, or browser tab},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/johanwiden/i3-switch-window}}
}
```
