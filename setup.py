#!/usr/bin/env python3
"""
Mining Reliability Dashboard - Package Configuration
Professional analytics platform with clean architecture.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mining-reliability-dashboard",
    version="2.0.0",
    author="Mining Analytics Team",
    description="Professional analytics platform for operational intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "redis>=5.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "mining-dashboard=dashboard.app:main",
            "validate-architecture=dashboard.validation.architecture_validator:main",
            "profile-performance=dashboard.validation.performance_profiler:main",
            "test-integration=dashboard.validation.integration_tester:main",
        ],
    },
    include_package_data=True,
    package_data={
        "configs": ["*.json"],
        "dashboard": ["static/*", "assets/*"],
    },
)
