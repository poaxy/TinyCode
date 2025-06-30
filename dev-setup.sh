#!/bin/bash

# tinycode development setup script
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}tinycode - Development Setup${NC}"
echo -e "${BLUE}===========================${NC}"
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

# Check if we're in the right directory
if [[ ! -f "$SCRIPT_DIR/setup.py" ]]; then
    echo -e "${RED}Error: setup.py not found. Please run this script from the tinycode directory${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install in development mode
echo -e "${YELLOW}Installing tinycode in development mode...${NC}"
pip install -e .
echo -e "${GREEN}✓ tinycode installed in development mode${NC}"

# Install development dependencies
echo -e "${YELLOW}Installing development dependencies...${NC}"
pip install pytest black flake8 mypy
echo -e "${GREEN}✓ Development dependencies installed${NC}"

# Create config directory
CONFIG_DIR="$HOME/.config/tinycode"
echo -e "${YELLOW}Creating configuration directory...${NC}"
mkdir -p "$CONFIG_DIR"
echo -e "${GREEN}✓ Configuration directory created: $CONFIG_DIR${NC}"

echo
echo -e "${GREEN}Development setup completed successfully!${NC}"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo
echo "2. Configure your API keys:"
echo "   tinycode --set-api-key openai YOUR_OPENAI_KEY"
echo "   tinycode --set-api-key claude YOUR_CLAUDE_KEY"
echo
echo "3. Test the installation:"
echo "   tinycode --version"
echo "   tinycode --help"
echo
echo "4. Run tests:"
echo "   pytest"
echo
echo "5. Format code:"
echo "   black src/"
echo
echo "6. Lint code:"
echo "   flake8 src/"
echo
echo -e "${BLUE}Happy coding!${NC}" 