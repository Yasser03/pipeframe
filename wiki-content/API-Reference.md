# API Reference

Complete reference for all PipeFrame functions and classes.

## Table of Contents

- [Core Classes](#core-classes)
- [Data Selection](#data-selection)
- [Data Filtering](#data-filtering)
- [Data Transformation](#data-transformation)
- [Grouping & Aggregation](#grouping--aggregation)
- [Joining & Combining](#joining--combining)
- [Sorting & Ordering](#sorting--ordering)
- [Reshaping](#reshaping)
- [Utilities](#utilities)

---

## Core Classes

### DataFrame

PipeFrame's enhanced DataFrame class.

```python
from pipeframe import DataFrame

df = DataFrame(data, columns=None, index=None)
```

**Arguments:**
- `data`: dict, array, or pandas DataFrame
- `columns`: column labels (optional)
- `index`: row labels (optional)

**Returns:** PipeFrame DataFrame (fully compatible with pandas)

**Example:**
```python
df = DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
```

### Series

Enhanced Series class with pipe support.

```python
from pipeframe import Series

s = Series(data, index=None, name=None)
```

---

## Data Selection

### select()

Select columns from DataFrame.

```python
df >> select(*columns)
```

**Arguments:**
- `*columns`: Column names to select

**Special patterns:**
- `starts_with('prefix')`: Columns starting with prefix
- `ends_with('suffix')`: Columns ending with suffix
- `contains('text')`: Columns containing text
- `matches('regex')`: Columns matching regex
- `-column`: Exclude column

**Examples:**
```python
# Select specific columns
df >> select('name', 'age', 'salary')

# Select with patterns
df >> select(starts_with('sales_'))

# Exclude columns
df >> select('-temp', '-id')
```

---

## Data Filtering

### filter() / where()

Filter rows based on conditions.

```python
df >> filter(condition)
df >> where(condition)  # Alias
```

**Arguments:**
- `condition`: String expression for filtering

**Examples:**
```python
# Simple condition
df >> filter('age > 25')

# Multiple conditions with &
df >> filter('age > 25 & salary > 50000')

# Or conditions with |
df >> filter('department == "Sales" | department == "IT"')

# String operations
df >> filter('name.str.startswith("A")')
df >> filter('city.str.contains("York")')

# IN operator
df >> filter('status in ["Active", "Pending"]')
```

---

## Data Transformation

### define() / mutate()

Create or modify columns.

```python
df >> define(**kwargs)
df >> mutate(**kwargs)  # Alias
```

**Arguments:**
- `**kwargs`: name=expression pairs

**Examples:**
```python
# Create new column
df >> define(bonus='salary * 0.1')

# Multiple columns
df >> define(
    bonus='salary * 0.1',
    total='salary + bonus',
    is_senior='age > 35'
)

# Complex expressions
df >> define(
    category='''
        "High" if amount > 1000 else
        "Medium" if amount > 500 else
        "Low"
    '''
)
```

### drop()

Drop columns.

```python
df >> drop(*columns)
```

**Examples:**
```python
df >> drop('temp_column')
df >> drop('col1', 'col2', 'col3')
```

### rename()

Rename columns.

```python
df >> rename(mapper, **kwargs)
```

**Examples:**
```python
# Using dict
df >> rename({'old_name': 'new_name'})

# Using kwargs
df >> rename(old_name='new_name')
```

---

## Grouping & Aggregation

### group_by()

Group DataFrame by columns.

```python
df >> group_by(*columns)
```

**Examples:**
```python
df >> group_by('department')
df >> group_by('department', 'location')
```

### summarize() / summarise()

Aggregate grouped data.

```python
grouped_df >> summarize(**kwargs)
grouped_df >> summarise(**kwargs)  # British spelling
```

**Arguments:**
- `**kwargs`: name='aggregation_function(column)' pairs

**Common aggregations:**
- `mean(column)`: Average
- `sum(column)`: Total
- `count()`: Count rows
- `min(column)`: Minimum
- `max(column)`: Maximum
- `std(column)`: Standard deviation
- `nunique(column)`: Count unique values

**Examples:**
```python
result = (df
    >> group_by('department')
    >> summarize(
        avg_salary='mean(salary)',
        total_employees='count()',
        max_salary='max(salary)'
    )
)
```

### count()

Count observations.

```python
df >> count(*columns)
```

**Examples:**
```python
# Count all rows
df >> count()

# Count by group
df >> count('department')
df >> count('department', 'location')
```

---

## Joining & Combining

### left_join()

Left outer join.

```python
df >> left_join(right, on=None, left_on=None, right_on=None)
```

### right_join()

Right outer join.

```python
df >> right_join(right, on=None, left_on=None, right_on=None)
```

### inner_join()

Inner join.

```python
df >> inner_join(right, on=None, left_on=None, right_on=None)
```

### full_join()

Full outer join.

```python
df >> full_join(right, on=None, left_on=None, right_on=None)
```

**Examples:**
```python
# Join on common column
result = orders >> left_join(customers, on='customer_id')

# Join on different column names
result = orders >> left_join(
    customers, 
    left_on='cust_id', 
    right_on='id'
)
```

### bind_rows()

Concatenate DataFrames vertically.

```python
df >> bind_rows(other)
```

### bind_cols()

Concatenate DataFrames horizontally.

```python
df >> bind_cols(other)
```

---

## Sorting & Ordering

### arrange() / order_by()

Sort DataFrame by columns.

```python
df >> arrange(*columns)
df >> order_by(*columns)  # Alias
```

**Arguments:**
- `*columns`: Column names (prefix with `-` for descending)

**Examples:**
```python
# Ascending
df >> arrange('age')

# Descending (use - prefix)
df >> arrange('-salary')

# Multiple columns
df >> arrange('department', '-salary')
```

---

## Reshaping

### pivot_wider()

Pivot from long to wide format.

```python
df >> pivot_wider(id_cols, names_from, values_from)
```

### pivot_longer()

Pivot from wide to long format.

```python
df >> pivot_longer(cols, names_to='name', values_to='value')
```

**Examples:**
```python
# Wide to long
long_df = (wide_df
    >> pivot_longer(
        cols=['Q1', 'Q2', 'Q3', 'Q4'],
        names_to='quarter',
        values_to='sales'
    )
)

# Long to wide
wide_df = (long_df
    >> pivot_wider(
        id_cols='product',
        names_from='quarter',
        values_from='sales'
    )
)
```

---

## Utilities

### head()

Return first n rows.

```python
df >> head(n=5)
```

### tail()

Return last n rows.

```python
df >> tail(n=5)
```

### sample()

Random sample of rows.

```python
df >> sample(n=None, frac=None)
```

**Examples:**
```python
# Sample 10 rows
df >> sample(n=10)

# Sample 10% of rows
df >> sample(frac=0.1)
```

### distinct()

Remove duplicate rows.

```python
df >> distinct(*columns)
```

**Examples:**
```python
# Remove all duplicate rows
df >> distinct()

# Remove duplicates based on columns
df >> distinct('customer_id', 'date')
```

### drop_na()

Drop rows with missing values.

```python
df >> drop_na(*columns)
```

**Examples:**
```python
# Drop rows with any NA
df >> drop_na()

# Drop rows with NA in specific columns
df >> drop_na('critical_column')
```

### fill_na()

Fill missing values.

```python
df >> fill_na(value, **kwargs)
```

**Examples:**
```python
# Fill all NAs with 0
df >> fill_na(0)

# Fill specific columns
df >> fill_na(age=0, salary=50000)
```

### peek()

View intermediate results (for debugging).

```python
df >> peek(n=5)
```

**Example:**
```python
result = (df
    >> filter('age > 25')
    >> peek(n=3)  # Shows first 3 rows
    >> define(bonus='salary * 0.1')
    >> peek()  # Shows first 5 rows
)
```

---

## Column Selectors

### starts_with()

Select columns starting with prefix.

```python
df >> select(starts_with('sales_'))
```

### ends_with()

Select columns ending with suffix.

```python
df >> select(ends_with('_total'))
```

### contains()

Select columns containing text.

```python
df >> select(contains('amount'))
```

### matches()

Select columns matching regex pattern.

```python
df >> select(matches(r'\\d{4}'))  # Columns with 4 digits
```

---

## More Information

- [Quick Start Guide](Quick-Start) - Learn the basics
- [Examples](Examples) - Real-world use cases
- [FAQ](FAQ) - Common questions

**Need help?** Open an issue https://github.com/Yasser03/pipeframe/issues
