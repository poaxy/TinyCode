#!/usr/bin/env python3
"""
System information detection module for tinycode.
Detects Linux distribution and provides system context.
"""

import os
import re
import subprocess
from typing import Dict, Optional, Tuple


def detect_linux_distro() -> Dict[str, str]:
    """
    Detect Linux distribution and version.
    
    Returns:
        Dict containing 'name', 'version', 'id', and 'pretty_name'
    """
    distro_info = {
        'name': 'Unknown',
        'version': 'Unknown',
        'id': 'unknown',
        'pretty_name': 'Unknown Linux Distribution'
    }
    
    # Method 1: Check /etc/os-release (standard method)
    if os.path.exists('/etc/os-release'):
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read()
                
            # Parse key-value pairs
            for line in content.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().strip('"').strip("'")
                    
                    if key == 'NAME':
                        distro_info['name'] = value
                    elif key == 'VERSION':
                        distro_info['version'] = value
                    elif key == 'ID':
                        distro_info['id'] = value.lower()
                    elif key == 'PRETTY_NAME':
                        distro_info['pretty_name'] = value
                        
        except Exception:
            pass
    
    # Method 2: Fallback to /etc/issue
    if distro_info['name'] == 'Unknown' and os.path.exists('/etc/issue'):
        try:
            with open('/etc/issue', 'r') as f:
                content = f.read().strip()
                if content:
                    distro_info['pretty_name'] = content
                    # Try to extract name and version
                    match = re.search(r'([A-Za-z]+)\s+([0-9.]+)', content)
                    if match:
                        distro_info['name'] = match.group(1)
                        distro_info['version'] = match.group(2)
        except Exception:
            pass
    
    # Method 3: Check /proc/version as last resort
    if distro_info['name'] == 'Unknown' and os.path.exists('/proc/version'):
        try:
            with open('/proc/version', 'r') as f:
                content = f.read()
                # Look for common distribution names
                for distro in ['Ubuntu', 'Debian', 'CentOS', 'Red Hat', 'Fedora', 'Arch', 'Alpine']:
                    if distro.lower() in content.lower():
                        distro_info['name'] = distro
                        break
        except Exception:
            pass
    
    return distro_info


def get_package_manager() -> str:
    """
    Detect the package manager used by the system.
    
    Returns:
        Package manager name (apt, yum, dnf, pacman, zypper, etc.)
    """
    package_managers = {
        'apt': ['/usr/bin/apt', '/usr/bin/apt-get'],
        'yum': ['/usr/bin/yum'],
        'dnf': ['/usr/bin/dnf'],
        'pacman': ['/usr/bin/pacman'],
        'zypper': ['/usr/bin/zypper'],
        'apk': ['/sbin/apk']
    }
    
    for pm, paths in package_managers.items():
        for path in paths:
            if os.path.exists(path):
                return pm
    
    return 'unknown'


def get_system_info() -> Dict[str, str]:
    """
    Get comprehensive system information.
    
    Returns:
        Dict containing all system information
    """
    distro_info = detect_linux_distro()
    package_manager = get_package_manager()
    
    system_info = {
        **distro_info,
        'package_manager': package_manager,
        'kernel': get_kernel_version(),
        'architecture': get_architecture()
    }
    
    return system_info


def get_kernel_version() -> str:
    """Get kernel version."""
    try:
        with open('/proc/version', 'r') as f:
            content = f.read()
            match = re.search(r'Linux version ([0-9.]+)', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return 'Unknown'


def get_architecture() -> str:
    """Get system architecture."""
    try:
        return os.uname().machine
    except Exception:
        return 'Unknown'


def format_system_context(system_info: Dict[str, str]) -> str:
    """
    Format system information for AI prompt context.
    
    Args:
        system_info: System information dictionary
        
    Returns:
        Formatted string for AI prompt
    """
    context_parts = []
    
    if system_info['pretty_name'] != 'Unknown Linux Distribution':
        context_parts.append(f"Distribution: {system_info['pretty_name']}")
    
    if system_info['package_manager'] != 'unknown':
        context_parts.append(f"Package Manager: {system_info['package_manager']}")
    
    if system_info['kernel'] != 'Unknown':
        context_parts.append(f"Kernel: {system_info['kernel']}")
    
    if system_info['architecture'] != 'Unknown':
        context_parts.append(f"Architecture: {system_info['architecture']}")
    
    return ' | '.join(context_parts) if context_parts else "Generic Linux System"


if __name__ == "__main__":
    # Test the module
    info = get_system_info()
    print("System Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\nFormatted Context:")
    print(format_system_context(info)) 