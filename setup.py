#!/usr/bin/env python3
"""
Setup script for Daltonismo Test System
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="daltonismo-test",
    version="1.0.0",
    author="Developer Team",
    author_email="dev@example.com",
    description="Sistema completo de detección de daltonismo para Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/daltonismo-test",
    project_urls={
        "Bug Tracker": "https://github.com/username/daltonismo-test/issues",
        "Documentation": "https://github.com/username/daltonismo-test/wiki",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
        ],
        "rpi": [
            "RPi.GPIO>=0.7.1",
        ],
        "full": [
            "matplotlib>=3.7.0",
            "opencv-python>=4.8.0",
            "scipy>=1.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "daltonismo-test=dalton:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.png", "*.jpg"],
    },
    zip_safe=False,
    keywords="daltonism colorblind test medical raspberry-pi ishihara",
    platforms=["Linux", "Raspberry Pi OS"],
)