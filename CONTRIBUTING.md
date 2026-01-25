# Contributing to OCR-LLM Distributed Chat

First off, thank you for considering contributing to OCR-LLM! 🎉 It's people like you that make OCR-LLM such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Python version, Ollama version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* End all files with a newline
* Update documentation as needed

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add streaming response display

Add real-time token streaming to improve perceived performance.
This includes performance metrics logging.

Fixes #123
```

### Python Styleguide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and use [Black](https://github.com/psf/black) for code formatting.

* Use type hints for function parameters and return types
* Write docstrings for all functions and classes
* Maximum line length: 88 characters (Black default)
* Use descriptive variable names
* Comment non-obvious logic

Example:
```python
def extract_text_from_doc(uploaded_file: UploadedFile) -> str:
    """
    Extract text from uploaded document (PDF or text file).
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text or error message
        
    Raises:
        ValueError: If file format is not supported
    """
    # Implementation here
    pass
```

### Documentation Style

* Use Markdown for all documentation
* Include code examples where applicable
* Keep documentation up-to-date with code changes
* Link to relevant issues and PRs

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/OCR-LLM-DIST.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements-dev.txt`
6. Create a new branch: `git checkout -b feature/your-feature-name`
7. Make your changes
8. Run tests and linting
9. Commit and push your changes
10. Submit a pull request

## Testing

* Write tests for new features
* Ensure all tests pass before submitting PR
* Aim for >80% code coverage for new code

Run tests:
```bash
pytest
```

## Code Quality

We use several tools to maintain code quality:

```bash
# Format code
black .

# Lint code
pylint services/ utils/

# Type checking
mypy .
```

## Documentation

* Update README.md if adding new features
* Update docstrings for modified functions
* Keep examples up-to-date

## Recognition

Contributors will be recognized in:
* README.md contributors section
* Release notes for substantial contributions

## Questions?

* Open a GitHub discussion
* Create an issue with your question

Thank you for contributing! 🚀
