from setuptools import find_packages, setup

setup(
    name="career-hunter",
    version="0.1.0",
    description="A powerful job scraping tool with a CLI and Web UI.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["main", "server", "config", "models", "utils"],
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "python-jobspy",
        "pandas",
        "requests",
        "beautifulsoup4",
        "termcolor",
        "tabulate",
        "httpx",
    ],
    entry_points={
        "console_scripts": [
            "career-hunter=main:main",
        ],
    },
    python_requires=">=3.10",
)
