"""Tests for the dependency_checker module."""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.dependency_checker import (
    DependencyInfo,
    check_dependencies,
    get_installed_packages,
    get_latest_version,
    get_outdated_dependencies,
)


SAMPLE_PIP_OUTPUT = json.dumps([
    {"name": "requests", "version": "2.28.0"},
    {"name": "flask", "version": "2.3.0"},
])


@patch("subprocess.run")
def test_get_installed_packages(mock_run):
    mock_run.return_value = MagicMock(stdout=SAMPLE_PIP_OUTPUT)
    packages = get_installed_packages()
    assert packages == {"requests": "2.28.0", "flask": "2.3.0"}


@patch("urllib.request.urlopen")
def test_get_latest_version_success(mock_urlopen):
    payload = json.dumps({"info": {"version": "2.31.0"}}).encode()
    mock_response = MagicMock()
    mock_response.read.return_value = payload
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    mock_urlopen.return_value = mock_response

    version = get_latest_version("requests")
    assert version == "2.31.0"


@patch("urllib.request.urlopen", side_effect=Exception("network error"))
def test_get_latest_version_failure(mock_urlopen):
    version = get_latest_version("nonexistent-package")
    assert version is None


def test_check_dependencies_outdated():
    packages = {"requests": "2.28.0"}
    with patch("src.dependency_checker.get_latest_version", return_value="2.31.0"):
        results = check_dependencies(packages)
    assert len(results) == 1
    assert results[0].is_outdated is True
    assert results[0].latest_version == "2.31.0"


def test_check_dependencies_up_to_date():
    packages = {"flask": "2.3.0"}
    with patch("src.dependency_checker.get_latest_version", return_value="2.3.0"):
        results = check_dependencies(packages)
    assert results[0].is_outdated is False


def test_check_dependencies_skips_unknown():
    packages = {"mystery-lib": "1.0.0"}
    with patch("src.dependency_checker.get_latest_version", return_value=None):
        results = check_dependencies(packages)
    assert results == []


def test_get_outdated_dependencies_filters_correctly():
    fake_packages = {"requests": "2.28.0", "flask": "2.3.0"}
    fake_deps = [
        DependencyInfo("requests", "2.28.0", "2.31.0", True),
        DependencyInfo("flask", "2.3.0", "2.3.0", False),
    ]
    with patch("src.dependency_checker.get_installed_packages", return_value=fake_packages), \
         patch("src.dependency_checker.check_dependencies", return_value=fake_deps):
        outdated = get_outdated_dependencies()
    assert len(outdated) == 1
    assert outdated[0].name == "requests"
