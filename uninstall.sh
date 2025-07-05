#!/bin/bash

# tinycode uninstall script
# Version: 2.0.0 - Virtual Environment Support

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}tinycode - Uninstaller${NC}"
echo -e "${BLUE}=====================${NC}"
echo

# Installation directories
VENV_DIR="$HOME/.local/share/tinycode/venv"
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/tinycode"

# Check if tinycode is installed
if ! command -v tinycode &> /dev/null; then
    echo -e "${YELLOW}tinycode is not installed or not found in PATH${NC}"
    exit 0
fi

echo -e "${YELLOW}Found tinycode installation${NC}"

# Remove wrapper script
if [[ -f "$INSTALL_DIR/tinycode" ]]; then
    echo -e "${YELLOW}Removing wrapper script...${NC}"
    rm -f "$INSTALL_DIR/tinycode"
    echo -e "${GREEN}✓ Wrapper script removed${NC}"
fi

# Remove virtual environment
if [[ -d "$VENV_DIR" ]]; then
    echo -e "${YELLOW}Removing virtual environment...${NC}"
    rm -rf "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment removed${NC}"
fi

# Remove parent directory if empty
if [[ -d "$(dirname "$VENV_DIR")" ]] && [[ -z "$(ls -A "$(dirname "$VENV_DIR")")" ]]; then
    rmdir "$(dirname "$VENV_DIR")"
    echo -e "${GREEN}✓ Empty parent directory removed${NC}"
fi

# Ask about configuration removal
echo -e "${YELLOW}Do you want to remove configuration files? (y/N)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    if [[ -d "$CONFIG_DIR" ]]; then
        echo -e "${YELLOW}Removing configuration directory...${NC}"
        rm -rf "$CONFIG_DIR"
        echo -e "${GREEN}✓ Configuration directory removed${NC}"
    fi
else
    echo -e "${BLUE}Configuration files preserved at: $CONFIG_DIR${NC}"
fi

echo
echo -e "${GREEN}Uninstallation completed successfully!${NC}"
echo -e "${BLUE}Thank you for using tinycode!${NC}" 