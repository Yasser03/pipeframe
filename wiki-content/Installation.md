# Installation Guide

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Basic Installation

Install PipeFrame using pip:

```bash
pip install pipeframe
```

That's it! You're ready to use PipeFrame.

## Verify Installation

```python
import pipeframe
print(pipeframe.__version__)  # Should print: 0.2.0
```

## Optional Dependencies

PipeFrame supports optional features through extra dependencies:

### Excel Support

```bash
pip install pipeframe[excel]
```

Includes: `openpyxl`, `xlrd`

### Parquet Support

```bash
pip install pipeframe[parquet]
```

Includes: `pyarrow`

### SQL Support

```bash
pip install pipeframe[sql]
```

Includes: `sqlalchemy`

### Plotting Support

```bash
pip install pipeframe[plot]
```

Includes: `matplotlib`, `seaborn`, `plotnine`

### All Optional Dependencies

```bash
pip install pipeframe[all]
```

## Development Installation

For contributing to PipeFrame:

```bash
# Clone the repository
git clone https://github.com/Yasser03/pipeframe.git
cd pipeframe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev,test]"
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade pipeframe
```

## Uninstalling

```bash
pip uninstall pipeframe
```

## Troubleshooting

### Import Error

If you get an import error, make sure pipeframe is installed:

```bash
pip list | grep pipeframe
```

### Version Conflicts

If you have dependency conflicts, try creating a fresh virtual environment:

```bash
python -m venv fresh_env
source fresh_env/bin/activate
pip install pipeframe
```

### Windows-Specific Issues

On Windows, if you encounter path issues, try:

```bash
python -m pip install pipeframe
```

## Next Steps

- [Quick Start Guide](Quick-Start) - Learn the basics
- [Examples](Examples) - See PipeFrame in action
- [API Reference](API-Reference) - Explore all functions
