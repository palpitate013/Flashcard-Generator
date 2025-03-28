#!/bin/bash

INSTALL_DIR="/opt/flashcard_generator"
BIN_PATH="/usr/local/bin/flashcard"
REPO_URL="https://raw.githubusercontent.com/palpitate013/Flashcard-Generator/refs/heads/main/main.py"

echo "Installing Flashcard Generator..."

# Create installation directory
sudo mkdir -p $INSTALL_DIR

# Download the main script
sudo curl -o $INSTALL_DIR/flashcard.py "$REPO_URL/flashcard.py"

# Make the script executable
sudo chmod +x $INSTALL_DIR/flashcard.py

# Create a symlink in /usr/local/bin for easy execution
sudo ln -sf $INSTALL_DIR/flashcard.py $BIN_PATH

echo "Installation complete. You can run the flashcard generator using: flashcard"
