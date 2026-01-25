"""
Setup script for OCR-LLM Distributed Chat application.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ocr-llm-chat",
    version="1.0.0",
    author="Akshay",
    description="A distributed chat application with OCR and LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ax5hay/OCR-LLM-DIST",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.22.0",
        "PyMuPDF>=1.23.7",
        "loguru>=0.7.2",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "black>=23.12.1",
            "pylint>=3.0.3",
            "mypy>=1.8.0",
            "pytest>=7.4.4",
            "pre-commit>=3.6.0",
        ],
        "remote": [
            "pyngrok>=5.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ocr-llm-chat=app:main",
        ],
    },
)
