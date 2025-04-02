""" Script that runs after the project generation"""
import os

MESSAGE_COLOR = '\033[92m'
RESET_ALL = "\x1b[0m"

# Get the selected package manager from cookiecutter
package_manager = "{{cookiecutter.package_manager}}"
project_name = "{{cookiecutter.project_name}}"

print(f"{MESSAGE_COLOR}Setting up project with {package_manager}...{RESET_ALL}")

if package_manager == "poetry":
    # Install poetry
    print(f"{MESSAGE_COLOR}Installing Poetry...{RESET_ALL}")
    os.system("pipx install poetry")

    # Create pyproject.toml - Note the removal of indentation
    print(f"{MESSAGE_COLOR}Creating pyproject.toml file...{RESET_ALL}")
    with open("pyproject.toml", "w") as f:
        f.write("""[tool.poetry]
name = "{{cookiecutter.project_slug}}"
version = "0.1.0"
description = "{{cookiecutter.project_description}}"
authors = ["{{cookiecutter.project_author}}"]
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = "^3.8"
ipykernel = "^6.0.3"
nbformat = "^5.1.3"
pandas = "^1.3.0"
numpy = "^1.21.0"
requests = "^2.26.0"
plotly = "^5.3.1"
openpyxl = "^3.0.9"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
""")
    
    # Install virtual environment and synchronize packages
    print(f"{MESSAGE_COLOR}Creating virtual environment with Poetry...{RESET_ALL}")
    os.system(f"poetry env use python{{{cookiecutter.python_version}}}")
    os.system("poetry install")
    
elif package_manager == "uv":
    # Install uv
    print(f"{MESSAGE_COLOR}Installing uv...{RESET_ALL}")
    os.system("pipx install uv")
    
    # Set up virtual environment with uv
    print(f"{MESSAGE_COLOR}Creating virtual environment with uv...{RESET_ALL}")
    os.system(f"uv venv --python={{{cookiecutter.python_version}}}")
    os.system("uv pip install -r requirements.txt")

# Initialize git (common for both package managers)
print(f"{MESSAGE_COLOR}Initializing a git repository...{RESET_ALL}")
os.system("git init && git add . && git commit -m 'Initial commit' && git branch -M main")

# Final message
print(f"{MESSAGE_COLOR}Your template for {{cookiecutter.project_name}} is ready!{RESET_ALL}")