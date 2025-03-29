from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="teamcraft-api",
    version="0.1.0",
    author="Luna",
    author_email="",
    description="CLI tool to fetch and process FFXIV Teamcraft API data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Luna-Salamanca/TeamcraftAPI-status-extract",
    packages=find_packages(include=["teamcraft_api", "teamcraft_api.*"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "ruff>=0.0.1",
            "build>=0.10.0",
            "typing-extensions>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "teamcraft-api=teamcraft_api.main:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords=["ffxiv", "teamcraft", "api", "cli", "xivapi", "json", "game-data"],
    project_urls={
        "Bug Tracker": "https://github.com/Luna-Salamanca/TeamcraftAPI-status-extract/issues",
        "Documentation": "https://github.com/Luna-Salamanca/TeamcraftAPI-status-extract#readme",
        "Source Code": "https://github.com/Luna-Salamanca/TeamcraftAPI-status-extract",
    },
)
