#!/bin/bash
#
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This file is obtained from https://src.fedoraproject.org/rpms/chromium/
# and modified by Akarshan Biswas <akarshanbiswas@fedoraproject.org>. All modifications are also
# licensed under 3-clause BSD license.

# Let the wrapped binary know that it has been run through the wrapper.
export CHROME_WRAPPER="$(readlink -f "$0")"

HERE="`dirname "$CHROME_WRAPPER"`"
# We include some xdg utilities next to the binary, and we want to prefer them
# over the system versions when we know the system versions are very old. We
# detect whether the system xdg utilities are sufficiently new to be likely to
# work for us by looking for xdg-settings. If we find it, we leave $PATH alone,
# so that the system xdg utilities (including any distro patches) will be used.
if ! which xdg-settings &> /dev/null; then
  # Old xdg utilities. Prepend $HERE to $PATH to use ours instead.
  export PATH="$HERE:$PATH"
else
  # Use system xdg utilities. But first create mimeapps.list if it doesn't
  # exist; some systems have bugs in xdg-mime that make it fail without it.
  xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
  mkdir -p "$xdg_app_dir"
  [ -f "$xdg_app_dir/mimeapps.list" ] || touch "$xdg_app_dir/mimeapps.list"
fi

# Always use our versions of ffmpeg libs.
# This also makes RPMs find the compatibly-named library symlinks.
if [[ -n "$LD_LIBRARY_PATH" ]]; then
  LD_LIBRARY_PATH="$HERE:$HERE/lib:$LD_LIBRARY_PATH"
else
  LD_LIBRARY_PATH="$HERE:$HERE/lib"
fi
export LD_LIBRARY_PATH

# We don't want bug-buddy intercepting our crashes. http://crbug.com/24120
export GNOME_DISABLE_CRASH_DIALOG=SET_BY_GOOGLE_CHROME

# Disable allow_rgb_configs to fix odd color and vaapi issues with Mesa
export allow_rgb10_configs=false

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

CHROMIUM_DISTRO_FLAGS="  --enable-plugins \
                         --enable-extensions \
                         --enable-user-scripts \
                         --enable-printing \
                         --enable-gpu-rasterization \
                         --disable-features=AudioServiceSandbox \
                         --enable-sync"

# This provides a much better experience on Wayland.
if [ "$XDG_SESSION_TYPE" == "wayland" ] || [[ $WAYLAND_DISPLAY ]] ; then
  CHROMIUM_DISTRO_FLAGS="--ozone-platform=wayland $CHROMIUM_DISTRO_FLAGS"
fi

ARGS=""
# Load user flags
if [ -n "$XDG_CONFIG_HOME" ]; then
    USER_FLAGS_LOCATION="$XDG_CONFIG_HOME/ungoogled-chromium-flags.conf"
elif [ -n "$HOME" ]; then
    USER_FLAGS_LOCATION="$HOME/.config/ungoogled-chromium-flags.conf"
fi
if [ -f $USER_FLAGS_LOCATION ]; then
    while read -r line; do
    case "$line" in
        --*)
            ARGS+=" $line"
        ;;
    esac
    done < "$USER_FLAGS_LOCATION"
fi


exec -a "$0" "@@CHROMIUMDIR@@/$(basename "$0" | sed 's/\.sh$//')" $CHROMIUM_DISTRO_FLAGS $ARGS "$@"
