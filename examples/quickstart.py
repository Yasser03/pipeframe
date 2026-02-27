"""
PipeFrame Quickstart Example

A quick introduction to PipeFrame's core features.
Author: Dr. Yasser Mustafa
"""

from pipeframe import *


def main():
    print("🔄 PipeFrame Quickstart\n")
    print("=" * 60)

    # Create sample data
    print("\n1️⃣  Creating DataFrame...")
    employees = DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "age": [25, 32, 37, 29, 41],
            "salary": [50000, 65000, 72000, 58000, 85000],
            "dept": ["Engineering", "Marketing", "Engineering", "Sales", "Engineering"],
        }
    )
    print(employees)

    # Simple filter
    print("\n2️⃣  Filter (age > 30)...")
    seniors = employees >> filter("age > 30")
    print(seniors)

    # Create new columns
    print("\n3️⃣  Adding bonus column...")
    with_bonus = (
        employees
        >> define(bonus="salary * 0.1", total="salary + bonus")
        >> select("name", "salary", "bonus", "total")
    )
    print(with_bonus)

    # Group and summarize
    print("\n4️⃣  Department summary...")
    dept_stats = (
        employees
        >> group_by("dept")
        >> summarize(count="count()", avg_salary="mean(salary)", max_salary="max(salary)")
        >> arrange("-avg_salary")
    )
    print(dept_stats)

    # Complex pipeline
    print("\n5️⃣  Complex pipeline...")
    result = (
        employees
        >> filter("age >= 30")
        >> define(seniority=if_else("age >= 40", "Senior", "Mid-level"), bonus="salary * 0.15")
        >> select("name", "dept", "salary", "bonus", "seniority")
        >> arrange("-salary")
    )
    print(result)

    print("\n" + "=" * 60)
    print("✅ Quickstart complete!")
    print("\nNext steps:")
    print("  - Check out examples/tutorial.ipynb for full tutorial")
    print("  - Read the docs: https://pipeframe.readthedocs.io")
    print("  - Star on GitHub: https://github.com/Yasser03/pipeframe")


if __name__ == "__main__":
    main()
