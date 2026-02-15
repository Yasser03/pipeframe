# PipeFrame 🔄

**Pipe Your Data Naturally**

[![PyPI version](https://img.shields.io/pypi/v/pipeframe.svg)](https://pypi.org/project/pipeframe/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, intuitive data manipulation library for Python that makes your data workflows read like natural language. Built on pandas' robust foundation with a clean, pipe-based syntax inspired by R's dplyr and tidyverse.

```python
from pipeframe import *

# Your data pipeline reads like a story
result = (df
    >> filter('age > 21')
    >> group_by('city')  
    >> summarize(avg_income='mean(income)', count='count()')
    >> arrange('-avg_income')
)
```

---

## 🌟 Why PipeFrame?

### **Readability First**
```python
# ❌ Traditional pandas: Hard to read
df[df['age'] > 30].groupby('dept')['salary'].mean().sort_values(ascending=False)

# ✅ PipeFrame: Clear and intuitive
df >> filter('age > 30') >> group_by('dept') >> summarize(avg='mean(salary)') >> arrange('-avg')
```

### **Key Features**

- 🔗 **Pipe Operator `>>`** - Natural method chaining without nested parentheses
- 📝 **String Expressions** - Write conditions as readable strings: `'age > 30 & salary > 50000'`
- 🔒 **Security Hardened** - Built-in expression validation prevents code injection
- 🐼 **Pandas Compatible** - Works seamlessly with existing pandas DataFrames
- 🎯 **Type Safe** - Full type hints for excellent IDE support and autocomplete
- ⚡ **Performance** - Only ~5-15% overhead vs raw pandas
- 📊 **Rich I/O** - Read/write CSV, Excel, JSON, Parquet, SQL, and more
- 🔄 **Powerful Reshaping** - Tidyr-style pivoting, melting, and transformations
- 🛡️ **Production Ready** - Comprehensive error handling and validation

---

## 🚀 Quick Start

### Installation

```bash
# Basic installation
pip install pipeframe

# With all optional dependencies
pip install pipeframe[all]

# Specific features
pip install pipeframe[excel]      # Excel support
pip install pipeframe[parquet]    # Parquet files
pip install pipeframe[sql]        # SQL databases
pip install pipeframe[plot]       # Visualization
```

### Hello PipeFrame!

```python
from pipeframe import *

# Create a DataFrame
df = DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'age': [25, 32, 37, 29],
    'salary': [50000, 65000, 72000, 58000],
    'dept': ['Engineering', 'Marketing', 'Engineering', 'Sales']
})

# Transform with intuitive verbs
result = (df
    >> filter('age > 30')
    >> define(
        bonus='salary * 0.1',
        total='salary + bonus'
    )
    >> select('name', 'dept', 'total')
    >> arrange('-total')
)

print(result)
#       name          dept    total
# 0  Charlie  Engineering  79200.0
# 1      Bob     Marketing  71500.0
```

---

## 📚 Core Concepts

### The Pipe Operator `>>`

Chain operations naturally without nested function calls:

```python
# Traditional approach (hard to read)
result = arrange(
    select(
        define(
            filter(df, 'age > 25'),
            experience='2024 - start_year'
        ),
        'name', 'experience', 'salary'
    ),
    '-salary'
)

# PipeFrame approach (reads like a recipe)
result = (df
    >> filter('age > 25')
    >> define(experience='2024 - start_year')
    >> select('name', 'experience', 'salary')
    >> arrange('-salary')
)
```

### Core Verbs

| Verb | Purpose | Example |
|------|---------|---------|
| `define()` | Create/modify columns | `>> define(total='price * quantity')` |
| `filter()` | Filter rows | `>> filter('age > 30 & city == "NYC"')` |
| `select()` | Choose columns | `>> select('name', 'age', 'salary')` |
| `arrange()` | Sort data | `>> arrange('-salary', 'name')` |
| `group_by()` | Group data | `>> group_by('category', 'region')` |
| `summarize()` | Aggregate | `>> summarize(total='sum(sales)', avg='mean(price)')` |
| `rename()` | Rename columns | `>> rename(customer_id='cid')` |
| `distinct()` | Unique rows | `>> distinct('product', 'store')` |

---

## 🔥 Advanced Features

### Conditional Logic

```python
# if_else for binary conditions
df >> define(
    status=if_else('salary > 60000', 'High', 'Standard'),
    category=if_else('age >= 30', 'Senior', 'Junior')
)

# case_when for multiple conditions
df >> define(
    grade=case_when(
        ('score >= 90', 'A'),
        ('score >= 80', 'B'),
        ('score >= 70', 'C'),
        ('score >= 60', 'D'),
        default='F'
    )
)
```

### GroupBy Operations

```python
# Summary by group
summary = (df
    >> group_by('department', 'location')
    >> summarize(
        headcount='count()',
        avg_salary='mean(salary)',
        total_sales='sum(sales)',
        top_performer='max(performance_score)'
    )
    >> arrange('-avg_salary')
)

# Multiple aggregations
analysis = (df
    >> group_by('product_category')
    >> summarize(
        units_sold='sum(quantity)',
        revenue='sum(price * quantity)',
        avg_price='mean(price)',
        num_transactions='count()'
    )
    >> define(
        avg_transaction_value='revenue / num_transactions'
    )
)
```

### Data Reshaping

```python
# Pivot wider (long to wide)
wide = (df
    >> pivot_wider(
        id_cols='student',
        names_from='subject',
        values_from='grade'
    )
)

# Pivot longer (wide to long)
long = (df
    >> pivot_longer(
        cols=['Q1_sales', 'Q2_sales', 'Q3_sales', 'Q4_sales'],
        names_to='quarter',
        values_to='sales'
    )
)

# Separate columns
separated = df >> separate('full_name', into=['first', 'last'], sep=' ')

# Unite columns
united = df >> unite('full_date', ['year', 'month', 'day'], sep='-')
```

### Column Selection Helpers

```python
# Select by pattern
df >> select(
    'id',
    starts_with('date_'),      # All columns starting with 'date_'
    ends_with('_amount'),      # All columns ending with '_amount'
    contains('price'),         # All columns containing 'price'
    matches(r'Q\d_sales')      # Regex pattern matching
)

# Column ranges
df >> select('id', 'name:salary')  # Select from 'name' to 'salary'
```

### I/O Operations

```python
# Read from various sources
df = read_csv('data.csv')
df = read_excel('data.xlsx', sheet_name='Sales')
df = read_json('data.json', orient='records')
df = read_parquet('data.parquet')
df = read_sql('SELECT * FROM users', connection)
df = read_clipboard()  # Paste from spreadsheet!

# Write to different formats
df.to_csv('output.csv', index=False)
df.to_excel('report.xlsx', sheet_name='Results')
df.to_parquet('data.parquet', compression='gzip')
df.to_json('data.json', orient='records', lines=True)
```

---

## 🎯 Real-World Examples

### Sales Analysis Pipeline

```python
from pipeframe import *

# Load and analyze sales data
analysis = (
    read_csv('sales_data.csv')
    >> filter('date >= "2024-01-01" & revenue > 0')
    >> define(
        profit='revenue - cost',
        margin='profit / revenue * 100',
        quarter='pd.to_datetime(date).dt.quarter'
    )
    >> group_by('product_category', 'quarter')
    >> summarize(
        total_revenue='sum(revenue)',
        total_profit='sum(profit)',
        avg_margin='mean(margin)',
        num_sales='count()'
    )
    >> define(
        profit_per_sale='total_profit / num_sales'
    )
    >> arrange('-total_revenue')
)

# Export results
analysis.to_excel('quarterly_analysis.xlsx', sheet_name='Summary')
```

### Customer Segmentation

```python
# Segment customers by behavior
segments = (df
    >> filter('total_purchases > 0')
    >> define(
        avg_order_value='total_spent / total_purchases',
        recency_days='(pd.Timestamp.now() - last_purchase_date).dt.days',
        segment=case_when(
            ('avg_order_value > 100 & recency_days < 30', 'Premium Active'),
            ('avg_order_value > 100 & recency_days >= 30', 'Premium At Risk'),
            ('recency_days < 30', 'Standard Active'),
            ('recency_days < 90', 'At Risk'),
            default='Churned'
        )
    )
    >> group_by('segment')
    >> summarize(
        customers='count()',
        total_value='sum(total_spent)',
        avg_value='mean(total_spent)'
    )
)
```

### Data Cleaning Pipeline

```python
# Clean and standardize data
clean_data = (
    read_excel('messy_data.xlsx')
    >> filter('id.notna()')  # Remove rows without ID
    >> define(
        # Standardize text fields
        name='name.str.title().str.strip()',
        email='email.str.lower().str.strip()',
        # Parse dates
        signup_date='pd.to_datetime(signup_date)',
        # Fill missing values
        phone='phone.fillna("Not Provided")',
        # Create derived fields
        account_age_days='(pd.Timestamp.now() - signup_date).dt.days'
    )
    >> distinct('email', keep='first')  # Deduplicate by email
    >> arrange('signup_date')
)
```

---

## 🔒 Security Features

PipeFrame includes built-in security features to prevent code injection:

```python
# ✅ Safe expressions are allowed
df >> define(total='price * quantity')
df >> filter('age > 30 & city == "NYC"')

# ❌ Dangerous expressions are blocked
df >> define(bad="__import__('os').system('rm -rf /')")
# PipeFrameExpressionError: Expression contains dangerous pattern

# All string expressions are validated before execution
# - Blocks: __import__, exec(), eval(), compile(), open(), file()
# - Validates expression syntax
# - Uses pandas' restricted eval environment
```

---

## 📊 Performance

PipeFrame adds minimal overhead while dramatically improving code readability:

**Benchmarks (1M rows):**
- Filter operation: ~8% overhead
- GroupBy aggregation: ~12% overhead  
- Complex pipeline (5 operations): ~10% overhead

**Why the overhead is worth it:**
- 🧠 Reduced cognitive load
- 🐛 Fewer bugs from clearer intent
- ⚡ Faster development time
- 👥 Easier code review
- 📚 Better maintainability

---

## 🎓 Learning Resources

- **[Tutorial Notebook](examples/tutorial.ipynb)** - Complete walkthrough
- **[API Reference](docs/API.md)** - Detailed documentation
- **[Examples](examples/)** - Real-world use cases
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🐛 **Report bugs** - Open an issue
2. 💡 **Suggest features** - Share your ideas
3. 📝 **Improve docs** - Help others learn
4. 🔧 **Submit PRs** - Fix bugs or add features

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Dr. Yasser Mustafa**

*AI & Data Science Specialist | Theoretical Physics PhD*

- 🎓 PhD in Theoretical Nuclear Physics
- 💼 10+ years in production AI/ML systems
- 🔬 48+ research publications
- 🏢 Experience: Government (Abu Dhabi), Media (Track24), Recruitment (Reed), Energy (ADNOC)
- 📍 Based in Newcastle Upon Tyne, UK
- ✉️ yasser.mustafan@gmail.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/yasser-mustafa-phd-72886344/) | [GitHub](https://github.com/Yasser03)

**PipeFrame** was born from years of working with data pipelines in production environments, combining the elegance of R's tidyverse with Python's practicality.

---

## 🌟 Star History

If PipeFrame helps your work, please consider giving it a star! ⭐

---

## 📈 Roadmap

### Current (v0.2.0)
- ✅ Core verbs and operators
- ✅ Security hardening
- ✅ Comprehensive I/O
- ✅ Reshape operations
- ✅ Type hints

### Upcoming (v0.3.0)
- [ ] Join operations (left_join, inner_join, etc.)
- [ ] Window functions
- [ ] Time series helpers
- [ ] Enhanced plotting integration
- [ ] Performance optimizations

### Future (v1.0.0)
- [ ] Lazy evaluation engine
- [ ] Alternative backends (Polars, DuckDB)
- [ ] Distributed computing support
- [ ] Interactive data exploration tools
- [ ] SQL generation from pipes

---

## 💬 Community

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions, share use cases

---

**Built with ❤️ for data scientists who value readability**

*Make your data speak naturally with PipeFrame* 🔄
