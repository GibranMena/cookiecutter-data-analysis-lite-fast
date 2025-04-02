#!/usr/bin/env python
"""Script that runs before the project generation to validate inputs."""
import os
import re
import sys
from typing import Optional

# ANSI color codes for terminal output
ERROR_COLOR = "\x1b[31m"  # Red
MESSAGE_COLOR = "\x1b[34m"  # Blue
RESET_ALL = "\x1b[0m"

# Validation constants
MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
PROJECT_SLUG = "{{cookiecutter.project_slug}}"


def print_colored(message: str, color: str = MESSAGE_COLOR) -> None:
    """
    Print a message with color formatting.
    
    Args:
        message: The message to print
        color: ANSI color code to use
    """
    print(f"{color}{message}{RESET_ALL}")


def validate_project_slug(slug: str) -> Optional[str]:
    """
    Validate that the project slug is a valid Python module name.
    
    Args:
        slug: The project slug to validate
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not re.match(MODULE_REGEX, slug):
        return (
            f"ERROR: The project slug '{slug}' is not a valid Python module name. "
            f"Please use _ instead of - and ensure it starts with a letter or underscore, "
            f"followed by letters, numbers, or underscores."
        )
    return None


def main() -> int:
    """
    Main function to run pre-generation validation.
    
    Returns:
        Exit code (0 for success, 1 for errors)
    """
    # Validate the project slug
    error = validate_project_slug(PROJECT_SLUG)
    if error:
        print_colored(error, ERROR_COLOR)
        return 1
    
    # Display creation message
    current_dir = os.getcwd()
    print_colored(f"Creating '{PROJECT_SLUG}' at {current_dir}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())