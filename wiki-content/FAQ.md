# Frequently Asked Questions

## General Questions

### What is PipeFrame?

PipeFrame is a Python library for data manipulation that uses the pipe operator (`>>`) to create readable, chainable data workflows. It's built on pandas but provides a more intuitive syntax inspired by R's dplyr and tidyverse.

### Why use PipeFrame instead of pandas?

PipeFrame doesn't replace pandas - it enhances it! benefits:
- **More Readable**: Workflows read like natural language
- **Less Nesting**: No more deeply nested function calls
- **Easier to Learn**: Consistent verb-based API
- **100% Compatible**: Works seamlessly with pandas

You can mix PipeFrame and pandas freely in the same code.

### Is PipeFrame production-ready?

Yes! PipeFrame is:
- ✅ Tested thoroughly
- ✅ Type-hinted
- ✅ Well-documented
- ✅ Built on proven pandas foundation
- ✅ MIT licensed

---

## Installation & Setup

### How do I install PipeFrame?

```bash
pip install pipeframe
```

### What are the dependencies?

Core dependencies:
- pandas >= 1.5.0
- numpy >= 1.21.0

Optional dependencies available through extras like `pip install pipeframe[excel]`.

### Can I use PipeFrame with Python 3.7?

No, PipeFrame requires Python 3.8 or higher.

---

## Usage

### How do I read the `>>` operator?

Read `>>` as **"then"** or **"pipe to"**:

```python
df >> filter('x > 5')  
# "Take df, THEN filter where x > 5"
```

### Can I use pandas methods with PipeFrame

?

Absolutely! PipeFrame DataFrames are pandas DataFrames:

```python
from pipeframe import DataFrame

df = DataFrame({'x': [1, 2, 3]})

# Mix PipeFrame and pandas
result = (df
    >> filter('x > 1')  # PipeFrame
    .reset_index(drop=True)  # pandas
    >> select('x')  # PipeFrame
)
```

### How do I debug a pipeline?

Use `peek()` to view intermediate results:

```python
result = (df
    >> filter('age > 25')
    >> peek(n=5)  # Shows first 5 rows
    >> define(category='age // 10')
    >> peek()  # Shows first 5 rows again
    >> group_by('category')
)
```

### Can I save intermediate results?

Yes, save to variables:

```python
filtered = df >> filter('age > 25')
with_bonus = filtered >> define(bonus='salary * 0.1')
final = with_bonus >> select('name', 'bonus')
```

---

## Syntax Questions

### What type of expressions can I use in `filter()`?

Any valid pandas query expression:

```python
# Comparisons
df >> filter('age > 25')
df >> filter('name == "Alice"')

# Logic
df >> filter('age > 25 & salary > 50000')
df >> filter('age > 60 | salary > 100000')

# String operations
df >> filter('name.str.startswith("A")')
df >> filter('name.str.contains("Smith")')

# In operator
df >> filter('department in ["Sales", "IT"]')
```

### How do I create calculated columns?

Use `define()` (alias for `mutate()`):

```python
df >> define(
    bonus='salary * 0.1',
    total='salary + bonus',
    is_senior='age > 35'
)
```

### Can I drop columns while selecting?

Yes, use `select()` with exclusion:

```python
# Select everything except id
df >> select('-id')

# Select everything except id and temp columns
df >> select('-id', '-temp')
```

---

## Performance

### Is PipeFrame slower than pandas?

PipeFrame has minimal overhead. It's built on pandas, so most operations are just as fast. The pipe operator adds negligible overhead (<1%).

### Can I use PipeFrame with large datasets?

Yes! PipeFrame uses pandas under the hood, so it handles large datasets as efficiently as pandas does. For very large data (>RAM), consider dask or polars.

### Does PipeFrame support parallel processing?

PipeFrame inherits pandas' performance characteristics. For parallel processing, integrate with dask:

```python
import dask.dataframe as dd
from pipeframe import filter, select

ddf = dd.read_csv('large_file.csv')
result = ddf.compute() >> filter('x > 5') >> select('a', 'b')
```

---

## Errors & Troubleshooting

### I get "AttributeError: 'DataFrame' object has no attribute '>>'"

Make sure you're using PipeFrame's DataFrame:

```python
# Wrong
import pandas as pd
df = pd.DataFrame(...)  # Regular pandas DataFrame

# Right
from pipeframe import DataFrame
df = DataFrame(...)  # PipeFrame DataFrame
```

Or convert:

```python
from pipeframe import DataFrame
df = DataFrame(pandas_df)
```

### My filter expression doesn't work

Check for:
- String columns need quotes: `'name == "Alice"'`
- Use `&` not `and`, `|` not `or`
- Column names with spaces need backticks: `` `column name` ``

### How do I handle missing values in expressions?

```python
# Filter out NA values
df >> filter('column.notna()')

# Replace NA before filtering
df >> define(column='column.fillna(0)') >> filter('column > 0')
```

---

## Integration

### Can I use PipeFrame in Jupyter notebooks?

Yes! PipeFrame works great in Jupyter. DataFrames display exactly like pandas DataFrames.

### Does PipeFrame work with plotting libraries?

Yes! Since PipeFrame DataFrames are pandas DataFrames:

```python
import matplotlib.pyplot as plt

plot_data = df >> filter('year == 2024') >> group_by('month') >> summarize(total='sum(sales)')
plot_data.plot(x='month', y='total', kind='line')
plt.show()
```

### Can I use PipeFrame with sklearn?

Absolutely:

```python
from sklearn.model_selection import train_test_split
from pipeframe import *

# Prepare data
X = data >> select('-target')
y = data >> select('target')

X_train, X_test, y_train, y_test = train_test_split(X, y)
```

---

## Contributing

### How can I contribute?

See our [Contributing Guide](Contributing) for:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Writing documentation

### Where do I report bugs?

Open an issue on GitHub: https://github.com/Yasser03/pipeframe/issues

---

## More Questions?

- Check the [API Reference](API-Reference)
- Join [Discussions](https://github.com/Yasser03/pipeframe/discussions)
- Open an [Issue](https://github.com/Yasser03/pipeframe/issues)
