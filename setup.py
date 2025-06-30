#!/usr/bin/env python3
"""
Setup script for tinycode.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tinycode",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered command line generator using ChatGPT and Claude APIs",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/tinycode",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "tinycode=core.tinycode:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="cli, ai, command-line, linux, openai, claude, automation",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/tinycode/issues",
        "Source": "https://github.com/your-repo/tinycode",
        "Documentation": "https://github.com/your-repo/tinycode#readme",
    },
) 