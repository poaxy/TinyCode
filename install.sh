#!/bin/bash

# tinycode installation script
# Version: 2.1.0 - Auto-distribution detection and package installation

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

# Function to detect Linux distribution
detect_distribution() {
    local distro_id="unknown"
    local package_manager="unknown"
    
    # Check /etc/os-release first
    if [[ -f /etc/os-release ]]; then
        source /etc/os-release
        distro_id="${ID:-unknown}"
    fi
    
    # Detect package manager
    if command -v apt &> /dev/null; then
        package_manager="apt"
    elif command -v dnf &> /dev/null; then
        package_manager="dnf"
    elif command -v yum &> /dev/null; then
        package_manager="yum"
    elif command -v pacman &> /dev/null; then
        package_manager="pacman"
    elif command -v zypper &> /dev/null; then
        package_manager="zypper"
    elif command -v apk &> /dev/null; then
        package_manager="apk"
    fi
    
    echo "$distro_id:$package_manager"
}

# Function to get venv package name for distribution
get_venv_package() {
    local distro_id="$1"
    local package_manager="$2"
    
    case "$distro_id" in
        "ubuntu"|"debian"|"linuxmint"|"pop"|"elementary")
            echo "python3-venv"
            ;;
        "fedora"|"rhel"|"centos"|"rocky"|"alma"|"amazon")
            echo "python3-venv"
            ;;
        "arch"|"manjaro"|"endeavouros")
            echo "python-virtualenv"
            ;;
        "opensuse"|"sles")
            echo "python3-venv"
            ;;
        "alpine")
            echo "py3-venv"
            ;;
        *)
            # For unknown distributions, try common package names
            case "$package_manager" in
                "apt")
                    echo "python3-venv"
                    ;;
                "dnf"|"yum")
                    echo "python3-venv"
                    ;;
                "pacman")
                    echo "python-virtualenv"
                    ;;
                "zypper")
                    echo "python3-venv"
                    ;;
                "apk")
                    echo "py3-venv"
                    ;;
                *)
                    echo "unknown"
                    ;;
            esac
            ;;
    esac
}

# Function to install venv package
install_venv_package() {
    local distro_id="$1"
    local package_manager="$2"
    local venv_package="$3"
    
    if [[ "$venv_package" == "unknown" ]]; then
        echo -e "${YELLOW}Could not determine venv package for your distribution${NC}"
        echo "Please install the appropriate python3-venv package manually:"
        echo "  Ubuntu/Debian: sudo apt install python3-venv"
        echo "  Fedora/CentOS: sudo dnf install python3-venv"
        echo "  Arch: sudo pacman -S python-virtualenv"
        echo "  Alpine: sudo apk add py3-venv"
        return 1
    fi
    
    echo -e "${YELLOW}Installing $venv_package...${NC}"
    
    case "$package_manager" in
        "apt")
            if ! sudo apt update &> /dev/null; then
                echo -e "${RED}Failed to update package list${NC}"
                return 1
            fi
            if sudo apt install -y "$venv_package"; then
                echo -e "${GREEN}✓ $venv_package installed successfully${NC}"
                return 0
            else
                echo -e "${RED}Failed to install $venv_package${NC}"
                return 1
            fi
            ;;
        "dnf")
            if sudo dnf install -y "$venv_package"; then
                echo -e "${GREEN}✓ $venv_package installed successfully${NC}"
                return 0
            else
                echo -e "${RED}Failed to install $venv_package${NC}"
                return 1
            fi
            ;;
        "yum")
            if sudo yum install -y "$venv_package"; then
                echo -e "${GREEN}✓ $venv_package installed successfully${NC}"
                return 0
            else
                echo -e "${RED}Failed to install $venv_package${NC}"
                return 1
            fi
            ;;
        "pacman")
            if sudo pacman -S --noconfirm "$venv_package"; then
                echo -e "${GREEN}✓ $venv_package installed successfully${NC}"
                return 0
            else
                echo -e "${RED}Failed to install $venv_package${NC}"
                return 1
            fi
            ;;
        "zypper")
            if sudo zypper install -y "$venv_package"; then
                echo -e "${GREEN}✓ $venv_package installed successfully${NC}"
                return 0
            else
                echo -e "${RED}Failed to install $venv_package${NC}"
                return 1
            fi
            ;;
        "apk")
            if sudo apk add "$venv_package"; then
                echo -e "${GREEN}✓ $venv_package installed successfully${NC}"
                return 0
            else
                echo -e "${RED}Failed to install $venv_package${NC}"
                return 1
            fi
            ;;
        *)
            echo -e "${RED}Unknown package manager: $package_manager${NC}"
            return 1
            ;;
    esac
}

