#!/usr/bin/env python3
"""
API manager for tinycode.
Handles automatic API selection and fallback logic.
"""

from typing import Optional, Dict, Any
from .openai_client import OpenAIClient
from .claude_client import ClaudeClient


class APIManager:
    """Manages API clients and handles automatic selection."""
    
    def __init__(self, config_manager):
        """
        Initialize API manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.openai_client = None
        self.claude_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients based on available keys."""
        # Initialize OpenAI client
        openai_key = self.config_manager.get_api_key("openai")
        if openai_key:
            openai_config = self.config_manager.get_api_config("openai")
            self.openai_client = OpenAIClient(
                api_key=openai_key,
                model=openai_config.get("model", "gpt-3.5-turbo"),
                max_tokens=openai_config.get("max_tokens", 100)
            )
        
        # Initialize Claude client
        claude_key = self.config_manager.get_api_key("claude")
        if claude_key:
            claude_config = self.config_manager.get_api_config("claude")
            self.claude_client = ClaudeClient(
                api_key=claude_key,
                model=claude_config.get("model", "claude-3-sonnet-20240229"),
                max_tokens=claude_config.get("max_tokens", 100)
            )
    
    def get_available_apis(self) -> list:
        """
        Get list of available API clients.
        
        Returns:
            List of available API names
        """
        available = []
        if self.openai_client:
            available.append("openai")
        if self.claude_client:
            available.append("claude")
        return available
    
    def select_api(self, preferred_api: Optional[str] = None) -> Optional[str]:
        """
        Select the best available API.
        
        Args:
            preferred_api: Manually specified API to use
            
        Returns:
            Selected API name or None if none available
        """
        available = self.get_available_apis()
        
        if not available:
            return None
        
        # If preferred API is specified and available, use it
        if preferred_api and preferred_api in available:
            return preferred_api
        
        # Auto-select based on configuration
        if not self.config_manager.config.get("auto_select_api", True):
            config_preferred = self.config_manager.config.get("preferred_api", "openai")
            if config_preferred in available:
                return config_preferred
        
        # If only one available, use it
        if len(available) == 1:
            return available[0]
        
        # If multiple available, use preferred from config
        config_preferred = self.config_manager.config.get("preferred_api", "openai")
        if config_preferred in available:
            return config_preferred
        
        # Fallback to first available
        return available[0]
    
    def generate_command(self, query: str, system_context: str = "", preferred_api: Optional[str] = None) -> Optional[str]:
        """
        Generate command using the best available API.
        
        Args:
            query: User's query
            system_context: System information context
            preferred_api: Manually specified API to use
            
        Returns:
            Generated command or None if all APIs failed
        """
        # Select API to use
        selected_api = self.select_api(preferred_api)
        if not selected_api:
            print("Error: No API keys configured. Use --set-api-key to configure.")
            return None
        
        # Try the selected API first
        result = self._try_api(selected_api, query, system_context)
        if result:
            return result
        
        # If preferred API failed and auto-select is enabled, try other APIs
        if self.config_manager.config.get("auto_select_api", True) and preferred_api:
            available_apis = self.get_available_apis()
            for api in available_apis:
                if api != selected_api:
                    result = self._try_api(api, query, system_context)
                    if result:
                        print(f"Note: {selected_api} failed, used {api} instead")
                        return result
        
        return None
    
    def _try_api(self, api_name: str, query: str, system_context: str) -> Optional[str]:
        """
        Try to generate command using specified API.
        
        Args:
            api_name: Name of the API to use
            query: User's query
            system_context: System information context
            
        Returns:
            Generated command or None if failed
        """
        client = None
        
        if api_name == "openai" and self.openai_client:
            client = self.openai_client
        elif api_name == "claude" and self.claude_client:
            client = self.claude_client
        
        if not client:
            return None
        
        try:
            return client.generate_command(query, system_context)
        except Exception as e:
            print(f"Error with {api_name} API: {e}")
            return None
    
    def test_apis(self) -> Dict[str, bool]:
        """
        Test all available APIs.
        
        Returns:
            Dictionary mapping API names to test results
        """
        results = {}
        
        if self.openai_client:
            results["openai"] = self.openai_client.test_connection()
        
        if self.claude_client:
            results["claude"] = self.claude_client.test_connection()
        
        return results
    
    def get_api_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about available APIs.
        
        Returns:
            Dictionary with API information
        """
        info = {}
        
        if self.openai_client:
            openai_config = self.config_manager.get_api_config("openai")
            info["openai"] = {
                "enabled": True,
                "model": openai_config.get("model", "gpt-3.5-turbo"),
                "max_tokens": openai_config.get("max_tokens", 100)
            }
        else:
            info["openai"] = {"enabled": False}
        
        if self.claude_client:
            claude_config = self.config_manager.get_api_config("claude")
            info["claude"] = {
                "enabled": True,
                "model": claude_config.get("model", "claude-3-sonnet-20240229"),
                "max_tokens": claude_config.get("max_tokens", 100)
            }
        else:
            info["claude"] = {"enabled": False}
        
        return info


if __name__ == "__main__":
    # Test the API manager
    from ..utils.config import ConfigManager
    
    config = ConfigManager()
    manager = APIManager(config)
    
    print("Available APIs:", manager.get_available_apis())
    print("Selected API:", manager.select_api())
    
    # Test API connections
    test_results = manager.test_apis()
    print("API Test Results:", test_results)
    
    # Get API info
    api_info = manager.get_api_info()
    print("API Info:", api_info) 