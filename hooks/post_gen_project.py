"""
Post-generation script for Cookiecutter project.
Sets up the project with selected package manager and initializes Git repository.
"""
import os
import subprocess
import sys
from typing import List, Optional

# Console colors for better readability
class Colors:
    SUCCESS = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = "\x1b[0m"

# Project configuration from cookiecutter
PACKAGE_MANAGER = "{{cookiecutter.package_manager}}"
PROJECT_NAME = "{{cookiecutter.project_name}}"
PROJECT_SLUG = "{{cookiecutter.project_slug}}"
PROJECT_DESCRIPTION = "{{cookiecutter.project_description}}"
PROJECT_AUTHOR = "{{cookiecutter.project_author}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"

def print_status(message: str, color: str = Colors.INFO) -> None:
    """Print a formatted status message."""
    print(f"{color}{message}{Colors.RESET}")

def run_command(command: List[str], error_message: str = "Command failed") -> bool:
    """
    Run a shell command safely.
    
    Args:
        command: List of command parts to execute
        error_message: Message to display if command fails
    
    Returns:
        bool: True if command succeeded, False otherwise
    """
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print_status(f"Error: {error_message}", Colors.ERROR)
        return False
    
def setup_poetry() -> bool:
    """Set up the project using Poetry."""
    print_status("Installing Poetry...", Colors.INFO)
    if not run_command(["pipx", "install", "poetry"], "Failed to install Poetry"):
        return False

    print_status("Creating pyproject.toml file...", Colors.INFO)
    with open("pyproject.toml", "w") as f:
        f.write(f"""
[tool.poetry]
name = "{PROJECT_SLUG}"
version = "0.1.0"
description = "{PROJECT_DESCRIPTION}"
authors = ["{PROJECT_AUTHOR}"]
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = "^{PYTHON_VERSION}"
ipykernel = "*"
nbformat = "*"
pandas = "*"
numpy = "*"
requests = "*"
plotly = "*"
openpyxl = "*"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
""")
    
    print_status("Creating virtual environment with Poetry...", Colors.INFO)
    if not run_command(["poetry", "env", "use", f"python{PYTHON_VERSION}"], 
                     "Failed to set Python version"):
        return False
    
    if not run_command(["poetry", "install"], "Failed to install dependencies"):
        return False
    
    return True

def setup_uv() -> bool:
    """Set up the project using uv."""
    print_status("Installing uv...", Colors.INFO)
    if not run_command(["pipx", "install", "uv"], "Failed to install uv"):
        return False

    print_status("Creating pyproject.toml file...", Colors.INFO)
    with open("pyproject.toml", "w") as f:
        f.write(f"""
[project]
name = "{PROJECT_SLUG}"
version = "0.1.0"
description = "{PROJECT_DESCRIPTION}"
readme = "README.md"
requires-python = ">={PYTHON_VERSION}"
authors = [
    {{{{name: "{PROJECT_AUTHOR}"}}}}
]

dependencies = [
    "ipykernel",
    "nbformat",
    "pandas",
    "numpy",
    "requests",
    "plotly",
    "openpyxl",
]

[build-system]
requires = ["hatchling>=1.0.0"]
build-backend = "hatchling.build"

[tool.uv]
package-mode = false
""")
    
    print_status("Creating virtual environment with uv...", Colors.INFO)
    if not run_command(["uv", "venv", "--python", f"{PYTHON_VERSION}"], 
                     "Failed to create virtual environment"):
        return False
    
    if not run_command(["uv", "pip", "sync", "pyproject.toml"], 
                     "Failed to install dependencies"):
        return False
    
    return True

def setup_git() -> bool:
    """Initialize git repository with initial commit."""
    print_status("Initializing git repository...", Colors.INFO)
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit"],
        ["git", "branch", "-M", "main"]
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Failed to run {' '.join(cmd)}"):
            return False
    
    return True

def main() -> int:
    """Main function that orchestrates the post-generation setup."""
    print_status(f"Setting up project {PROJECT_NAME} with {PACKAGE_MANAGER}...", Colors.SUCCESS)
    
    success = False
    if PACKAGE_MANAGER == "poetry":
        success = setup_poetry()
    elif PACKAGE_MANAGER == "uv":
        success = setup_uv()
    else:
        print_status(f"Unsupported package manager: {PACKAGE_MANAGER}", Colors.ERROR)
        return 1
    
    if not success:
        print_status("Failed to set up package manager", Colors.ERROR)
        return 1
    
    if not setup_git():
        print_status("Failed to initialize git repository", Colors.ERROR)
        return 1
    
    print_status(f"Your template for {PROJECT_NAME} is ready!", Colors.SUCCESS)
    return 0

if __name__ == "__main__":
    sys.exit(main())