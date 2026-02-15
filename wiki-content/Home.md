# Welcome to PipeFrame! 🔄

**Pipe Your Data Naturally**

PipeFrame is a modern, intuitive data manipulation library for Python that makes your data workflows read like natural language. Built on pandas' robust foundation with a clean, pipe-based syntax inspired by R's dplyr and tidyverse.

## Quick

 Links

- 📦 **[Installation](Installation)** - Get started in seconds
- 🚀 **[Quick Start](Quick-Start)** - Your first pipeline in 5 minutes
- 📚 **[API Reference](API-Reference)** - Complete function documentation
- 💡 **[Examples](Examples)** - Real-world use cases
- 🤝 **[Contributing](Contributing)** - Join the community
- ❓ **[FAQ](FAQ)** - Common questions answered

## Installation

```bash
pip install pipeframe
```

## Example

```python
from pipeframe import *

# Read like a story!
result = (df
    >> filter('age > 21')
    >> group_by('city')
    >> summarize(avg_income='mean(income)', count='count()')
    >> arrange('-avg_income')
)
```

> **💡 How to read `>>`:** Read the `>>` operator as **"pipe to"** or **"then"**.

## Key Features

- 🔗 **Intuitive Pipe Operator** (`>>`) - Chain operations naturally
- 📊 **dplyr-Style Verbs** - `filter()`, `select()`, `mutate()`, and more
- 🐼 **100% Pandas Compatible** - Built on pandas, works with pandas
- 🎯 **Readable Syntax** - Code that reads like English
- 🚀 **Production Ready** - Tested, documented, type-hinted

## Resources

- **GitHub**: https://github.com/Yasser03/pipeframe
- **PyPI**: https://pypi.org/project/pipeframe/
- **Issues**: https://github.com/Yasser03/pipeframe/issues
- **Discussions**: https://github.com/Yasser03/pipeframe/discussions

## Community

Join our growing community of data scientists and engineers using PipeFrame!

- Share your pipelines
- Ask questions
- Contribute code
- Report bugs
- Suggest features

**Start Building Better Pipelines Today!** 🚀
