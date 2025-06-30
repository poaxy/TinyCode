#!/bin/bash

# tinycode uninstall script
# Version: 1.0.0

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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Error: This script should not be run as root${NC}"
   echo "Please run without sudo"
   exit 1
fi

# Check if tinycode is installed
if ! command -v tinycode &> /dev/null; then
    echo -e "${YELLOW}tinycode is not installed or not found in PATH${NC}"
    exit 0
fi

echo -e "${YELLOW}Found tinycode installation at: $(which tinycode)${NC}"

# Uninstall using pip
echo -e "${YELLOW}Uninstalling tinycode...${NC}"
if python3 -m pip uninstall tinycode -y; then
    echo -e "${GREEN}✓ tinycode uninstalled successfully${NC}"
else
    echo -e "${RED}Error: Failed to uninstall tinycode using pip${NC}"
    echo "Trying manual removal..."
    
    # Manual removal
    TINYCODE_PATH=$(which tinycode)
    if [[ -f "$TINYCODE_PATH" ]]; then
        rm -f "$TINYCODE_PATH"
        echo -e "${GREEN}✓ Removed tinycode binary${NC}"
    fi
fi

# Remove configuration directory
CONFIG_DIR="$HOME/.config/tinycode"
if [[ -d "$CONFIG_DIR" ]]; then
    echo -e "${YELLOW}Removing configuration directory...${NC}"
    rm -rf "$CONFIG_DIR"
    echo -e "${GREEN}✓ Configuration directory removed${NC}"
else
    echo -e "${YELLOW}No configuration directory found${NC}"
fi

echo
echo -e "${GREEN}Uninstallation completed successfully!${NC}"
echo
echo -e "${BLUE}Note:${NC}"
echo "• Dependencies (openai, anthropic, etc.) were not removed"
echo "• If you want to remove dependencies, run:"
echo "  pip3 uninstall openai anthropic requests click colorama python-dotenv" 