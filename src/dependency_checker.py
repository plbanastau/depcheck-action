"""Module for checking outdated Python dependencies using pip and PyPI."""

import json
import subprocess
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class DependencyInfo:
    name: str
    current_version: str
    latest_version: str
    is_outdated: bool

    def __repr__(self) -> str:
        return (
            f"DependencyInfo(name={self.name!r}, "
            f"current={self.current_version!r}, "
            f"latest={self.latest_version!r}, "
            f"outdated={self.is_outdated})"
        )


def get_installed_packages() -> dict[str, str]:
    """Return a mapping of package name -> installed version."""
    result = subprocess.run(
        ["pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        check=True,
    )
    packages = json.loads(result.stdout)
    return {pkg["name"].lower(): pkg["version"] for pkg in packages}


def get_latest_version(package_name: str) -> Optional[str]:
    """Fetch the latest version of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except Exception:
        return None


def check_dependencies(packages: dict[str, str]) -> list[DependencyInfo]:
    """Check each package against PyPI and return dependency info list."""
    results: list[DependencyInfo] = []
    for name, current_version in packages.items():
        latest = get_latest_version(name)
        if latest is None:
            continue
        is_outdated = latest != current_version
        results.append(
            DependencyInfo(
                name=name,
                current_version=current_version,
                latest_version=latest,
                is_outdated=is_outdated,
            )
        )
    return results


def get_outdated_dependencies() -> list[DependencyInfo]:
    """Convenience function: return only outdated dependencies."""
    packages = get_installed_packages()
    all_deps = check_dependencies(packages)
    return [dep for dep in all_deps if dep.is_outdated]
