# PipeFrame - Installation & Publishing Guide

Complete guide for installing, developing, and publishing PipeFrame.

**Author:** Dr. Yasser Mustafa  
**Email:** yasser.mustafan@gmail.com  
**Repository:** https://github.com/Yasser03/pipeframe

---

## 📥 For Users: Installing PipeFrame

### Basic Installation

```bash
# Install from PyPI (once published)
pip install pipeframe

# With all optional dependencies
pip install pipeframe[all]

# With specific features
pip install pipeframe[excel]      # Excel support
pip install pipeframe[parquet]    # Parquet files
pip install pipeframe[sql]        # SQL databases
pip install pipeframe[plot]       # Visualization
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/Yasser03/pipeframe.git
cd pipeframe

# Install in development mode
pip install -e ".[dev,test]"
```

### Verify Installation

```python
import pipeframe
print(pipeframe.__version__)  # Should print: 0.2.0

# Run quickstart
python examples/quickstart.py
```

---

## 🔧 For Developers: Setting Up Development Environment

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/pipeframe.git
cd pipeframe
```

### 2. Create Virtual Environment

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n pipeframe python=3.10
conda activate pipeframe
```

### 3. Install Dependencies

```bash
# Install in editable mode with all dev dependencies
pip install -e ".[dev,test,all]"

# Or from requirements
pip install -r requirements-dev.txt
```

### 4. Set Up Pre-commit Hooks

```bash
pre-commit install
```

### 5. Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=pipeframe --cov-report=html

# Specific test
pytest tests/test_basic.py -v
```

### 6. Code Quality Checks

```bash
# Format code
black pipeframe/
isort pipeframe/

# Lint
flake8 pipeframe/

# Type check
mypy pipeframe/
```

---

## 📦 Building the Package

### Local Build

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build

# This creates:
# - dist/pipeframe-0.2.0-py3-none-any.whl
# - dist/pipeframe-0.2.0.tar.gz
```

### Test the Build

```bash
# Install in clean environment
python -m venv test_env
source test_env/bin/activate
pip install dist/pipeframe-0.2.0-py3-none-any.whl

# Test it works
python -c "from pipeframe import DataFrame; print('Success!')"
```

---

## 🚀 Publishing to PyPI

### First Time Setup

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Verify your email
   - Enable 2FA (recommended)

2. **Create API Token**
   - Go to https://pypi.org/manage/account/
   - Scroll to API tokens section
   - Create new token with scope: "Entire account"
   - Save the token securely!

3. **Configure Token**
   ```bash
   # Create/edit ~/.pypirc
   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```

### Publishing Steps

#### 1. Test on TestPyPI First (Recommended)

```bash
# Register on TestPyPI
# https://test.pypi.org/account/register/

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ pipeframe
```

#### 2. Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Verify
pip install pipeframe
```

### Publishing Checklist

Before publishing, ensure:

- [ ] Version number updated in `pyproject.toml` and `pipeframe/__init__.py`
- [ ] CHANGELOG.md updated with release notes
- [ ] All tests passing: `pytest`
- [ ] Code formatted: `black pipeframe/` and `isort pipeframe/`
- [ ] Documentation updated
- [ ] README.md reviewed
- [ ] LICENSE file present
- [ ] Git tagged: `git tag v0.2.0 && git push --tags`

---

## 🏷️ Version Management

### Semantic Versioning

PipeFrame uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** (0.x.x → 1.0.0): Breaking changes
- **MINOR** (0.2.x → 0.3.0): New features, backward compatible
- **PATCH** (0.2.0 → 0.2.1): Bug fixes

### Update Version

1. **Update version in files:**
   ```python
   # pipeframe/__init__.py
   __version__ = "0.3.0"
   ```
   
   ```toml
   # pyproject.toml
   version = "0.3.0"
   ```

2. **Update CHANGELOG.md:**
   ```markdown
   ## [0.3.0] - 2024-XX-XX
   ### Added
   - New feature description
   ```

3. **Commit and tag:**
   ```bash
   git add .
   git commit -m "Bump version to 0.3.0"
   git tag v0.3.0
   git push && git push --tags
   ```

---

## 🤖 Automated Publishing (GitHub Actions)

### Setup GitHub Secrets

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add new secret: `PYPI_API_TOKEN` with your PyPI token

### Publish on Release

The package is automatically published when you create a GitHub release:

```bash
# Create release on GitHub
# Or use GitHub CLI:
gh release create v0.3.0 \
    --title "PipeFrame v0.3.0" \
    --notes "Release notes here"
```

The GitHub Action (`.github/workflows/publish.yml`) will:
- Run tests
- Build the package
- Upload to PyPI

---

## 📚 Documentation

### Build Documentation Locally

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build docs
cd docs
make html

# View docs
open _build/html/index.html
```

### Deploy Documentation

Documentation can be hosted on:
- **Read the Docs**: https://readthedocs.org (recommended)
- **GitHub Pages**: Use `gh-pages` branch
- **GitLab Pages**: Use `.gitlab-ci.yml`

---

## 🧪 Testing Strategy

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=pipeframe --cov-report=html
# View coverage: open htmlcov/index.html

# Specific module
pytest tests/test_basic.py

# Specific test
pytest tests/test_basic.py::TestDataFrame::test_create_dataframe

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run in parallel
pytest -n auto
```

### Writing Tests

```python
# tests/test_feature.py
import pytest
from pipeframe import DataFrame, filter

class TestNewFeature:
    def test_feature_works(self):
        """Test the feature works correctly."""
        df = DataFrame({'x': [1, 2, 3]})
        result = df >> new_feature()
        assert len(result) > 0
    
    def test_feature_error(self):
        """Test error handling."""
        df = DataFrame({'x': [1, 2, 3]})
        with pytest.raises(ValueError):
            df >> new_feature(invalid_param=True)
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue: `pip install` fails**
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel
```

**Issue: Import errors after install**
```bash
# Reinstall in editable mode
pip uninstall pipeframe
pip install -e .
```

**Issue: Tests fail on import**
```bash
# Install test dependencies
pip install -e ".[test]"
```

**Issue: Version conflicts**
```bash
# Create fresh environment
python -m venv clean_env
source clean_env/bin/activate
pip install pipeframe
```

---

## 📞 Getting Help

- **Issues**: https://github.com/Yasser03/pipeframe/issues
- **Discussions**: https://github.com/Yasser03/pipeframe/discussions
- **Email**: yasser.mustafan@gmail.com

---

## 🎯 Quick Reference

```bash
# Development workflow
git clone https://github.com/Yasser03/pipeframe.git
cd pipeframe
python -m venv venv && source venv/bin/activate
pip install -e ".[dev,test]"
pytest  # Run tests
black pipeframe/ && isort pipeframe/  # Format

# Publishing workflow
# 1. Update version in pyproject.toml and __init__.py
# 2. Update CHANGELOG.md
# 3. Commit and tag
git commit -am "Release v0.3.0"
git tag v0.3.0
# 4. Build
python -m build
# 5. Publish
twine upload dist/*
# 6. Push
git push && git push --tags
```

---

**Maintained by Dr. Yasser Mustafa**

*Built with ❤️ for the data science community*
