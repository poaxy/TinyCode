#!/bin/bash

# tinycode installation script
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation directories
CONFIG_DIR="$HOME/.config/tinycode"

echo -e "${BLUE}tinycode - AI-powered command line generator${NC}"
echo -e "${BLUE}=============================================${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Error: This script should not be run as root${NC}"
   echo "Please run without sudo"
   exit 1
fi

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.7"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo -e "${RED}Error: Python 3.7 or higher is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if setup.py exists
if [[ ! -f "$SCRIPT_DIR/setup.py" ]]; then
    echo -e "${RED}Error: setup.py not found in $SCRIPT_DIR${NC}"
    exit 1
fi

# Check if requirements.txt exists
if [[ ! -f "$SCRIPT_DIR/requirements.txt" ]]; then
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

# Create config directory
echo -e "${YELLOW}Creating configuration directory...${NC}"
mkdir -p "$CONFIG_DIR"
echo -e "${GREEN}✓ Configuration directory created: $CONFIG_DIR${NC}"

# Install tinycode using pip
echo -e "${YELLOW}Installing tinycode using pip...${NC}"
cd "$SCRIPT_DIR"

# Install in user mode to avoid permission issues
python3 -m pip install --user .

# Check if installation was successful
if command -v tinycode &> /dev/null; then
    echo -e "${GREEN}✓ tinycode installed successfully${NC}"
    
    # Get the actual location of the installed command
    TINYCODE_PATH=$(which tinycode)
    echo -e "${GREEN}✓ Command available at: $TINYCODE_PATH${NC}"
    
    # Check if it's in a standard PATH location
    if [[ "$TINYCODE_PATH" == *"/usr/local/bin/"* ]] || [[ "$TINYCODE_PATH" == *"/.local/bin/"* ]]; then
        echo -e "${GREEN}✓ Command is in standard PATH location${NC}"
    else
        echo -e "${YELLOW}Note: Command installed to: $TINYCODE_PATH${NC}"
        echo "Make sure this location is in your PATH"
    fi
else
    echo -e "${RED}Error: tinycode installation failed${NC}"
    echo "Trying alternative installation method..."
    
    # Fallback: install dependencies manually and copy script
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    python3 -m pip install --user -r requirements.txt
    
    # Try to find a writable location
    if [[ -w "/usr/local/bin" ]]; then
        cp "$SCRIPT_DIR/tinycode" "/usr/local/bin/"
        chmod +x "/usr/local/bin/tinycode"
        echo -e "${GREEN}✓ tinycode installed to /usr/local/bin/tinycode${NC}"
    else
        USER_BIN="$HOME/.local/bin"
        mkdir -p "$USER_BIN"
        cp "$SCRIPT_DIR/tinycode" "$USER_BIN/"
        chmod +x "$USER_BIN/tinycode"
        echo -e "${GREEN}✓ tinycode installed to $USER_BIN/tinycode${NC}"
        
        # Check if user bin is in PATH
        if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
            echo -e "${YELLOW}Note: $USER_BIN is not in your PATH${NC}"
            echo "Add this line to your shell profile (.bashrc, .zshrc, etc.):"
            echo -e "${BLUE}export PATH=\"\$PATH:$USER_BIN\"${NC}"
        fi
    fi
fi

echo
echo -e "${GREEN}Installation completed successfully!${NC}"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. Configure your API keys:"
echo "   tinycode --set-api-key openai YOUR_OPENAI_KEY"
echo "   tinycode --set-api-key claude YOUR_CLAUDE_KEY"
echo
echo "2. Test the installation:"
echo "   tinycode --version"
echo "   tinycode --help"
echo
echo "3. Try it out:"
echo "   tinycode \"list all files in current directory\""
echo
echo -e "${BLUE}For more information, visit: https://github.com/your-repo/tinycode${NC}" 