# Changelog

All notable changes to PipeFrame will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2024-02-18

### Added
- **Pedagogical Utilities**
  - Updated `peek()` to support custom message strings (e.g., `peek("Checking results")`)
  - Added `Snapshot` and `profile_pipeline` to top-level `pipeframe` namespace exports

### Fixed
- Fixed missing exports in `pipeframe/__init__.py` ensuring `peek`, `Snapshot`, and `profile_pipeline` are available via `from pipeframe import *`.
- Standardized variable names in Chapter 4 documentation and tutorial notebooks to prevent `KeyError` in piped expressions.

---

## [0.2.0] - 2024-02-14

### 🎉 Initial Public Release

First production-ready release of PipeFrame - a modern data manipulation library for Python.

### Added
- **Core Data Structures**
  - Complete DataFrame implementation with 80+ methods
  - Series wrapper with full pandas compatibility
  - Index implementation
  - Custom exception hierarchy for clear error messages

- **Manipulation Verbs**
  - `define()` / `mutate()` - Create/modify columns with security hardening
  - `filter()` - Filter rows with validated expressions
  - `select()` - Column selection with pattern matching
  - `arrange()` - Intuitive sorting
  - `group_by()` / `summarize()` - Powerful aggregation
  - `rename()`, `distinct()`, `slice_rows()` - Essential operations

- **Conditional Functions**
  - `if_else()` - Vectorized conditional logic
  - `case_when()` - Multiple conditions (optimized with np.select)

- **Selection Helpers**
  - `starts_with()`, `ends_with()`, `contains()` - Pattern matching
  - `matches()` - Regex support
  - `one_of()` - List membership
  - `desc()` - Descending sort helper

- **GroupBy Operations**
  - Complete GroupBy class with all aggregation methods
  - Group manipulation (first, last, head, tail)
  - Apply/transform/filter operations
  - Pipe operator support

- **Reshape Operations** (11 functions)
  - `pivot_wider()` / `pivot_longer()` - Tidyr-style pivoting
  - `pivot()` / `pivot_table()` - Traditional pivoting
  - `melt()` / `gather()` - Unpivot operations
  - `stack()` / `unstack()` - Stack operations
  - `separate()` / `unite()` - Column splitting/combining
  - `transpose()` - Row/column swap

- **I/O Operations** (11 readers, 4 writers)
  - Readers: CSV, TSV, Excel, JSON, Parquet, Feather, SQL, HTML, Clipboard
  - Writers: CSV, Excel, JSON, Parquet
  - Comprehensive parameter support
  - Optional dependencies for different formats

- **Security Features**
  - Expression validation to prevent code injection
  - Blocked patterns: `__import__`, `exec()`, `eval()`, `compile()`, `open()`, `file()`
  - Input type checking
  - Column existence validation
  - Safe expression evaluation with restricted environment

- **Developer Experience**
  - 100% type hints for excellent IDE support
  - Google-style docstrings throughout
  - Comprehensive error messages with suggestions
  - Modern packaging with pyproject.toml

- **Documentation**
  - Complete README with examples
  - Tutorial Jupyter notebook
  - API documentation
  - Contributing guidelines

### Performance
- ~5-15% overhead vs raw pandas
- Vectorized operations where possible
- Efficient column selection
- Memory-conscious design

### Security
- Expression validation prevents code injection attacks
- Comprehensive input sanitization
- Safe evaluation environment

---

## [0.1.0] - 2024-01-15

### Added
- Initial development version
- Basic proof of concept
- Core pipe operator implementation

---

## Upcoming Releases

### [0.3.0] - Planned for Q2 2024
- Join operations (left_join, inner_join, full_join, anti_join)
- Window functions (lead, lag, cumsum, rank)
- Time series helpers
- Enhanced plotting integration
- Performance optimizations
- Copy-on-write support

### [0.4.0] - Planned for Q3 2024
- Lazy evaluation engine
- Alternative backends (Polars, DuckDB)
- Parallel processing support
- SQL generation from pipes
- Interactive data exploration

### [1.0.0] - Planned for Q4 2024
- Stable API with backwards compatibility guarantee
- 100% test coverage
- Complete documentation site
- Production deployment examples
- Performance benchmark suite
- Community-contributed extensions

---

## Support

For questions, issues, or suggestions:
- **GitHub Issues**: https://github.com/Yasser03/pipeframe/issues
- **Discussions**: https://github.com/Yasser03/pipeframe/discussions
- **Email**: yasser.mustafan@gmail.com

---

[0.2.0]: https://github.com/Yasser03/pipeframe/releases/tag/v0.2.0
[0.1.0]: https://github.com/Yasser03/pipeframe/releases/tag/v0.1.0
