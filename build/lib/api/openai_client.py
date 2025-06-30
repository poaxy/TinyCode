#!/usr/bin/env python3
"""
OpenAI API client for tinycode.
Handles ChatGPT API calls for command generation.
"""

import os
import time
from typing import Dict, Any, Optional
import openai
from openai import OpenAI


class OpenAIClient:
    """OpenAI API client for command generation."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", max_tokens: int = 100):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for generation
            max_tokens: Maximum tokens for response
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key)
    
    def generate_command(self, query: str, system_context: str = "") -> Optional[str]:
        """
        Generate a command using OpenAI API.
        
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=self.max_tokens,
                temperature=0.1,  # Low temperature for consistent command generation
                timeout=30
            )
            
            # Extract and clean response
            if response.choices and response.choices[0].message:
                command = response.choices[0].message.content.strip()
                return self._clean_command(command)
            
            return None
            
        except openai.AuthenticationError:
            print("Error: Invalid OpenAI API key")
            return None
        except openai.RateLimitError:
            print("Error: OpenAI API rate limit exceeded")
            return None
        except openai.APIError as e:
            print(f"Error: OpenAI API error: {e}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error with OpenAI API: {e}")
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "echo hello"}],
                max_tokens=10,
                timeout=10
            )
            return True
        except Exception:
            return False


if __name__ == "__main__":
    # Test the OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)
    
    client = OpenAIClient(api_key)
    
    # Test connection
    if client.test_connection():
        print("OpenAI API connection successful")
        
        # Test command generation
        result = client.generate_command("list all files in current directory")
        print(f"Generated command: {result}")
    else:
        print("OpenAI API connection failed") 