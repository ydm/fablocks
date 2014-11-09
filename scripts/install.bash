#!/bin/bash

ROOT="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")/.." )"

# Return 1 if package $1 is installed and updated, 0 otherwise.  This
# function works with pacman (Arch GNU/Linux's package manager) only.
function _ax_installp {
    pacman -Qu "$1" >/dev/null 2>&1
    return $?
}

# Install the package $1 on Arch GNU/Linux
function ax_install {
    if _ax_installp "$1" ; then
        sudo pacman -S --noconfirm "$1"
    fi
}

function _gem_installp {
    if which gem 1>/dev/null
    then
        gem list --local | grep "$1" >/dev/null 2>&1
        return $(test $? -eq 1)
    else
        return 1
    fi
}

function gem_install {
    if _gem_installp "$1"
    then
        gem install "$1"
    fi
}

function _main  {
    # 1. If host platform is Arch GNU/Linux, install package dependencies
    grep -e "Arch Linux" /etc/os-release >/dev/null 2>&1
    if [ $? -eq 0 ] ; then
        for pkg in postgresql python-virtualenv ruby ; do
            ax_install $pkg
        done
    fi

    # 2. Install Ruby gems
    for g in foreman ; do
        gem_install $g
    done

    # 3. Install Python virtualenv and pips
    VENV="$ROOT/venv"
    if [ ! -d "$VENV" ] ; then
        virtualenv "$VENV"
    fi
    source "$VENV/bin/activate"
    pip install --upgrade django-toolbelt
    while read line ; do
        pip install --upgrade "$line"
    done < "$ROOT/scripts/pips.txt"

    # 4. Update requirements file
    pip freeze > "$ROOT/requirements.txt"
}

_main
