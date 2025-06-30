#!/usr/bin/env python3
"""
Main application logic for tinycode.
Handles CLI interface and coordinates all components.
"""

import sys
import os
import argparse
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.config import ConfigManager
from utils.system_info import get_system_info, format_system_context
from api.api_manager import APIManager
from ui.loading import show_loading


class TinyCode:
    """Main application class for tinycode."""
    
    def __init__(self):
        """Initialize the application."""
        self.config_manager = ConfigManager()
        self.api_manager = APIManager(self.config_manager)
    
    def run(self, args):
        """
        Run the application with given arguments.
        
        Args:
            args: Parsed command line arguments
        """
        try:
            if args.version:
                self._show_version()
                return
            
            if args.help or len(sys.argv) == 1:
                self._show_help()
                return
            
            if args.set_api_key:
                self._set_api_key(args.set_api_key[0], args.set_api_key[1])
                return
            
            if args.check_apis:
                self._check_apis()
                return
            
            if args.config:
                self._show_config()
                return
            
            if args.reset_config:
                self._reset_config()
                return
            
            # Main command generation
            if args.query:
                self._generate_command(args.query, args)
            else:
                print("Error: No query provided. Use --help for usage information.")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def _generate_command(self, query: str, args):
        """
        Generate a command based on the query.
        
        Args:
            query: User's query
            args: Command line arguments
        """
        # Get system context
        system_context = ""
        if self.config_manager.get_system_config().get("include_distro_in_prompt", True):
            system_info = get_system_info()
            system_context = format_system_context(system_info)
        
        # Determine which API to use
        preferred_api = None
        if args.openai:
            preferred_api = "openai"
        elif args.claude:
            preferred_api = "claude"
        
        # Check if any API is available
        available_apis = self.api_manager.get_available_apis()
        if not available_apis:
            print("Error: No API keys configured.")
            print("Use 'tinycode --set-api-key openai YOUR_KEY' to configure OpenAI")
            print("Use 'tinycode --set-api-key claude YOUR_KEY' to configure Claude")
            sys.exit(1)
        
        # Show loading animation
        ui_config = self.config_manager.get_ui_config()
        loading_message = "Thinking"
        loading_style = ui_config.get("animation_style", "dots")
        
        with show_loading(loading_message, loading_style):
            # Generate command
            command = self.api_manager.generate_command(
                query=query,
                system_context=system_context,
                preferred_api=preferred_api
            )
        
        # Display result
        if command:
            print(command)
            
            # Copy to clipboard if enabled
            if ui_config.get("copy_to_clipboard", False):
                self._copy_to_clipboard(command)
        else:
            print("Error: Could not generate command. Please try again.")
            sys.exit(1)
    
    def _set_api_key(self, api_name: str, api_key: str):
        """
        Set API key for specified service.
        
        Args:
            api_name: Name of the API ('openai' or 'claude')
            api_key: API key to set
        """
        if api_name not in ["openai", "claude"]:
            print(f"Error: Invalid API name '{api_name}'. Use 'openai' or 'claude'.")
            sys.exit(1)
        
        if self.config_manager.set_api_key(api_name, api_key):
            print(f"Successfully set {api_name} API key.")
            
            # Reinitialize API manager with new key
            self.api_manager = APIManager(self.config_manager)
        else:
            print(f"Error: Failed to set {api_name} API key.")
            sys.exit(1)
    
    def _check_apis(self):
        """Check available APIs and their status."""
        available_apis = self.api_manager.get_available_apis()
        api_info = self.api_manager.get_api_info()
        
        print("API Status:")
        print("=" * 50)
        
        for api_name in ["openai", "claude"]:
            info = api_info.get(api_name, {})
            enabled = info.get("enabled", False)
            
            if enabled:
                model = info.get("model", "Unknown")
                max_tokens = info.get("max_tokens", "Unknown")
                print(f"✓ {api_name.upper()}: {model} (max {max_tokens} tokens)")
            else:
                print(f"✗ {api_name.upper()}: Not configured")
        
        print(f"\nAvailable APIs: {', '.join(available_apis) if available_apis else 'None'}")
        
        if available_apis:
            selected = self.api_manager.select_api()
            print(f"Auto-selected API: {selected}")
    
    def _show_config(self):
        """Show current configuration."""
        config = self.config_manager.config
        
        print("Current Configuration:")
        print("=" * 50)
        
        # API settings
        print("API Settings:")
        for api_name in ["openai", "claude"]:
            api_config = config.get(api_name, {})
            enabled = api_config.get("enabled", False)
            model = api_config.get("model", "Unknown")
            print(f"  {api_name}: {'✓' if enabled else '✗'} ({model})")
        
        # General settings
        print(f"\nGeneral Settings:")
        print(f"  Auto-select API: {config.get('auto_select_api', True)}")
        print(f"  Preferred API: {config.get('preferred_api', 'openai')}")
        
        # System settings
        system_config = config.get("system", {})
        print(f"\nSystem Settings:")
        print(f"  Auto-detect distro: {system_config.get('auto_detect_distro', True)}")
        print(f"  Include distro in prompt: {system_config.get('include_distro_in_prompt', True)}")
        
        # UI settings
        ui_config = config.get("ui", {})
        print(f"\nUI Settings:")
        print(f"  Loading animation: {ui_config.get('loading_animation', True)}")
        print(f"  Animation style: {ui_config.get('animation_style', 'dots')}")
        print(f"  Copy to clipboard: {ui_config.get('copy_to_clipboard', False)}")
    
    def _reset_config(self):
        """Reset configuration to defaults."""
        if self.config_manager.reset_config():
            print("Configuration reset to defaults.")
            # Reinitialize API manager
            self.api_manager = APIManager(self.config_manager)
        else:
            print("Error: Failed to reset configuration.")
            sys.exit(1)
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        try:
            import subprocess
            
            # Try different clipboard commands
            commands = [
                ["xclip", "-selection", "clipboard"],
                ["xsel", "--clipboard", "--input"],
                ["pbcopy"],  # macOS
                ["clip"]     # Windows
            ]
            
            for cmd in commands:
                try:
                    subprocess.run(cmd, input=text.encode(), check=True, capture_output=True)
                    print("(Copied to clipboard)")
                    return
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            print("(Could not copy to clipboard)")
        except ImportError:
            print("(Could not copy to clipboard)")
    
    def _show_version(self):
        """Show version information."""
        print("tinycode v1.0.0")
        print("AI-powered command line generator")
        print("Supports OpenAI (ChatGPT) and Anthropic (Claude) APIs")
    
    def _show_help(self):
        """Show help information."""
        help_text = """
tinycode - AI-powered command line generator

USAGE:
    tinycode "your query here"
    tinycode [OPTIONS] "your query here"

EXAMPLES:
    tinycode "what command I need to be able to ssh to ip 192.168.2.45 on port 2222?"
    tinycode "give me a code to remove all files in a directory"
    tinycode --openai "find all files modified in last 24 hours"
    tinycode --claude "compress a directory to tar.gz"

OPTIONS:
    -h, --help              Show this help message
    -v, --version           Show version information
    --openai                Force use of OpenAI (ChatGPT) API
    --claude                Force use of Claude API
    --set-api-key API KEY   Set API key for specified service (openai/claude)
    --check-apis            Check available APIs and their status
    --config                Show current configuration
    --reset-config          Reset configuration to defaults

API CONFIGURATION:
    tinycode --set-api-key openai sk-your-openai-key
    tinycode --set-api-key claude sk-ant-your-claude-key

FEATURES:
    • Automatic API selection (uses available API or preferred)
    • Linux distribution detection for better command generation
    • Animated loading indicator
    • Fallback between APIs if one fails
    • Single-line command output
    • Copy to clipboard support

For more information, visit: https://github.com/your-repo/tinycode
"""
        print(help_text)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI-powered command line generator",
        add_help=False  # We'll handle help manually
    )
    
    # Main query argument
    parser.add_argument("query", nargs="?", help="Your query for command generation")
    
    # Options
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("-v", "--version", action="store_true", help="Show version information")
    parser.add_argument("--openai", action="store_true", help="Force use of OpenAI API")
    parser.add_argument("--claude", action="store_true", help="Force use of Claude API")
    parser.add_argument("--set-api-key", nargs=2, metavar=("API", "KEY"), help="Set API key")
    parser.add_argument("--check-apis", action="store_true", help="Check available APIs")
    parser.add_argument("--config", action="store_true", help="Show configuration")
    parser.add_argument("--reset-config", action="store_true", help="Reset configuration")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create and run application
    app = TinyCode()
    app.run(args)


if __name__ == "__main__":
    main() 