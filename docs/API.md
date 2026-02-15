# PipeFrame API Reference

**Version:** 0.2.0

Complete API documentation for PipeFrame - the modern, intuitive data manipulation library for Python.

---

## Table of Contents

1. [Core Classes](#core-classes)
   - [DataFrame](#dataframe)
   - [Series](#series)
   - [GroupBy](#groupby)
2. [Data Manipulation Verbs](#data-manipulation-verbs)
   - [filter()](#filter)
   - [define()](#define)
   - [select()](#select)
   - [arrange()](#arrange)
   - [rename()](#rename)
   - [distinct()](#distinct)
3. [Aggregation Verbs](#aggregation-verbs)
   - [group_by()](#group_by)
   - [summarize()](#summarize)
   - [ungroup()](#ungroup)
4. [Reshape Operations](#reshape-operations)
   - [pivot_longer()](#pivot_longer)
   - [pivot_wider()](#pivot_wider)
   - [melt()](#melt)
   - [separate()](#separate)
   - [unite()](#unite)
5. [Conditional Functions](#conditional-functions)
   - [if_else()](#if_else)
   - [case_when()](#case_when)
6. [Column Selection Helpers](#column-selection-helpers)
7. [I/O Operations](#io-operations)
8. [Utility Functions](#utility-functions)

---

## Core Classes

### DataFrame

The main data structure in PipeFrame, wrapping pandas DataFrame with enhanced functionality.

#### Constructor

```python
DataFrame(data=None, index=None, columns=None, **kwargs)
```

**Parameters:**
- `data` : dict, list, ndarray, DataFrame, or Series
  - Data to construct DataFrame from
- `index` : Index or array-like
  - Index to use for resulting frame
- `columns` : Index or array-like
  - Column labels
- `**kwargs` : Additional arguments passed to pandas DataFrame

**Returns:**
- `DataFrame` : PipeFrame DataFrame object

**Examples:**

```python
from pipeframe import DataFrame

# From dictionary
df = DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

# From pandas DataFrame
import pandas as pd
pdf = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
df = DataFrame(pdf)

# From list of dictionaries
df = DataFrame([
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30}
])
```

#### Pipe Operator (`>>`)

Chain operations using the `>>` operator.

```python
df >> operation
```

**Parameters:**
- `operation` : Callable
  - Function to apply to the DataFrame

**Returns:**
- `DataFrame` or `GroupBy` : Result of the operation

**Examples:**

```python
result = (df
    >> filter('age > 25')
    >> define(bonus='salary * 0.1')
    >> select('name', 'bonus')
)
```

#### Properties

- **`shape`** : tuple - Dimensions of the DataFrame (rows, columns)
- **`columns`** : Index - Column labels  
- **`index`** : Index - Row labels
- **`dtypes`** : Series - Data types of each column
- **`empty`** : bool - Whether DataFrame is empty
- **`size`** : int - Number of elements

#### Methods

**`head(n=5)`**
- Return first `n` rows
- **Returns:** DataFrame

**`tail(n=5)`**
- Return last `n` rows  
- **Returns:** DataFrame

**`copy()`**
- Make a deep copy
- **Returns:** DataFrame

**`to_pandas()`**
- Convert to pandas DataFrame
- **Returns:** pd.DataFrame

**I/O Methods:**
- `to_csv(path, **kwargs)` - Write to CSV file
- `to_excel(path, **kwargs)` - Write to Excel file
- `to_json(path, **kwargs)` - Write to JSON file
- `to_parquet(path, **kwargs)` - Write to Parquet file

---

### Series

One-dimensional labeled array, similar to pandas Series.

#### Constructor

```python
Series(data=None, index=None, name=None, **kwargs)
```

**Parameters:**
- `data` : array-like, dict, or scalar
  - Data for the Series
- `index` : array-like or Index
  - Index labels
- `name` : str
  - Name for the Series
- `**kwargs` : Additional arguments

**Examples:**

```python
from pipeframe import Series

# From list
s = Series([1, 2, 3, 4, 5])

# From dict
s = Series({'a': 1, 'b': 2, 'c': 3})

# With index and name
s = Series([10, 20, 30], index=['x', 'y', 'z'], name='values')
```

#### Methods

**`to_frame(name=None)`**
- Convert Series to DataFrame
- **Parameters:** `name` (str) - Column name for resulting DataFrame
- **Returns:** DataFrame

**`to_pandas()`**
- Convert to pandas Series
- **Returns:** pd.Series

---

### GroupBy

Grouped data structure for split-apply-combine operations.

#### Methods

**`summarize(**aggregations)`**
- Aggregate grouped data
- See [summarize()](#summarize) for details

**`ungroup()`**
- Remove grouping
- **Returns:** DataFrame

**`head(n=5)`**
- First `n` rows of each group
- **Returns:** DataFrame

**`tail(n=5)`**
- Last `n` rows of each group
- **Returns:** DataFrame

---

## Data Manipulation Verbs

### filter()

Filter rows based on conditions.

```python
filter(condition: str) -> Callable
```

**Parameters:**
- `condition` : str
  - Boolean expression to filter rows

**Returns:**
- `Callable` : Function that filters a DataFrame

**Examples:**

```python
# Single condition
df >> filter('age > 30')

# Multiple conditions with &
df >> filter('age > 30 & salary > 50000')

# Using OR
df >> filter('(age < 25) | (age > 60)')

# String matching
df >> filter('name.str.contains("Alice")')

# Not null
df >> filter('email.notna()')
```

**Notes:**
- Uses pandas `eval()` for safe expression evaluation
- Supports all pandas comparison operators: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Use `&` for AND, `|` for OR, `~` for NOT
- Parentheses group conditions

---

### define()

Create or modify columns.

```python
define(**columns) -> Callable
```

**Parameters:**
- `**columns` : str or Callable
  - Column definitions as keyword arguments
  - Values can be string expressions or callable functions

**Returns:**
- `Callable` : Function that adds/modifies columns in a DataFrame

**Examples:**

```python
# Simple arithmetic
df >> define(total='price * quantity')

# Multiple columns
df >> define(
    revenue='price * quantity',
    profit='revenue - cost',
    margin='profit / revenue * 100'
)

# Using pandas functions
df >> define(
    month='pd.to_datetime(date).dt.month',
    year='pd.to_datetime(date).dt.year'
)

# String operations
df >> define(
    upper_name='name.str.upper()',
    email='name.str.lower() + "@example.com"'
)

# Callable functions
df >> define(
    category=lambda df: df['value'].apply(lambda x: 'high' if x > 100 else 'low')
)

# Conditional with if_else
df >> define(
    status=if_else('age >= 18', 'adult', 'minor')
)
```

**Supported in Expressions:**
- Pandas module functions: `pd.to_datetime()`, `pd.cut()`, etc.
- NumPy functions: `np.sqrt()`, `np.log()`, etc.
- DataFrame column operations
- String methods: `.str.upper()`, `.str.contains()`, etc.
- DateTime methods: `.dt.year`, `.dt.month`, etc.

---

### select()

Choose columns to keep.

```python
select(*columns) -> Callable
```

**Parameters:**
- `*columns` : str
  - Column names or selection helpers

**Returns:**
- `Callable` : Function that selects columns from a DataFrame

**Examples:**

```python
# Basic selection
df >> select('name', 'age', 'salary')

# Using helpers
df >> select(
    'id',
    starts_with('date_'),
    ends_with('_amount'),
    contains('price')
)

# Column ranges
df >> select('name:salary')  # All columns from 'name' to 'salary'

# Regex patterns
df >> select('id', matches(r'Q\d_sales'))

# Everything except
df >> select('-age', '-salary')  # Remove these columns
```

**Selection Helpers:**
- `starts_with(prefix)` - Columns starting with prefix
- `ends_with(suffix)` - Columns ending with suffix  
- `contains(pattern)` - Columns containing pattern
- `matches(pattern)` - Columns matching regex pattern

---

### arrange()

Sort rows by column values.

```python
arrange(*columns) -> Callable
```

**Parameters:**
- `*columns` : str
  - Column names to sort by
  - Prefix with `-` for descending order

**Returns:**
- `Callable` : Function that sorts a DataFrame

**Examples:**

```python
# Single column ascending
df >> arrange('age')

# Descending
df >> arrange('-salary')

# Multiple columns
df >> arrange('department', '-salary', 'name')

# Mixed ascending/descending
df >> arrange('city', '-age', 'name')
```

---

### rename()

Rename columns.

```python
rename(**renames) -> Callable
```

**Parameters:**
- `**renames` : str
  - Mapping of new_name=old_name

**Returns:**
- `Callable` : Function that renames columns in a DataFrame

**Examples:**

```python
# Single column
df >> rename(customer_name='name')

# Multiple columns
df >> rename(
    emp_id='id',
    emp_name='name',
    emp_age='age'
)

# Chain with other operations
df >> rename(total_sales='sales') >> filter('total_sales > 1000')
```

---

### distinct()

Keep only unique rows.

```python
distinct(*columns, keep='first') -> Callable
```

**Parameters:**
- `*columns` : str, optional
  - Columns to consider for uniqueness
  - If empty, considers all columns
- `keep` : {'first', 'last', False}, default 'first'
  - Which duplicate to keep

**Returns:**
- `Callable` : Function that removes duplicates from a DataFrame

**Examples:**

```python
# All columns
df >> distinct()

# Specific columns
df >> distinct('customer_id')

# Multiple columns
df >> distinct('product', 'store', 'date')

# Keep last occurrence
df >> distinct('email', keep='last')

# Remove all duplicates
df >> distinct('id', keep=False)
```

---

## Aggregation Verbs

### group_by()

Group data by column values.

```python
group_by(*columns) -> Callable
```

**Parameters:**
- `*columns` : str
  - Column names to group by

**Returns:**
- `Callable` : Function that creates a GroupBy object

**Examples:**

```python
# Single column
df >> group_by('category')

# Multiple columns
df >> group_by('category', 'region', 'year')

# Combined with summarize
df >> group_by('department') >> summarize(
    avg_salary='mean(salary)',
    count='count()'
)
```

---

### summarize()

Aggregate grouped data.

```python
summarize(**aggregations) -> Callable
```

**Parameters:**
- `**aggregations` : str
  - Aggregation specifications as keyword arguments
  - Format: `new_col='function(column)'`

**Returns:**
- `Callable` : Function that aggregates a GroupBy or DataFrame

**Aggregation Functions:**
- `count()` - Count rows
- `sum(col)` - Sum values
- `mean(col)` - Average
- `median(col)` - Median
- `min(col)` - Minimum
- `max(col)` - Maximum
- `std(col)` - Standard deviation
- `var(col)` - Variance
- `first(col)` - First value
- `last(col)` - Last value

**Examples:**

```python
# Basic aggregation
df >> group_by('category') >> summarize(
    total='sum(sales)',
    avg='mean(price)',
    count='count()'
)

# Multiple aggregations
df >> group_by('region', 'product') >> summarize(
    total_revenue='sum(revenue)',
    total_units='sum(units)',
    avg_price='mean(price)',
    max_price='max(price)',
    min_price='min(price)',
    num_transactions='count()'
)

# Without grouping (overall statistics)
df >> summarize(
    total_sales='sum(sales)',
    avg_price='mean(price)'
)

# With post-aggregation calculations
df >> group_by('category') >> summarize(
    total='sum(sales)',
    count='count()'
) >> define(
    avg_per_item='total / count'
)
```

---

### ungroup()

Remove grouping from a GroupBy object.

```python
ungroup() -> Callable
```

**Returns:**
- `Callable` : Function that converts GroupBy to DataFrame

**Examples:**

```python
df >> group_by('category') >> ungroup()

# After aggregation
result = (df
    >> group_by('dept')
    >> summarize(avg='mean(salary)')
    >> ungroup()
    >> arrange('-avg')
)
```

---

## Reshape Operations

### pivot_longer()

Convert wide data to long format.

```python
pivot_longer(
    cols,
    names_to='name',
    values_to='value',
    names_prefix=None
) -> Callable
```

**Parameters:**
- `cols` : list of str
  - Columns to pivot longer
- `names_to` : str, default 'name'
  - Name for the new column containing column names
- `values_to` : str, default 'value'
  - Name for the new column containing values
- `names_prefix` : str, optional
  - Prefix to remove from column names

**Examples:**

```python
# Basic pivot
df >> pivot_longer(
    cols=['Q1', 'Q2', 'Q3', 'Q4'],
    names_to='quarter',
    values_to='sales'
)

# Remove prefix
df >> pivot_longer(
    cols=['revenue_2021', 'revenue_2022', 'revenue_2023'],
    names_to='year',
    values_to='revenue',
    names_prefix='revenue_'
)
```

---

### pivot_wider()

Convert long data to wide format.

```python
pivot_wider(
    id_cols=None,
    names_from='name',
    values_from='value',
    values_fill=None
) -> Callable
```

**Parameters:**
- `id_cols` : str or list of str
  - Columns to use as identifiers
- `names_from` : str, default 'name'
  - Column to get new column names from
- `values_from` : str, default 'value'
  - Column to get values from
- `values_fill` : scalar, optional
  - Value to fill for missing combinations

**Examples:**

```python
# Basic pivot
df >> pivot_wider(
    id_cols='student',
    names_from='subject',
    values_from='grade'
)

# With fill value
df >> pivot_wider(
    id_cols=['year', 'month'],
    names_from='category',
    values_from='sales',
    values_fill=0
)
```

---

### melt()

Unpivot DataFrame (similar to pivot_longer).

```python
melt(
    id_vars=None,
    value_vars=None,
    var_name='variable',
    value_name='value'
) -> Callable
```

**Parameters:**
- `id_vars` : list of str, optional
  - Columns to keep as identifiers
- `value_vars` : list of str, optional
  - Columns to unpivot
- `var_name` : str, default 'variable'
  - Name for variable column
- `value_name` : str, default 'value'
  - Name for value column

**Examples:**

```python
df >> melt(
    id_vars=['id', 'name'],
    value_vars=['math', 'science', 'english'],
    var_name='subject',
    value_name='score'
)
```

---

### separate()

Split one column into multiple columns.

```python
separate(
    col,
    into,
    sep='_',
    remove=True
) -> Callable
```

**Parameters:**
- `col` : str
  - Column to separate
- `into` : list of str
  - Names for new columns
- `sep` : str or regex, default '_'
  - Separator pattern
- `remove` : bool, default True
  - Whether to remove original column

**Examples:**

```python
# Split by underscore
df >> separate('full_name', into=['first', 'last'], sep=' ')

# Split by regex
df >> separate('date', into=['year', 'month', 'day'], sep='-')

# Keep original column
df >> separate('code', into=['prefix', 'number'], sep='_', remove=False)
```

---

### unite()

Combine multiple columns into one.

```python
unite(
    col,
    cols,
    sep='_',
    remove=True,
    na_rm=False
) -> Callable
```

**Parameters:**
- `col` : str
  - Name for new combined column
- `cols` : list of str
  - Columns to combine
- `sep` : str, default '_'
  - Separator to use
- `remove` : bool, default True
  - Whether to remove original columns
- `na_rm` : bool, default False
  - Whether to remove NaN values before uniting

**Examples:**

```python
# Combine columns
df >> unite('full_name', ['first', 'last'], sep=' ')

# Custom separator
df >> unite('date', ['year', 'month', 'day'], sep='-')

# Keep original columns
df >> unite('full_address', ['street', 'city', 'zip'], sep=', ', remove=False)
```

---

## Conditional Functions

### if_else()

Vectorized if-else condition.

```python
if_else(condition, true_value, false_value)
```

**Parameters:**
- `condition` : str
  - Boolean expression
- `true_value` : scalar or str
  - Value when condition is True
- `false_value` : scalar or str
  - Value when condition is False

**Returns:**
- Expression that can be used in `define()`

**Examples:**

```python
df >> define(
    status=if_else('age >= 18', 'adult', 'minor'),
    category=if_else('salary > 60000', 'high', 'standard'),
    eligible=if_else('score >= 70', True, False)
)
```

---

### case_when()

Multiple conditional statements (like SQL CASE WHEN).

```python
case_when(*conditions, default=None)
```

**Parameters:**
- `*conditions` : tuple
  - Tuples of (condition, value)
- `default` : scalar, optional
  - Default value when no conditions match

**Returns:**
- Expression for use in `define()`

**Examples:**

```python
df >> define(
    grade=case_when(
        ('score >= 90', 'A'),
        ('score >= 80', 'B'),
        ('score >= 70', 'C'),
        ('score >= 60', 'D'),
        default='F'
    )
)

df >> define(
    segment=case_when(
        ('revenue > 10000 & age < 30', 'Young High Value'),
        ('revenue > 10000 & age >= 30', 'Mature High Value'),
        ('revenue <= 10000 & age < 30', 'Young Standard'),
        default='Mature Standard'
    )
)
```

---

## Column Selection Helpers

### starts_with()

Select columns starting with a prefix.

```python
starts_with(prefix: str) -> list
```

### ends_with()

Select columns ending with a suffix.

```python
ends_with(suffix: str) -> list
```

### contains()

Select columns containing a pattern.

```python
contains(pattern: str) -> list
```

### matches()

Select columns matching a regex pattern.

```python
matches(pattern: str) -> list
```

**Examples:**

```python
df >> select(
    'id',
    starts_with('date_'),
    ends_with('_total'),
    contains('revenue'),
    matches(r'Q[1-4]_\d{4}')
)
```

---

## I/O Operations

### Reading Data

**`read_csv(filepath, **kwargs)`**
- Read CSV file
- **Returns:** DataFrame

**`read_excel(filepath, **kwargs)`**
- Read Excel file
- **Returns:** DataFrame

**`read_json(filepath, **kwargs)`**
- Read JSON file
- **Returns:** DataFrame

**`read_parquet(filepath, **kwargs)`**
- Read Parquet file
- **Returns:** DataFrame

**`read_sql(query, connection, **kwargs)`**
- Read from SQL database
- **Returns:** DataFrame

**`read_clipboard(**kwargs)`**
- Read from clipboard
- **Returns:** DataFrame

**Examples:**

```python
from pipeframe import read_csv, read_excel, read_json

# CSV
df = read_csv('data.csv')
df = read_csv('data.csv', sep=';', encoding='utf-8')

# Excel
df = read_excel('data.xlsx', sheet_name='Sheet1')
df = read_excel('data.xlsx', sheet_name=0)

# JSON
df = read_json('data.json', orient='records')

# Parquet
df = read_parquet('data.parquet')

# SQL
from sqlalchemy import create_engine
engine = create_engine('sqlite:///database.db')
df = read_sql('SELECT * FROM users', engine)

# Clipboard
df = read_clipboard()  # Paste data from Excel/spreadsheet
```

### Writing Data

All write methods are available on DataFrame objects:

**`df.to_csv(filepath, **kwargs)`**
**`df.to_excel(filepath, **kwargs)`**
**`df.to_json(filepath, **kwargs)`**
**`df.to_parquet(filepath, **kwargs)`**

**Examples:**

```python
# CSV
df.to_csv('output.csv', index=False)

# Excel
df.to_excel('report.xlsx', sheet_name='Results', index=False)

# JSON
df.to_json('data.json', orient='records', lines=True)

# Parquet
df.to_parquet('data.parquet', compression='gzip')
```

---

## Utility Functions

### peek()

Quick look at intermediate data in pipelines.

```python
peek(n=5, where='head') -> Callable
```

**Parameters:**
- `n` : int, default 5
  - Number of rows to display
- `where` : {'head', 'tail', 'sample'}, default 'head'
  - Which rows to show

**Examples:**

```python
result = (df
    >> filter('age > 30')
    >> peek(3)  # Shows first 3 rows
    >> define(bonus='salary * 0.1')
    >> peek(5, where='tail')  # Shows last 5 rows
)
```

### Snapshot

Capture and compare DataFrame states.

```python
from pipeframe.utils import Snapshot

snap = Snapshot()

result = (df
    >> snap.capture('after_filter')
    >> filter('x > 50')
    >> snap.capture('after_group')
    >> group_by('category')
)

# Compare snapshots
stats = snap.compare('after_filter', 'after_group')
```

### Decorators

**`@timer`**
- Time function execution

**`@catch_empty(default=None)`**
- Handle empty DataFrames gracefully

**`@validate_columns(*required_cols)`**
- Validate required columns exist

**Examples:**

```python
from pipeframe.utils import timer, catch_empty, validate_columns

@timer
def process_data(df):
    return df >> filter('x > 100') >> group_by('category')

@catch_empty(default=DataFrame())
def get_filtered_data(df):
    return df >> filter('value > 1000')

@validate_columns('name', 'age', 'salary')
def process_employees(df):
    return df >> filter('age > 30')
```

---

## Error Handling

PipeFrame provides custom exceptions for clear error messages:

- **`PipeFrameError`** - Base exception
- **`PipeFrameTypeError`** - Type-related errors
- **`PipeFrameValueError`** - Invalid values
- **`PipeFrameExpressionError`** - Expression evaluation errors
- **`PipeFrameIOError`** - I/O operations errors

**Example:**

```python
from pipeframe.exceptions import PipeFrameExpressionError

try:
    df >> define(bad="__import__('os').system('ls')")
except PipeFrameExpressionError as e:
    print(f"Dangerous expression blocked: {e}")
```

---

## Security Features

PipeFrame validates all expressions to prevent code injection:

**Blocked patterns:**
- `__import__`
- `exec()`
- `eval()`
- `compile()`
- `open()`
- `file()`

**Safe evaluation:**
- Uses pandas `eval()` with restricted environment
- Validates expression syntax
- Limited namespace access

---

## Best Practices

### 1. Use Pipe Operator for Readability

```python
# ✅ Good - readable pipeline
result = (df
    >> filter('age > 25')
    >> define(bonus='salary * 0.1')
    >> select('name', 'salary', 'bonus')
    >> arrange('-bonus')
)

# ❌ Avoid - nested functions
result = arrange(
    select(
        define(
            filter(df, 'age > 25'),
            bonus='salary * 0.1'
        ),
        'name', 'salary', 'bonus'
    ),
    '-bonus'
)
```

### 2. Break Long Pipelines

```python
# Filter and transform
processed = (df
    >> filter('date >= "2024-01-01"')
    >> define(
        revenue='price * quantity',
        profit='revenue - cost'
    )
)

# Aggregate
summary = (processed
    >> group_by('category')
    >> summarize(
        total_revenue='sum(revenue)',
        total_profit='sum(profit)'
    )
)
```

### 3. Use peek() for Debugging

```python
result = (df
    >> filter('value > 0')
    >> peek(3)  # Debug checkpoint
    >> group_by('category')
    >> peek(5, where='tail')  # Check aggregation
    >> summarize(total='sum(value)')
)
```

### 4. Leverage String Expressions

```python
# ✅ Readable and concise
df >> filter('age > 30 & salary > 50000')

# ❌ More verbose
df >> filter(lambda df: (df['age'] > 30) & (df['salary'] > 50000))
```

---

## Complete Example

```python
from pipeframe import *

# Load data
sales = read_csv('sales_data.csv')

# Full analysis pipeline
analysis = (sales
    # Data cleaning
    >> filter('order_date >= "2024-01-01" & revenue > 0')
    >> define(
        quarter='pd.to_datetime(order_date).dt.quarter',
        profit='revenue - cost',
        margin='(profit / revenue) * 100'
    )
    
    # Categorization
    >> define(
        customer_segment=case_when(
            ('total_orders > 10 & revenue > 10000', 'VIP'),
            ('total_orders > 5', 'Regular'),
            default='New'
        )
    )
    
    # Aggregation
    >> group_by('product_category', 'quarter', 'customer_segment')
    >> summarize(
        total_revenue='sum(revenue)',
        total_profit='sum(profit)',
        avg_margin='mean(margin)',
        num_orders='count()',
        unique_customers='nunique(customer_id)'
    )
    
    # Post-aggregation
    >> define(
        profit_per_order='total_profit / num_orders',
        revenue_per_customer='total_revenue / unique_customers'
    )
    
    # Final formatting
    >> arrange('-total_revenue')
    >> select(
        'product_category',
        'quarter',
        'customer_segment',
        'total_revenue',
        'total_profit',
        'avg_margin',
        'num_orders'
    )
)

# Export results
analysis.to_excel('quarterly_analysis.xlsx', sheet_name='Summary')
```

---

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history.

---

## Getting Help

- **GitHub Issues**: https://github.com/Yasser03/pipeframe/issues
- **Discussions**: https://github.com/Yasser03/pipeframe/discussions
- **Email**: yasser.mustafan@gmail.com

---

**Last Updated:** 2026-02-15  
**Version:** 0.2.0  
**License:** MIT
