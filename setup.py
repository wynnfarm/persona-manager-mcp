#!/usr/bin/env python3
"""
Setup script for the MCP Persona Server.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="mcp-persona-server",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Model Context Protocol server for managing AI personas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-experiments",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-persona-server=mcp_persona_server.server:main",
            "persona-cli=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mcp_persona_server": ["*.json"],
    },
    keywords="mcp, model-context-protocol, ai, personas, artificial-intelligence",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mcp-experiments/issues",
        "Source": "https://github.com/yourusername/mcp-experiments",
        "Documentation": "https://github.com/yourusername/mcp-experiments#readme",
    },
)
