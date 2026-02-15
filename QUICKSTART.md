# PipeFrame Quick Start Guide

Get up and running with PipeFrame in 5 minutes!

## Installation

```bash
pip install pipeframe
```

## Your First Pipeline

```python
from pipeframe import *

# Create data
df = DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 32, 37],
    'salary': [50000, 65000, 72000]
})

# Transform with pipes
result = (df
    >> filter('age > 30')
    >> define(bonus='salary * 0.1')
    >> select('name', 'salary', 'bonus')
    >> arrange('-salary')
)

print(result)
```

## Core Concepts

### 1. The Pipe Operator `>>`

Chain operations naturally:

```python
df >> operation1 >> operation2 >> operation3
```

### 2. String Expressions

Write conditions as readable strings:

```python
df >> filter('age > 30 & salary > 50000')
df >> define(bonus='salary * 0.1')
```

### 3. Essential Verbs

| Verb | What It Does |
|------|--------------|
| `filter()` | Keep rows matching condition |
| `define()` | Create/modify columns |
| `select()` | Choose columns |
| `arrange()` | Sort rows |
| `group_by()` | Group data |
| `summarize()` | Aggregate groups |

## Common Patterns

### Filter and Transform

```python
result = (df
    >> filter('status == "active"')
    >> define(total='quantity * price')
    >> select('customer', 'total')
)
```

### Group and Aggregate

```python
summary = (df
    >> group_by('category')
    >> summarize(
        count='count()',
        total='sum(amount)',
        average='mean(amount)'
    )
)
```

### Sort and Limit

```python
top_10 = (df
    >> arrange('-revenue')
    >> slice_rows(0, 10)
)
```

## Next Steps

- 📘 **Full Tutorial**: `examples/tutorial.ipynb`
- 📚 **Documentation**: https://pipeframe.readthedocs.io
- 💡 **Examples**: `examples/` directory
- ❓ **Questions**: Open an issue on GitHub

---

**Author**: Dr. Yasser Mustafa  
**Email**: yasser.mustafan@gmail.com
