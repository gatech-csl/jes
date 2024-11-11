#!/bin/sh
# add-to-menu.sh
# Creates a .desktop file for JES on Linux.

# Get the script's directory (absolute path)
JES_BASE="$(dirname "$(readlink -f "$0")")"
JES_HOME="$JES_BASE/jes"

# Define the user's applications directory (default to ~/.local/share/applications)
APPLICATIONS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

# The path to the .desktop file to be created
DESKTOP="$APPLICATIONS/jes.desktop"

# Icon file path (using .png format)
ICON="$JES_HOME/images/jesicon.png"

# Check if the icon exists
if [ ! -f "$ICON" ]; then
    echo "Warning: Icon file '$ICON' not found. Please ensure the icon exists."
    ICON=""
fi

# Creating the .desktop file
echo "[Desktop Entry]" > "$DESKTOP"
echo "Type=Application" >> "$DESKTOP"
echo "Version=6.0" >> "$DESKTOP"
echo >> "$DESKTOP"

echo "Name=JES" >> "$DESKTOP"
echo "Comment=Write Python programs to work with pictures, sounds, and videos" >> "$DESKTOP"

# Use the icon if found
if [ -n "$ICON" ]; then
    echo "Icon=$ICON" >> "$DESKTOP"
else
    echo "Warning: No icon specified in .desktop file" >> "$DESKTOP"
fi

echo "Categories=Development;Education" >> "$DESKTOP"
echo "Keywords=Jython;Environment;Students" >> "$DESKTOP"
echo >> "$DESKTOP"

# Ensure the `jes.sh` script is correctly referenced
echo "TryExec=$JES_BASE/jes.sh" >> "$DESKTOP"
echo "Exec=\"$JES_BASE/jes.sh\" %f" >> "$DESKTOP"
echo >> "$DESKTOP"

# MIME type for Python files (optional, adjust as necessary)
echo "MimeType=application/x-python;text/x-python" >> "$DESKTOP"

# Make the .desktop file executable
chmod +x "$DESKTOP"

# Refresh the application menu database if needed
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPLICATIONS"
    echo "Updated application menu."
else
    echo "Note: 'update-desktop-database' not found. You may need to refresh manually."
fi

echo "JES has been added to the menu!"
