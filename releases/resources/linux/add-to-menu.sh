#!/bin/sh
# add-to-menu.sh
# Creates a .desktop for JES.

# Where are we?

JES_BASE="$(dirname $(readlink -f $0))"
JES_HOME="$JES_BASE/jes"


# Where's the user's applications directory?

APPLICATIONS=${XDG_DATA_HOME:=$HOME/.local/share}/applications


# All right, let's build one!

DESKTOP=$APPLICATIONS/jes.desktop

echo "[Desktop Entry]" > $DESKTOP
echo "Type=Application" >> $DESKTOP
echo "Version=1.0" >> $DESKTOP
echo >> $DESKTOP

echo "Name=JES" >> $DESKTOP
echo "Comment=Write Python programs to work with pictures, sounds, and videos" >> $DESKTOP
echo "Icon=$JES_HOME/images/jesicon.png" >> $DESKTOP
echo "Categories=Development;Education" >> $DESKTOP
echo "Keywords=Jython;Environment;Students" >> $DESKTOP
echo >> $DESKTOP

echo "TryExec=$JES_BASE/jes.sh" >> $DESKTOP
echo "Exec=\"$JES_BASE/jes.sh\" %f" >> $DESKTOP
echo >> $DESKTOP

echo "MimeType=application/x-python;text/x-python" >> $DESKTOP


# Also, refresh stuff if we need to.

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database $APPLICATIONS

