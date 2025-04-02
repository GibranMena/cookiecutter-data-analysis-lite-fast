import pytest
from unittest.mock import mock_open
from hooks.post_gen_project import setup_poetry, setup_uv, setup_git, main, run_command, Colors
import subprocess

def test_setup_poetry_success(mocker):
    mocker.patch('hooks.post_gen_project.run_command', return_value=True)
    mock_open_instance = mock_open()
    mocker.patch('builtins.open', mock_open_instance)
    
    assert setup_poetry() is True
    mock_open_instance.assert_called_once_with("pyproject.toml", "w")

def test_setup_uv_success(mocker):
    mocker.patch('hooks.post_gen_project.run_command', return_value=True)
    mock_open_instance = mock_open()
    mocker.patch('builtins.open', mock_open_instance)
    
    assert setup_uv() is True
    mock_open_instance.assert_called_once_with("requirements.txt", "w")

def test_setup_git_success(mocker):
    mocker.patch('hooks.post_gen_project.run_command', return_value=True)
    
    assert setup_git() is True

def test_unsupported_package_manager_error(mocker):
    mocker.patch('hooks.post_gen_project.PACKAGE_MANAGER', 'unsupported')
    mocker.patch('hooks.post_gen_project.print_status')
    
    assert main() == 1

def test_poetry_installation_failure(mocker):
    mocker.patch('hooks.post_gen_project.run_command', side_effect=[False])
    mock_open_instance = mock_open()
    mocker.patch('builtins.open', mock_open_instance)
    
    assert setup_poetry() is False

def test_git_initialization_failure(mocker):
    mocker.patch('hooks.post_gen_project.run_command', side_effect=[True, True, False])
    
    assert setup_git() is False

def test_pyproject_toml_creation_success(mocker):
    mocker.patch('hooks.post_gen_project.run_command', return_value=True)
    mock_open_instance = mock_open()
    mocker.patch('builtins.open', mock_open_instance)
    
    assert setup_poetry() is True
    mock_open_instance.assert_called_once_with("pyproject.toml", "w")

def test_uv_virtualenv_creation_failure(mocker):
    mocker.patch('hooks.post_gen_project.run_command', side_effect=[True, False])
    mock_open_instance = mock_open()
    mocker.patch('builtins.open', mock_open_instance)
    
    assert setup_uv() is False