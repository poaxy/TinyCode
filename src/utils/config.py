#!/usr/bin/env python3
"""
Configuration management module for tinycode.
Handles API keys, settings, and configuration file operations.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages tinycode configuration and API keys."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Custom configuration directory
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Default to ~/.config/tinycode
            self.config_dir = Path.home() / ".config" / "tinycode"
        
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "auto_select_api": True,
            "preferred_api": "openai",
            "openai": {
                "api_key": "",
                "model": "gpt-3.5-turbo",
                "max_tokens": 100,
                "enabled": False
            },
            "claude": {
                "api_key": "",
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 100,
                "enabled": False
            },
            "system": {
                "auto_detect_distro": True,
                "include_distro_in_prompt": True
            },
            "ui": {
                "loading_animation": True,
                "copy_to_clipboard": False,
                "animation_style": "dots"
            }
        }
    
    def save_config(self) -> bool:
        """Save configuration to file."""
        try:
            # Ensure config directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_api_key(self, api_name: str) -> Optional[str]:
        """
        Get API key for specified service.
        
        Args:
            api_name: Name of the API ('openai' or 'claude')
            
        Returns:
            API key if available, None otherwise
        """
        if api_name not in self.config:
            return None
        
        api_key = self.config[api_name].get("api_key", "")
        return api_key if api_key else None
    
    def set_api_key(self, api_name: str, api_key: str) -> bool:
        """
        Set API key for specified service.
        
        Args:
            api_name: Name of the API ('openai' or 'claude')
            api_key: API key to set
            
        Returns:
            True if successful, False otherwise
        """
        if api_name not in self.config:
            return False
        
        self.config[api_name]["api_key"] = api_key
        self.config[api_name]["enabled"] = bool(api_key)
        return self.save_config()
    
    def is_api_enabled(self, api_name: str) -> bool:
        """
        Check if API is enabled and has a valid key.
        
        Args:
            api_name: Name of the API ('openai' or 'claude')
            
        Returns:
            True if API is enabled and has a key
        """
        if api_name not in self.config:
            return False
        
        return (
            self.config[api_name].get("enabled", False) and
            bool(self.config[api_name].get("api_key", ""))
        )
    
    def get_available_apis(self) -> list:
        """
        Get list of available APIs with valid keys.
        
        Returns:
            List of API names that are enabled and have keys
        """
        available = []
        for api_name in ["openai", "claude"]:
            if self.is_api_enabled(api_name):
                available.append(api_name)
        return available
    
    def get_preferred_api(self) -> Optional[str]:
        """
        Get the preferred API based on configuration.
        
        Returns:
            Name of preferred API if available, None otherwise
        """
        if not self.config.get("auto_select_api", True):
            preferred = self.config.get("preferred_api", "openai")
            if self.is_api_enabled(preferred):
                return preferred
            return None
        
        # Auto-select based on availability
        available = self.get_available_apis()
        if not available:
            return None
        
        # If only one available, use it
        if len(available) == 1:
            return available[0]
        
        # If multiple available, use preferred
        preferred = self.config.get("preferred_api", "openai")
        if preferred in available:
            return preferred
        
        # Fallback to first available
        return available[0]
    
    def get_api_config(self, api_name: str) -> Dict[str, Any]:
        """
        Get full configuration for specified API.
        
        Args:
            api_name: Name of the API ('openai' or 'claude')
            
        Returns:
            API configuration dictionary
        """
        return self.config.get(api_name, {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration."""
        return self.config.get("ui", {})
    
    def get_system_config(self) -> Dict[str, Any]:
        """Get system configuration."""
        return self.config.get("system", {})
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values.
        
        Args:
            updates: Dictionary of configuration updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._update_nested_dict(self.config, updates)
            return self.save_config()
        except Exception as e:
            print(f"Error updating config: {e}")
            return False
    
    def _update_nested_dict(self, target: Dict[str, Any], updates: Dict[str, Any]):
        """Recursively update nested dictionary."""
        for key, value in updates.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_nested_dict(target[key], value)
            else:
                target[key] = value
    
    def reset_config(self) -> bool:
        """Reset configuration to defaults."""
        self.config = self._get_default_config()
        return self.save_config()
    
    def validate_config(self) -> Dict[str, list]:
        """
        Validate configuration and return any issues.
        
        Returns:
            Dictionary of validation issues by category
        """
        issues = {
            "errors": [],
            "warnings": []
        }
        
        # Check if any API is configured
        available_apis = self.get_available_apis()
        if not available_apis:
            issues["errors"].append("No API keys configured. Use --set-api-key to configure.")
        
        # Check preferred API
        preferred = self.config.get("preferred_api")
        if preferred and preferred not in ["openai", "claude"]:
            issues["warnings"].append(f"Unknown preferred API: {preferred}")
        
        # Check API key formats
        for api_name in ["openai", "claude"]:
            api_key = self.get_api_key(api_name)
            if api_key:
                if api_name == "openai" and not api_key.startswith("sk-"):
                    issues["warnings"].append(f"OpenAI API key format may be invalid")
                elif api_name == "claude" and not api_key.startswith("sk-ant-"):
                    issues["warnings"].append(f"Claude API key format may be invalid")
        
        return issues


if __name__ == "__main__":
    # Test the configuration manager
    config = ConfigManager()
    
    print("Default config:")
    print(json.dumps(config.config, indent=2))
    
    print(f"\nAvailable APIs: {config.get_available_apis()}")
    print(f"Preferred API: {config.get_preferred_api()}")
    
    issues = config.validate_config()
    if issues["errors"]:
        print(f"\nErrors: {issues['errors']}")
    if issues["warnings"]:
        print(f"Warnings: {issues['warnings']}") 