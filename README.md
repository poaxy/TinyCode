## Features

- 🤖 **AI-Powered**: Uses OpenAI (ChatGPT) and Anthropic (Claude) APIs
- 🎯 **Single Command Output**: Returns only the command you need, no explanations
- 🐧 **Linux Distribution Aware**: Automatically detects your Linux distribution for better command generation
- 🔄 **Automatic API Selection**: Uses available API or falls back between them
- ⚡ **Animated Loading**: Shows loading animation while generating commands
- 🎨 **Modern CLI**: Clean, intuitive command-line interface
- 📋 **Copy to Clipboard**: Optional clipboard integration
- ⚙️ **Configurable**: Easy API key management and settings

## Installation

### Quick Install (Recommended)

```bash
# Clone or download the repository
git clone https://github.com/poaxy/TinyCode.git
cd TinyCode

#Make the file executable
chmod +x install.sh

# Run the installation script
./install.sh
```

The installation script will:
- Check Python version requirements
- Install all dependencies automatically
- Install tinycode to your system PATH
- Create configuration directory
- Provide next steps for API configuration

### Manual Install

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/poaxy/TinyCode.git
cd TinyCode

# Install using pip (recommended)
pip3 install --user .

# Or install dependencies manually
pip3 install --user requests click colorama openai anthropic python-dotenv
```

### System-wide Installation (Optional)

For system-wide installation (requires sudo):

```bash
# Install to system Python
sudo pip3 install .

# Or install to system packages
sudo python3 setup.py install
```

### Development Setup

For contributors and developers:

```bash
# Clone the repository
git clone https://github.com/poaxy/TinyCode.git
cd TinyCode

# Run development setup
./dev-setup.sh
```

This will:
- Create a virtual environment
- Install tinycode in development mode
- Install development dependencies (pytest, black, flake8, mypy)
- Set up the configuration directory

## Configuration

### Set API Keys

You need at least one API key to use tinycode:

```bash
# Set OpenAI API key
tinycode --set-api-key openai sk-your-openai-key-here

# Set Claude API key
tinycode --set-api-key claude sk-ant-your-claude-key-here
```

### Get API Keys

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Claude**: Get your API key from [Anthropic Console](https://console.anthropic.com/)

### Verify Installation

After installation, verify everything is working:

```bash
# Run the test script
./test_installation.sh

# Or check manually
tinycode --version
tinycode --check-apis
tinycode --config
```

## Usage

### Basic Usage

```bash
# Simple command generation
tinycode "what command I need to be able to ssh to ip 192.168.2.45 on port 2222?"

# Remove all files in a directory
tinycode "give me a code to remove all files in a directory"

# Find files modified in last 24 hours
tinycode "find all files modified in last 24 hours"
```

### API Selection

```bash
# Force use of OpenAI
tinycode --openai "compress a directory to tar.gz"

# Force use of Claude
tinycode --claude "install nginx web server"
```

### Configuration and Status

```bash
# Check available APIs
tinycode --check-apis

# Show current configuration
tinycode --config

# Reset configuration to defaults
tinycode --reset-config

# Show version
tinycode --version

# Show help
tinycode --help
```

## Examples

### System Administration

```bash
# Install packages
tinycode "install nginx web server"
# Output: sudo apt install nginx

# Check disk usage
tinycode "check disk usage of current directory"
# Output: du -sh .

# Find large files
tinycode "find files larger than 100MB"
# Output: find . -type f -size +100M
```

### Network and SSH

```bash
# SSH with custom port
tinycode "ssh to 192.168.1.100 on port 2222"
# Output: ssh -p 2222 user@192.168.1.100

# Check if port is open
tinycode "check if port 80 is open on localhost"
# Output: netstat -tuln | grep :80
```

### File Operations

```bash
# Remove all files in directory
tinycode "remove all files in current directory"
# Output: rm -rf *

# Find and replace text
tinycode "find all .txt files and replace 'old' with 'new'"
# Output: find . -name "*.txt" -exec sed -i 's/old/new/g' {} \;

# Compress directory
tinycode "compress directory to tar.gz"
# Output: tar -czf archive.tar.gz directory/
```

## How It Works

1. **System Detection**: Automatically detects your Linux distribution and package manager
2. **API Selection**: Chooses the best available API (OpenAI by default, Claude as fallback)
3. **Context-Aware Prompts**: Includes system information in the AI prompt for better results
4. **Command Generation**: AI generates a single, executable command
5. **Output**: Returns only the command, ready to use

## Configuration File

The configuration is stored in `~/.config/tinycode/config.json`:

```json
{
  "auto_select_api": true,
  "preferred_api": "openai",
  "openai": {
    "api_key": "sk-...",
    "model": "gpt-3.5-turbo",
    "max_tokens": 100,
    "enabled": true
  },
  "claude": {
    "api_key": "sk-ant-...",
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 100,
    "enabled": true
  },
  "system": {
    "auto_detect_distro": true,
    "include_distro_in_prompt": true
  },
  "ui": {
    "loading_animation": true,
    "copy_to_clipboard": false,
    "animation_style": "dots"
  }
}
```

## Scripts

The repository includes several helpful scripts:

- **`install.sh`**: Main installation script (recommended)
- **`uninstall.sh`**: Remove tinycode from your system
- **`dev-setup.sh`**: Set up development environment
- **`test_installation.sh`**: Test if installation is working correctly

## Troubleshooting

### Installation Issues

```bash
# Check if tinycode is installed
which tinycode

# Check if it's in PATH
echo $PATH | grep -o '[^:]*' | grep -E "(local|usr)" | head -5

# Reinstall if needed
pip3 uninstall tinycode -y
pip3 install --user .

# Run the test script
./test_installation.sh
```

### No API Keys Configured

```bash
# Check if APIs are configured
tinycode --check-apis

# If none are configured, set them up
tinycode --set-api-key openai YOUR_KEY
```

### API Connection Issues

```bash
# Test API connections
tinycode --check-apis

# Check your internet connection
ping api.openai.com
```

### Permission Issues

```bash
# Make sure the script is executable
chmod +x /usr/local/bin/tinycode

# Check if it's in your PATH
which tinycode
```

### Python Path Issues

If you get import errors:

```bash
# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Reinstall with --force-reinstall
pip3 install --user --force-reinstall .
```

### Uninstalling

To remove tinycode completely:

```bash
# Run the uninstall script
./uninstall.sh

# Or manually
pip3 uninstall tinycode -y
rm -rf ~/.config/tinycode
```

## Requirements

- Python 3.7 or higher
- Internet connection for API access
- At least one API key (OpenAI or Claude)

## Dependencies

- `requests` - HTTP library
- `click` - CLI framework
- `colorama` - Cross-platform colored terminal text
- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `python-dotenv` - Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Workflow

```bash
# Set up development environment
./dev-setup.sh

# Activate virtual environment
source venv/bin/activate

# Make your changes...

# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Run the test script: `./test_installation.sh`
3. Open an issue on GitHub
4. Check the configuration with `tinycode --config`
