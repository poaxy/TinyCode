#!/usr/bin/env python3
"""
Loading animation module for tinycode.
Provides animated loading indicator with moving dots.
"""

import sys
import time
import threading
from typing import Optional, Union
from abc import ABC, abstractmethod


class BaseLoadingAnimation(ABC):
    """Base class for loading animations."""
    
    def __init__(self, message: str = "Thinking", speed: float = 0.3):
        self.message = message
        self.speed = speed
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    @abstractmethod
    def _animate(self):
        """Internal animation loop."""
        pass
    
    def start(self):
        """Start the loading animation in a separate thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the loading animation and clear the line."""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        
        # Clear the line
        sys.stdout.write("\r" + " " * (len(self.message) + 4) + "\r")
        sys.stdout.flush()
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


class LoadingAnimation(BaseLoadingAnimation):
    """Animated loading indicator with moving dots."""
    
    def __init__(self, message: str = "Thinking", speed: float = 0.3):
        super().__init__(message, speed)
        self.dots = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_dot = 0
    
    def _animate(self):
        """Internal animation loop."""
        while self.running:
            # Clear line and show animation
            sys.stdout.write(f"\r{self.message} {self.dots[self.current_dot]}")
            sys.stdout.flush()
            
            # Move to next dot
            self.current_dot = (self.current_dot + 1) % len(self.dots)
            
            # Wait before next frame
            time.sleep(self.speed)
    
    def stop(self):
        """Stop the loading animation and clear the line."""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        
        # Clear the line
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()


class SimpleLoadingAnimation(BaseLoadingAnimation):
    """Simpler loading animation with just dots."""
    
    def __init__(self, message: str = "Thinking", speed: float = 0.5):
        super().__init__(message, speed)
        self.dot_count = 0
    
    def _animate(self):
        """Internal animation loop."""
        while self.running:
            dots = "." * (self.dot_count + 1)
            spaces = " " * (3 - len(dots))
            
            # Clear line and show animation
            sys.stdout.write(f"\r{self.message}{dots}{spaces}")
            sys.stdout.flush()
            
            # Cycle dots
            self.dot_count = (self.dot_count + 1) % 4
            
            # Wait before next frame
            time.sleep(self.speed)


def show_loading(message: str = "Thinking", style: str = "dots") -> BaseLoadingAnimation:
    """
    Factory function to create loading animation.
    
    Args:
        message: Message to display
        style: Animation style ('dots' or 'spinner')
        
    Returns:
        BaseLoadingAnimation instance
    """
    if style == "spinner":
        return LoadingAnimation(message)
    else:
        return SimpleLoadingAnimation(message)


if __name__ == "__main__":
    # Test the loading animation
    print("Testing loading animation...")
    
    with show_loading("Processing", "spinner"):
        time.sleep(3)
    
    print("Done!")
    
    with show_loading("Thinking", "dots"):
        time.sleep(3)
    
    print("Done!") 