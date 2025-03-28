#!/bin/bash

INSTALL_DIR="/opt/flashcard_generator"
BIN_PATH="/usr/local/bin/flashcard"

echo "Uninstalling Flashcard Generator..."

# Remove symlink
sudo rm -f $BIN_PATH

# Remove installation directory
sudo rm -rf $INSTALL_DIR

echo "Uninstallation complete."
