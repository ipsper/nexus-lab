#!/usr/bin/env python3
"""
Setup script for nexus-repository-api
This script handles symbolic links by copying the actual files during build.
"""
from setuptools import setup, find_packages
import os
import shutil
import tempfile

def copy_app_files():
    """Copy all files from app/ directory to build-pip/nexus_repository_api/ for setuptools"""
    import shutil
    
    # Source and destination directories
    # Find the root directory (where app/ is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)  # Go up one level from build-pip/ to nexus-lab/
    app_dir = os.path.join(root_dir, 'app')
    package_dir = os.path.join(current_dir, 'nexus_repository_api')
    
    print(f"Copying files from {app_dir} to {package_dir}")
    
    # Files to copy from app/ to nexus_repository_api/
    files_to_copy = ['main.py', 'cli.py', '__init__.py', 'models.py']
    
    # Copy individual files
    for filename in files_to_copy:
        src_file = os.path.join(app_dir, filename)
        dst_file = os.path.join(package_dir, filename)
        
        if os.path.exists(src_file):
            try:
                shutil.copy2(src_file, dst_file)
                print(f"Copied {filename}")
            except Exception as e:
                print(f"Warning: Could not copy {filename}: {e}")
        else:
            print(f"Warning: Source file {src_file} does not exist")
    
    # Copy api/ directory
    api_src_dir = os.path.join(app_dir, 'api')
    api_dst_dir = os.path.join(package_dir, 'api')
    
    if os.path.exists(api_src_dir):
        try:
            # Remove existing api directory if it exists
            if os.path.exists(api_dst_dir):
                shutil.rmtree(api_dst_dir)
            
            # Copy the entire api directory
            shutil.copytree(api_src_dir, api_dst_dir)
            print(f"Copied api/ directory")
        except Exception as e:
            print(f"Warning: Could not copy api/ directory: {e}")
    else:
        print(f"Warning: Source directory {api_src_dir} does not exist")

# Copy app files before setup
copy_app_files()

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="nexus-repository-api",
    version="1.0.0",
    description="En FastAPI-baserad webbapplikation för att hantera Nexus Repository Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IP-solutions Lab Team",
    author_email="per.nehlin@ip-solutions.se",
    url="https://github.com/ip-solutions-lab/nexus-repository-api",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "nexus_repository_api": ["*.txt", "*.md", "*.yaml", "*.yml"],
    },
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nexus-api=nexus_repository_api.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    keywords=["fastapi", "nexus", "repository", "api", "package-manager"],
)
