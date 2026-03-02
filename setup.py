#!/usr/bin/env python3
"""
SilverHand v3.0.0 - Advanced Cybersecurity Toolkit
Setup script for installation and distribution
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')
else:
    long_description = """
SilverHand v3.0.0 - Advanced Cybersecurity Toolkit

A comprehensive penetration testing and security assessment framework
featuring AI-powered vulnerability detection, advanced scanning modules,
and intelligent security analysis capabilities.

Features:
• Multi-module security scanning (XSS, SQL, LFI, RFI, etc.)
• AI-powered vulnerability analysis and recommendations
• Advanced XSS detection with zero-day pattern recognition
• Network and web application security assessment
• Comprehensive reporting with multiple output formats
• Interactive AI security assistant
• Parallel scanning with configurable threading
• Extensible plugin architecture
"""

# Read requirements
requirements = []
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#') and not line.startswith('-')
        ]

# Core requirements (minimal set)
core_requirements = [
    'requests>=2.28.0',
    'beautifulsoup4>=4.11.0',
    'lxml>=4.9.0',
    'click>=8.0.0',
    'colorama>=0.4.4',
    'python-dateutil>=2.8.0',
    'pyyaml>=6.0'
]

# Optional requirements for advanced features
optional_requirements = [
    'transformers>=4.20.0',
    'torch>=1.11.0',
    'scapy>=2.4.5',
    'python-nmap>=0.7.1',
    'selenium>=4.2.0',
    'cryptography>=3.4.8'
]

setup(
    name="silverhand",
    version="3.0.0",
    author="SilverHand Security Team",
    author_email="security@silverhand.dev",
    description="Advanced Cybersecurity Toolkit with AI-Powered Vulnerability Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silverhand/silverhand",

    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Natural Language :: English",
        "Framework :: AsyncIO",
        "Framework :: Flask",
        "Framework :: FastAPI"
    ],
    python_requires=">=3.8",
    install_requires=core_requirements,
    extras_require={
        "full": requirements,
        "ai": ['transformers>=4.20.0', 'torch>=1.11.0', 'numpy>=1.21.0'],
        "network": ['scapy>=2.4.5', 'python-nmap>=0.7.1'],
        "web": ['selenium>=4.2.0', 'beautifulsoup4>=4.11.0', 'lxml>=4.9.0'],
        "crypto": ['cryptography>=3.4.8', 'pycryptodome>=3.15.0'],
        "dev": ['pytest>=7.1.0', 'black>=22.0.0', 'flake8>=4.0.0', 'mypy>=0.950']
    },
    entry_points={
        "console_scripts": [
            "silverhand=silverhand.cli:main",
            "silverhand-ai=silverhand.ai.chat:main",
        ],
    },
    include_package_data=True,
    package_data={
        "silverhand": [
            "data/*.json",
            "data/*.txt",
            "templates/*.html",
            "static/*.css",
            "static/*.js",
            "config/*.yaml",
            "wordlists/*.txt"
        ],
    },
    zip_safe=False,
    keywords=[
        "cybersecurity", "penetration testing", "vulnerability scanner",
        "xss", "sql injection", "security", "ethical hacking", "ai security",
        "web security", "network security", "zero-day", "exploit detection",
        "security assessment", "vulnerability assessment", "security toolkit"
    ],
    license="MIT",
    license_files=["LICENSE"],
    platforms=["Linux", "Windows", "macOS"],
    download_url="https://github.com/silverhand/silverhand/archive/v3.0.0.tar.gz",
    
    # Additional metadata
    maintainer="SilverHand Security Team",
    maintainer_email="maintainers@silverhand.dev",
    provides=["silverhand"],
    obsoletes=[],
    requires=[],
    
    # Custom commands
    cmdclass={},
    
    # Test suite
    test_suite="tests",
    tests_require=[
        "pytest>=7.1.0",
        "pytest-cov>=3.0.0",
        "pytest-asyncio>=0.19.0"
    ],
    
    # Scripts and executables
    scripts=[],
    
    # Data files
    data_files=[
        ("silverhand/config", ["config/default.yaml"]),
        ("silverhand/wordlists", ["wordlists/common.txt"]),
        ("silverhand/templates", ["templates/report.html"])
    ],
    
    # Development status
    use_2to3=False,
    use_2to3_fixers=[],
    use_2to3_exclude_fixers=[],
    convert_2to3_doctests=[],
    
    # Egg metadata
    python_module="silverhand",
    
    # Setup requirements
    setup_requires=[
        "setuptools>=45.0.0",
        "wheel>=0.37.0"
    ],
    
    # Dependency links
    dependency_links=[],
    
    # Namespace packages
    namespace_packages=[],
    
    # Eager resources
    eager_resources=[],
    
    # Project URLs for PyPI
    project_urls={
        "Homepage": "https://silverhand.dev/",
        "Repository": "https://github.com/silverhand/silverhand",
        "Documentation": "https://silverhand.readthedocs.io/",
        "Bug Reports": "https://github.com/silverhand/silverhand/issues",
        "Source": "https://github.com/silverhand/silverhand",
        "Tracker": "https://github.com/silverhand/silverhand/issues",
    }
)

# Post-installation message
