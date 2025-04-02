"""Script that runs after the Cookiecutter project generation."""
import subprocess
import sys

# ANSI color codes for terminal output
MESSAGE_COLOR = '\033[92m'  # Green
RESET_ALL = "\x1b[0m"

# Get the selected package manager from cookiecutter
PACKAGE_MANAGER = "{{cookiecutter.package_manager}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"
PROJECT_NAME = "{{cookiecutter.project_name}}"


def print_colored(message):
    """Print a message in the defined color."""
    print(f"{MESSAGE_COLOR}{message}{RESET_ALL}")


def run_command(command, error_message=None):
    """
    Run a shell command and handle errors.
    
    Args:
        command (str): The command to execute
        error_message (str, optional): Custom error message if the command fails
    
    Returns:
        bool: True if command succeeded, False otherwise
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        if error_message:
            print(f"Error: {error_message}")
        print(f"Command failed: {command}")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False


def setup_poetry():
    """Set up the project using Poetry."""
    print_colored("Installing Poetry...")
    if not run_command("pipx install poetry", "Failed to install Poetry"):
        return False
    
    print_colored("Initializing Poetry project...")
    # Initialize Poetry project with basic configuration
    if not run_command(f"poetry init --no-interaction --name=\"{PROJECT_NAME.lower().replace(' ', '-')}\" --version=\"0.1.0\"", 
                       "Failed to initialize Poetry project"):
        return False
    
    print_colored("Creating virtual environment with Poetry...")
    if not run_command(f"poetry env use python{PYTHON_VERSION}", 
                       "Failed to create Poetry virtual environment"):
        return False
    
    print_colored("Installing dependencies from requirements.txt...")
    if not run_command("cat requirements.txt | xargs -a - poetry add", 
                      "Failed to install dependencies with Poetry"):
        return False
    
    return True

def setup_uv():
    """Set up the project using uv."""
    print_colored("Installing uv...")
    if not run_command("pipx install uv", "Failed to install uv"):
        return False
    
    print_colored("Creating virtual environment with uv...")
    if not run_command(f"uv venv --python={PYTHON_VERSION}", 
                      "Failed to create uv virtual environment"):
        return False
    
    if not run_command("uv install -r requirements.txt", 
                      "Failed to install dependencies with uv"):
        return False
    
    return True


def initialize_git():
    """Initialize git repository with initial commit."""
    print_colored("Initializing a git repository...")
    commands = [
        "git init",
        "git add .",
        "git commit -m 'Initial commit'",
        "git branch -M main"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Git command failed: {cmd}"):
            return False
    
    return True


def main():
    """Main function to orchestrate the post-generation setup."""
    print_colored(f"Setting up project with {PACKAGE_MANAGER}...")

    if PACKAGE_MANAGER == "poetry":
        success = setup_poetry()
        
    elif PACKAGE_MANAGER == "uv":
        success = setup_uv()
    else:
        print(f"Unsupported package manager: {PACKAGE_MANAGER}")
        return 1
    
    if not success:
        print("Failed to set up the package manager.")
        return 1
    
    if not initialize_git():
        print("Failed to initialize git repository.")
        return 1
    
    print_colored(f"Your template for {PROJECT_NAME} is ready!")
    return 0


if __name__ == "__main__":
    sys.exit(main())