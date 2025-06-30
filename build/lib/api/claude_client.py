#!/usr/bin/env python3
"""
Claude API client for tinycode.
Handles Anthropic Claude API calls for command generation.
"""

import os
import time
from typing import Dict, Any, Optional
import anthropic


class ClaudeClient:
    """Claude API client for command generation."""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229", max_tokens: int = 100):
        """
        Initialize Claude client.
        
        Args:
            api_key: Anthropic API key
            model: Model to use for generation
            max_tokens: Maximum tokens for response
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_command(self, query: str, system_context: str = "") -> Optional[str]:
        """
        Generate a command using Claude API.
        
        Args:
            query: User's query
            system_context: System information context
            
        Returns:
            Generated command or None if failed
        """
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt(system_context)
            
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            
            # Extract and clean response
            if response.content and len(response.content) > 0:
                command = response.content[0].text.strip()
                return self._clean_command(command)
            
            return None
            
        except anthropic.AuthenticationError:
            print("Error: Invalid Claude API key")
            return None
        except anthropic.RateLimitError:
            print("Error: Claude API rate limit exceeded")
            return None
        except anthropic.APIError as e:
            print(f"Error: Claude API error: {e}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error with Claude API: {e}")
            return None
    
    def _build_system_prompt(self, system_context: str) -> str:
        """
        Build system prompt with context.
        
        Args:
            system_context: System information context
            
        Returns:
            Formatted system prompt
        """
        base_prompt = """You are a command-line expert for Linux systems. Generate ONLY a single command line that solves the user's request. Do not include explanations, markdown formatting, or multiple commands. Return only the executable command suitable for the user's system.

Important rules:
1. Return ONLY the command, no explanations
2. No markdown formatting (no backticks, no code blocks)
3. No multiple commands separated by semicolons or newlines
4. Ensure the command is safe and appropriate for the user's system
5. Use the appropriate package manager and tools for their distribution"""

        if system_context:
            base_prompt += f"\n\nSystem Information: {system_context}"
        
        return base_prompt
    
    def _clean_command(self, command: str) -> str:
        """
        Clean and validate the generated command.
        
        Args:
            command: Raw command from API
            
        Returns:
            Cleaned command
        """
        # Remove markdown formatting
        command = command.strip()
        if command.startswith('```'):
            lines = command.split('\n')
            if len(lines) > 1:
                command = '\n'.join(lines[1:-1]) if lines[-1].startswith('```') else '\n'.join(lines[1:])
        
        # Remove backticks
        command = command.strip('`')
        
        # Remove any trailing explanations
        if '\n' in command:
            command = command.split('\n')[0]
        
        # Remove any markdown language specifiers
        if command.startswith('bash') or command.startswith('sh'):
            command = command[4:].strip()
        
        return command.strip()
    
    def test_connection(self) -> bool:
        """
        Test API connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "echo hello"}]
            )
            return True
        except Exception:
            return False


if __name__ == "__main__":
    # Test the Claude client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY environment variable")
        exit(1)
    
    client = ClaudeClient(api_key)
    
    # Test connection
    if client.test_connection():
        print("Claude API connection successful")
        
        # Test command generation
        result = client.generate_command("list all files in current directory")
        print(f"Generated command: {result}")
    else:
        print("Claude API connection failed") 