echo -e "${BLUE}tinycode - AI-powered command line generator${NC}"
echo -e "${BLUE}=============================================${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Error: This script should not be run as root${NC}"
   echo "Please run without sudo"
   exit 1
fi

# Detect distribution
echo -e "${YELLOW}Detecting Linux distribution...${NC}"
distro_info=$(detect_distribution)
distro_id=$(echo "$distro_info" | cut -d: -f1)
package_manager=$(echo "$distro_info" | cut -d: -f2)

echo -e "${GREEN}✓ Detected: $distro_id (package manager: $package_manager)${NC}"

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

# Check for venv module and ensurepip
echo -e "${YELLOW}Checking for virtual environment support...${NC}"
venv_available=false

# Check if venv module is available
if python3 -c "import venv" &> /dev/null; then
    # Check if ensurepip is available (needed for venv creation)
    if python3 -c "import ensurepip" &> /dev/null; then
        venv_available=true
        echo -e "${GREEN}✓ Virtual environment support available${NC}"
    else
        echo -e "${YELLOW}⚠ venv module found but ensurepip not available${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Python venv module not available${NC}"
fi

# If venv is not fully available, try to install it
if [[ "$venv_available" == "false" ]]; then
    echo -e "${YELLOW}Attempting to install virtual environment support...${NC}"
    
    # Get the appropriate venv package for this distribution
    venv_package=$(get_venv_package "$distro_id" "$package_manager")
    
    if [[ "$venv_package" != "unknown" ]]; then
        # Check if sudo is available
        if ! command -v sudo &> /dev/null; then
            echo -e "${RED}Error: sudo is required to install $venv_package${NC}"
            echo "Please install $venv_package manually or run this script with sudo privileges"
            exit 1
        fi
        
        # Try to install the package
        if install_venv_package "$distro_id" "$package_manager" "$venv_package"; then
            echo -e "${GREEN}✓ Virtual environment support now available${NC}"
            venv_available=true
        else
            echo -e "${RED}Failed to install virtual environment support${NC}"
            echo "Please install $venv_package manually:"
            case "$package_manager" in
                "apt")
                    echo "  sudo apt install $venv_package"
                    ;;
                "dnf")
                    echo "  sudo dnf install $venv_package"
                    ;;
                "yum")
                    echo "  sudo yum install $venv_package"
                    ;;
                "pacman")
                    echo "  sudo pacman -S $venv_package"
                    ;;
                "zypper")
                    echo "  sudo zypper install $venv_package"
                    ;;
                "apk")
                    echo "  sudo apk add $venv_package"
                    ;;
            esac
            exit 1
        fi
    else
        echo -e "${RED}Could not determine the appropriate venv package for your distribution${NC}"
        echo "Please install python3-venv manually:"
        echo "  Ubuntu/Debian: sudo apt install python3-venv"
        echo "  Fedora/CentOS: sudo dnf install python3-venv"
        echo "  Arch: sudo pacman -S python-virtualenv"
        echo "  Alpine: sudo apk add py3-venv"
        exit 1
    fi
fi

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