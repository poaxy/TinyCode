#!/bin/bash

# tinycode installation script
# Version: 2.0.0 - Virtual Environment Support

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation directories
CONFIG_DIR="$HOME/.config/tinycode"
VENV_DIR="$HOME/.local/share/tinycode/venv"
INSTALL_DIR="$HOME/.local/bin"

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

# Check for venv module
echo -e "${YELLOW}Checking for virtual environment support...${NC}"
if ! python3 -c "import venv" &> /dev/null; then
    echo -e "${RED}Error: Python venv module not available${NC}"
    echo "Please install python3-venv:"
    echo "  Ubuntu/Debian: sudo apt install python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3-venv"
    echo "  Fedora: sudo dnf install python3-venv"
    echo "  Arch: sudo pacman -S python-virtualenv"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment support available${NC}"

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

# Create directories
echo -e "${YELLOW}Creating installation directories...${NC}"
mkdir -p "$CONFIG_DIR"
mkdir -p "$INSTALL_DIR"
mkdir -p "$(dirname "$VENV_DIR")"
echo -e "${GREEN}✓ Directories created${NC}"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [[ -d "$VENV_DIR" ]]; then
    echo -e "${YELLOW}Virtual environment already exists, removing...${NC}"
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
echo -e "${GREEN}✓ Virtual environment created at $VENV_DIR${NC}"

# Activate virtual environment and install
echo -e "${YELLOW}Installing tinycode in virtual environment...${NC}"
cd "$SCRIPT_DIR"

# Activate venv and install
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -e .

echo -e "${GREEN}✓ tinycode installed in virtual environment${NC}"
    
# Create wrapper script
echo -e "${YELLOW}Creating wrapper script...${NC}"
cat > "$INSTALL_DIR/tinycode" << 'EOF'
#!/bin/bash

# tinycode wrapper script
# This script activates the virtual environment and runs tinycode

VENV_DIR="$HOME/.local/share/tinycode/venv"
PYTHON_SCRIPT="$VENV_DIR/bin/tinycode"
    
# Check if virtual environment exists
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Error: tinycode not found in virtual environment"
    echo "Please reinstall tinycode: ./install.sh"
    exit 1
fi

# Execute tinycode from virtual environment
exec "$PYTHON_SCRIPT" "$@"
EOF

chmod +x "$INSTALL_DIR/tinycode"
echo -e "${GREEN}✓ Wrapper script created at $INSTALL_DIR/tinycode${NC}"
        
# Check if install directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Note: $INSTALL_DIR is not in your PATH${NC}"
            echo "Add this line to your shell profile (.bashrc, .zshrc, etc.):"
    echo -e "${BLUE}export PATH=\"\$PATH:$INSTALL_DIR\"${NC}"
    echo
    echo "Or run this command to add it temporarily:"
    echo -e "${BLUE}export PATH=\"\$PATH:$INSTALL_DIR\"${NC}"
    echo
        fi

# Test installation
echo -e "${YELLOW}Testing installation...${NC}"
if "$INSTALL_DIR/tinycode" --version &> /dev/null; then
    echo -e "${GREEN}✓ Installation test successful${NC}"
else
    echo -e "${RED}✗ Installation test failed${NC}"
    echo "Please check the installation and try again"
    exit 1
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
echo -e "${BLUE}Installation details:${NC}"
echo "  Virtual environment: $VENV_DIR"
echo "  Wrapper script: $INSTALL_DIR/tinycode"
echo "  Configuration: $CONFIG_DIR"
echo
echo -e "${BLUE}For more information, visit: https://github.com/poaxy/tinycode${NC}" 