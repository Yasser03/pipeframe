# Contributing to PipeFrame

First off, thank you for considering contributing to PipeFrame! It's people like you that make PipeFrame such a great tool for the data science community.

---

## 🌟 Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please open an issue with:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Code samples
- Environment details (Python version, OS, pipeframe version)

### 💡 Suggest Features

Have an idea? We'd love to hear it! Include:
- Use case description
- Proposed API (how it would work)
- Example code showing the feature
- Why it would be useful

### 📝 Improve Documentation

Help others learn PipeFrame:
- Fix typos or clarify explanations
- Add examples
- Create tutorials
- Improve docstrings

### 🔧 Submit Code

Ready to code? Awesome! See development setup below.

---

## 🚀 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/pipeframe.git
cd pipeframe
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n pipeframe python=3.10
conda activate pipeframe
```

### 3. Install Development Dependencies

```bash
# Install package in editable mode with dev dependencies
pip install -e ".[dev,test]"

# Or install from requirements
pip install -r requirements-dev.txt
```

### 4. Set Up Pre-commit Hooks

```bash
pre-commit install
```

---

## 🔨 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 2. Make Changes

Follow these guidelines:
- Write clear, readable code
- Add docstrings (Google style)
- Include type hints
- Add tests for new features
- Update documentation

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pipeframe --cov-report=html

# Run specific test
pytest tests/test_dataframe.py::test_filter
```

### 4. Format Code

```bash
# Format with black
black pipeframe/

# Sort imports
isort pipeframe/

# Lint
flake8 pipeframe/

# Type check
mypy pipeframe/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add amazing new feature"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots/examples if applicable

---

## 📋 Code Style Guide

### Python Style

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use isort for import sorting
- Type hints required for public APIs

### Docstrings

Use Google style:

```python
def awesome_function(param1: str, param2: int = 0) -> DataFrame:
    """
    Brief description of what this does.
    
    More detailed explanation if needed. Can span multiple
    lines and include usage notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2. Defaults to 0.
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is empty
    
    Examples:
        >>> result = awesome_function("hello", 42)
        >>> print(result)
    """
    pass
```

### Type Hints

```python
from typing import Any, List, Optional, Union
from pipeframe.core.dataframe import DataFrame

def process_data(
    df: Union[DataFrame, pd.DataFrame],
    columns: Optional[List[str]] = None,
    **kwargs: Any
) -> DataFrame:
    ...
```

---

## 🧪 Testing Guidelines

### Writing Tests

```python
import pytest
from pipeframe import DataFrame, filter, define

class TestDataFrame:
    def test_filter_basic(self):
        """Test basic filtering functionality."""
        df = DataFrame({'x': [1, 2, 3, 4]})
        result = df >> filter('x > 2')
        assert len(result) == 2
    
    def test_filter_empty_result(self):
        """Test filtering that returns no rows."""
        df = DataFrame({'x': [1, 2, 3]})
        result = df >> filter('x > 10')
        assert len(result) == 0
    
    def test_filter_invalid_column(self):
        """Test error handling for invalid column."""
        df = DataFrame({'x': [1, 2, 3]})
        with pytest.raises(PipeFrameColumnError):
            df >> filter('y > 2')
```

### Test Organization

- One test file per module
- Test classes for related tests
- Clear test names describing what's tested
- Test both success and error cases
- Test edge cases

---

## 📚 Documentation Guidelines

### README Updates

- Keep examples simple and focused
- Ensure all code examples actually work
- Update table of contents if adding sections

### API Documentation

- Every public function/class needs docstring
- Include parameters, returns, raises
- Add usage examples
- Note any security considerations

### Tutorial Notebooks

- Start simple, build complexity
- Explain the "why" not just "how"
- Include real-world examples
- Test all code cells

---

## 🔍 Code Review Process

### What We Look For

- ✅ Tests pass
- ✅ Code is formatted (black, isort)
- ✅ Type hints present
- ✅ Docstrings complete
- ✅ No breaking changes (or clearly documented)
- ✅ Performance impact considered
- ✅ Security implications reviewed

### Review Timeline

- Initial response: Within 2 days
- Full review: Within 1 week
- Revisions: As needed

---

## 🎯 Priority Areas

We especially welcome contributions in:

1. **Performance Optimization**
   - Profiling and benchmarking
   - Vectorization improvements
   - Memory efficiency

2. **Additional Verbs**
   - Join operations
   - Window functions
   - Time series helpers

3. **Backend Support**
   - Polars integration
   - DuckDB support
   - Arrow format

4. **Documentation**
   - More examples
   - Video tutorials
   - Translation

5. **Testing**
   - Edge case coverage
   - Performance tests
   - Integration tests

---

## 💬 Communication

### Getting Help

- **GitHub Discussions**: Ask questions, share ideas
- **Issues**: Bug reports, feature requests
- **Email**: yasser.mustafan@gmail.com

### Proposing Major Changes

For substantial changes:
1. Open an issue first
2. Discuss the approach
3. Get feedback before coding
4. Then submit PR

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Annual contributor highlight

---

## ❓ Questions?

Don't hesitate to ask! We're here to help:
- Open a discussion on GitHub
- Email: yasser.mustafan@gmail.com
- Tag @Yasser03 in issues

Thank you for making PipeFrame better! 🎉