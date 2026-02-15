# Examples

Real-world examples of using PipeFrame for data analysis.

## Table of Contents

- [Basic Data Cleaning](#basic-data-cleaning)
- [Sales Analysis](#sales-analysis)
- [Customer Segmentation](#customer-segmentation)
- [Time Series Analysis](#time-series-analysis)
- [Data Joining](#data-joining)

---

## Basic Data Cleaning

```python
from pipeframe import *

cleaned_data = (raw_data
    # Remove missing values
    >> drop_na('critical_column')
    
    # Remove duplicates
    >> distinct()
    
    # Fix data types
    >> define(
        date='pd.to_datetime(date)',
        amount='amount.astype(float)'
    )
    
    # Remove outliers
    >> filter('amount > 0 & amount < 10000')
    
    # Standardize text
    >> define(category='category.str.upper().str.strip()')
)
```

---

## Sales Analysis

Analyze product sales by region and quarter:

```python
from pipeframe import *

sales_summary = (sales_data
    # Data preparation
    >> filter('date >= "2024-01-01" & revenue > 0')
    >> define(
        quarter='pd.to_datetime(date).dt.quarter',
        year='pd.to_datetime(date).dt.year',
        profit='revenue - cost',
        margin='(profit / revenue) * 100'
    )
    
    # Grouping and aggregation
    >> group_by('region', 'product', 'quarter')
    >> summarize(
        total_revenue='sum(revenue)',
        total_profit='sum(profit)',
        avg_margin='mean(margin)',
        num_transactions='count()'
    )
    
    # Filtering and sorting
    >> filter('total_revenue > 10000')
    >> arrange('region', 'quarter', '-total_revenue')
    
    # Final selection
    >> select('region', 'product', 'quarter', 
              'total_revenue', 'total_profit', 'avg_margin')
)

print(sales_summary)
```

---

## Customer Segmentation

Segment customers based on purchase behavior:

```python
from pipeframe import *

customer_segments = (transactions
    # Calculate customer metrics
    >> group_by('customer_id')
    >> summarize(
        total_spent='sum(amount)',
        num_purchases='count()',
        avg_purchase='mean(amount)',
        last_purchase='max(date)'
    )
    
    # Create segments
    >> define(
        value_segment='''
            "High" if total_spent > 1000 else
            "Medium" if total_spent > 500 else
            "Low"
        ''',
        frequency_segment='''
            "Frequent" if num_purchases > 10 else
            "Occasional" if num_purchases > 3 else
            "Rare"
        '''
    )
    
    # Analyze segments
    >> group_by('value_segment', 'frequency_segment')
    >> summarize(
        customer_count='count()',
        avg_spent='mean(total_spent)',
        avg_purchases='mean(num_purchases)'
    )
    >> arrange('-customer_count')
)
```

---

## Time Series Analysis

Analyze trends over time:

```python
from pipeframe import *

monthly_trends = (daily_data
    # Prepare time data
    >> define(
        date='pd.to_datetime(date)',
        year_month='date.dt.to_period("M")'
    )
    
    # Monthly aggregation
    >> group_by('year_month', 'category')
    >> summarize(
        total_sales='sum(sales)',
        avg_daily_sales='mean(sales)',
        max_sales='max(sales)',
        min_sales='min(sales)'
    )
    
    # Calculate month-over-month growth
    >> arrange('category', 'year_month')
    >> group_by('category')
    >> define(mom_growth='(total_sales / total_sales.shift(1) - 1) * 100')
    
    # Filter recent months
    >> filter('year_month >= "2024-01"')
)
```

---

## Data Joining

Combine multiple datasets:

```python
from pipeframe import *

# Simple join
combined = (orders
    >> left_join(customers, on='customer_id')
    >> left_join(products, on='product_id')
)

# Join and aggregate
result = (orders
    >> inner_join(customers, on='customer_id')
    >> filter('customer_age > 25')
    >> group_by('customer_city')
    >> summarize(
        total_orders='count()',
        total_revenue='sum(order_amount)',
        unique_customers='customer_id.nunique()'
    )
    >> arrange('-total_revenue')
)
```

---

## Complex Pipeline Example

A complete end-to-end analysis:

```python
from pipeframe import *

final_report = (raw_sales
    # 1. Data Cleaning
    >> filter('date.notna() & amount > 0')
    >> drop_na('customer_id', 'product_id')
    >> distinct()
    
    # 2. Feature Engineering
    >> define(
        date='pd.to_datetime(date)',
        year='date.dt.year',
        quarter='date.dt.quarter',
        is_weekend='date.dt.dayofweek >= 5',
        revenue_category='''
            "Premium" if amount > 1000 else
            "Standard" if amount > 100 else
            "Budget"
        '''
    )
    
    # 3. Join with reference data
    >> left_join(products, on='product_id')
    >> left_join(customers, on='customer_id')
    
    # 4. Filter relevant data
    >> filter('year == 2024 & customer_status == "Active"')
    
    # 5. Grouping and aggregation
    >> group_by('product_category', 'quarter', 'revenue_category')
    >> summarize(
        total_revenue='sum(amount)',
        total_transactions='count()',
        unique_customers='customer_id.nunique()',
        avg_transaction='mean(amount)',
        weekend_sales='sum(amount * is_weekend)'
    )
    
    # 6. Calculate percentages
    >> define(
        weekend_pct='(weekend_sales / total_revenue) * 100',
        avg_per_customer='total_revenue / unique_customers'
    )
    
    # 7. Final sorting and selection
    >> arrange('quarter', '-total_revenue')
    >> select('product_category', 'quarter', 'revenue_category',
              'total_revenue', 'total_transactions', 
              'unique_customers', 'weekend_pct')
    
    # 8. Top results only
    >> head(20)
)

# Export results
final_report.to_csv('quarterly_report.csv', index=False)
```

---

## Tips for Writing Pipelines

1. **One step at a time**: Test each operation before adding the next
2. **Use meaningful names**: `total_revenue` is better than `rev`
3. **Comment complex logic**: Help future you understand the code
4. **Chain related operations**: Group logical steps together
5. **Use `peek()`**: Debug by viewing intermediate results

## More Resources

- [Quick Start Guide](Quick-Start) - Learn the basics
- [API Reference](API-Reference) - All available functions
- [FAQ](FAQ) - Common questions
