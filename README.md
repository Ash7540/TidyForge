# TidyForge

[![CI](https://github.com/Ash7540/TidyForge/actions/workflows/ci.yml/badge.svg)](https://github.com/Ash7540/TidyForge/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://github.com/Ash7540/TidyForge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**TidyForge** is a modular, extensible, high-performance Python library that simplifies data cleaning for Pandas DataFrames through an intuitive, chainable API.

---

## Key Features

- **Chainable API**: Expressive, fluent interface for combining multiple data cleaning operations cleanly.
- **Modular Architecture**: Separate dedicated modules for handling missing data, duplicates, type conversions, text, dates, numbers, contact info, outliers, and validation.
- **Extensible**: Plugin-ready architecture for custom rules and transformations.
- **Reporting & Pipeline**: Built-in quality scoring, HTML/JSON report generation, and reusable cleaning pipeline configurations.
- **Zero Heavy AI Dependencies**: High performance using core scientific computing standards (`pandas` & `numpy`).

---

## Installation

```bash
pip install tidyforge
```

*(For development)*

```bash
git clone https://github.com/Ash7540/TidyForge.git
cd TidyForge
pip install -e .[dev]
```

---

## Quickstart Preview

```python
import pandas as pd
import tidyforge as tf

df = pd.read_csv("data.csv")

# Clean data using chainable methods
clean_df = (
    tf.Cleaner(df)
    .drop_missing(threshold=0.5)
    .impute_missing(strategy="median")
    .remove_duplicates()
    .clean_text(columns=["name", "email"], case="lower", strip=True)
    .to_dataframe()
)
```

---

## Development & Roadmap

TidyForge is currently following a 60-day development plan toward version 1.0.0.

See [plan.txt](plan.txt) for the full architectural roadmap.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
