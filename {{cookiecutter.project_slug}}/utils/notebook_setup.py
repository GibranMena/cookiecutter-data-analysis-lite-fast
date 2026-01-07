"""
Notebook setup utilities for fixing paths and initializing the environment.
"""

import os
from pathlib import Path


def setup_notebook_environment():
    """
    Fixes absolute and relative paths for folders and notebooks.
    
    This function ensures that the working directory is set to the project root,
    regardless of where the notebook is executed from.
    """
    if Path.cwd().name == '_notebooks':
        os.chdir('..')  # Go to project root
    elif not (Path.cwd() / '_notebooks').exists():
        # Find and change to project root
        for parent in Path.cwd().parents:
            if (parent / '_notebooks').exists():
                os.chdir(parent)
                break
    
    print(f"Working directory set to: {Path.cwd()}")
