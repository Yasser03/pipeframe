# Quick Start Guide

Get up and running with PipeFrame in 5 minutes!

## Your First Pipeline

```python
from pipeframe import DataFrame, filter, select, arrange

# Create a DataFrame
df = DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 28],
    'salary': [50000, 60000, 70000, 55000],
    'department': ['Sales', 'IT', 'Sales', 'IT']
})

# Build a pipeline
result = (df
    >> filter('age > 27')
    >> select('name', 'salary', 'department')
    >> arrange('-salary')
)

print(result)
```

**Output:**
```
      name  salary department
0  Charlie   70000      Sales
1      Bob   60000         IT
2    David   55000         IT
```

## Core Concepts

### 1. The Pipe Operator (`>>`)

Read `>>` as **"then"** or **"pipe to"**:

```python
df >> filter('x > 5')  # Take df, THEN filter where x > 5
```

### 2. Import Everything

```python
from pipeframe import *
```

This imports all data manipulation functions.

### 3. String Expressions

Most operations use simple string expressions:

```python
df >> filter('age > 30 & salary > 50000')
df >> define(bonus='salary * 0.1')
```

## Common Operations

### Filtering Rows

```python
# Single condition
df >> filter('age > 30')

# Multiple conditions
df >> filter('age > 30 & department == "Sales"')

# String operations
df >> filter('name.str.startswith("A")')
```

### Creating Columns

```python
df >> define(
    bonus='salary * 0.1',
    total='salary + bonus',
    senior='age > 35'
)
```

### Selecting Columns

```python
# Select specific columns
df >> select('name', 'salary')

# Select columns by pattern
df >> select(starts_with('sal'))
```

### Sorting

```python
# Ascending
df >> arrange('age')

# Descending (use minus sign)
df >> arrange('-salary')

# Multiple columns
df >> arrange('department', '-salary')
```

### Grouping and Summarizing

```python
result = (df
    >> group_by('department')
    >> summarize(
       avg_salary='mean(salary)',
        count='count()',
        total='sum(salary)'
    )
)
```

## Complete Example

Here's a realistic data analysis pipeline:

```python
from pipeframe import *

# Sales data analysis
sales_analysis = (sales_data
    # Data cleaning
    >> filter('revenue > 0 & date >= "2024-01-01"')
    >> define(
        quarter='pd.to_datetime(date).dt.quarter',
        profit='revenue - cost',
        margin='(profit / revenue) * 100'
    )
    
    # Grouping and aggregation
    >> group_by('product', 'quarter')
    >> summarize(
        total_revenue='sum(revenue)',
        total_profit='sum(profit)',
        avg_margin='mean(margin)',
        num_sales='count()'
    )
    
    # Final touches
    >> arrange('-total_revenue')
    >> select('product', 'quarter', 'total_revenue', 'total_profit')
)

print(sales_analysis)
```

## Tips for Beginners

1. **Start Simple**: Begin with single operations, then chain them
2. **Use peek()**: Debug your pipeline with `>> peek(n=3)`
3. **Read Aloud**: Say "then" when you see `>>`
4. **Test Expressions**: Try expressions in Python first if unsure

## Next Steps

- [Examples](Examples) - See more real-world examples
- [API Reference](API-Reference) - Learn all available functions
- [FAQ](FAQ) - Common questions answered

**Happy piping!** 🔄
