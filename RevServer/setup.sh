#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update

# Install Terminator (or another terminal emulator of your choice)
echo "Installing Terminator..."
sudo apt install -y terminator

# Check if installation was successful
if command -v terminator &> /dev/null
then
    echo "Terminator installed successfully!"
else
    echo "Failed to install Terminator."
    exit 1
fi

# Install Python packages from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing Python packages from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Skipping Python package installation."
fi

echo "Setup completed successfully!"
