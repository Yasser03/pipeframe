"""
Real-world example: Sales Analysis with PipeFrame

Demonstrates a complete sales analysis pipeline.
Author: Dr. Yasser Mustafa
"""

from pipeframe import *
import numpy as np

# Generate sample sales data
np.random.seed(42)
n_sales = 1000

sales = DataFrame(
    {
        "date": pd.date_range("2024-01-01", periods=n_sales, freq="H"),
        "product": np.random.choice(["Widget", "Gadget", "Doohickey", "Thingamajig"], n_sales),
        "region": np.random.choice(["North", "South", "East", "West"], n_sales),
        "quantity": np.random.randint(1, 20, n_sales),
        "unit_price": np.random.choice([10.99, 24.99, 49.99, 99.99], n_sales),
        "customer_type": np.random.choice(["New", "Returning", "Premium"], n_sales),
    }
)

print("🔄 Sales Analysis Pipeline\n")
print("=" * 70)

# Main analysis pipeline
analysis = (
    sales
    >> define(
        # Calculate revenue and costs
        revenue="quantity * unit_price",
        cost="quantity * unit_price * 0.6",  # 40% margin
        profit="revenue - cost",
        margin="profit / revenue * 100",
        # Extract time components
        month="date.dt.month",
        day_of_week="date.dt.dayofweek",
        hour="date.dt.hour",
    )
    >> filter("revenue > 0")  # Ensure valid sales
    >> group_by("product", "region")
    >> summarize(
        total_sales="count()",
        total_revenue="sum(revenue)",
        total_profit="sum(profit)",
        avg_margin="mean(margin)",
        avg_order_size="mean(quantity)",
    )
    >> define(
        # Derived metrics
        revenue_per_sale="total_revenue / total_sales",
        profit_per_sale="total_profit / total_sales",
    )
    >> arrange("-total_revenue")
)

print("\n📊 Top Product-Region Combinations by Revenue:\n")
print(analysis.head(10))

# Customer type analysis
customer_analysis = (
    sales
    >> define(revenue="quantity * unit_price")
    >> group_by("customer_type")
    >> summarize(
        customers="count()",
        total_revenue="sum(revenue)",
        avg_order_value="mean(revenue)",
        total_units="sum(quantity)",
    )
    >> define(revenue_per_customer="total_revenue / customers")
    >> arrange("-total_revenue")
)

print("\n\n👥 Customer Type Analysis:\n")
print(customer_analysis)

# Time-based analysis
hourly_analysis = (
    sales
    >> define(revenue="quantity * unit_price", hour="date.dt.hour")
    >> group_by("hour")
    >> summarize(sales_count="count()", total_revenue="sum(revenue)", avg_revenue="mean(revenue)")
    >> arrange("hour")
)

print("\n\n⏰ Sales by Hour of Day:\n")
print(hourly_analysis)

print("\n" + "=" * 70)
print("✅ Analysis complete!")
