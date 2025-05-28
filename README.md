# Advanced Messy Data Generator

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/advanced-messy-data-generator.svg)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/advanced-messy-data-generator.svg)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/advanced-messy-data-generator.svg)

A sophisticated Python tool that transforms clean datasets into realistic messy datasets for testing data cleaning and quality processes. This generator intelligently analyzes your input data and creates expanded datasets with various types of data quality issues commonly found in real-world scenarios.

## 🎯 Purpose

This tool is designed for:
- **Data Engineers** testing ETL pipelines and data validation rules
- **Data Scientists** training data cleaning models and algorithms
- **QA Teams** validating data processing systems
- **Developers** testing applications with realistic messy data
- **Students** learning data cleaning techniques with hands-on examples

## ✨ Key Features

### Intelligent Data Analysis
- Automatically detects column types (numeric, datetime, categorical, text)
- Preserves data patterns and distributions from your original dataset
- Generates realistic variations based on existing data patterns

### Comprehensive Messiness Generation
- **Smart Duplicates**: Creates both exact and near-duplicates with subtle variations
- **Strategic Nulls**: Introduces missing values with realistic patterns
- **Range Violations**: Generates out-of-bounds values for numeric columns
- **Timestamp Corruption**: Creates invalid dates and time anomalies
- **Text Corruption**: Introduces various text quality issues (case changes, special characters, truncation)

### Customizable Parameters
- Full control over messiness rates for each type of issue
- Configurable output size (scale up or down from original dataset)
- Flexible input/output formats (CSV, JSON)


## Final Project Structure 📋

Your final repository should look like this:
<details>
advanced-messy-data-generator/
├── .github/
│ └── ISSUE_TEMPLATE/
│ ├── bug_report.md
│ └── feature_request.md
├── examples/
│ └── sample_data.csv
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── python_standalone.py
└── requirements.txt
</details>

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- Minimum 2GB RAM (4GB+ recommended for large datasets)
- Disk space: ~3x the size of your input file

### Dependencies
```bash
pip install pandas numpy
```

**Core Dependencies:**
- `pandas >= 1.3.0` - Data manipulation and analysis
- `numpy >= 1.20.0` - Numerical computing
- `datetime` - Date/time handling (built-in)
- `random` - Random data generation (built-in)
- `string` - String manipulation (built-in)
- `os` - Operating system interface (built-in)
- `argparse` - Command-line argument parsing (built-in)

## 🚀 Installation

### Method 1: Direct Download
1. Download `python_standalone.py`
2. Install dependencies: `pip install pandas numpy`
3. Run the script directly

### Method 2: Clone Repository
```bash
git clone <repository-url>
cd messy-data-generator
pip install pandas numpy
```

### Method 3: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv messy_data_env

# Activate environment
# On Windows:
messy_data_env\Scripts\activate
# On macOS/Linux:
source messy_data_env/bin/activate

# Install dependencies
pip install pandas numpy
```

## 💻 Usage

### Command Line Interface

#### Basic Usage
```bash
python python_standalone.py input_file.csv
```

#### Advanced Usage with Custom Parameters
```bash
python python_standalone.py input_file.csv \
    --output messy_output.csv \
    --rows 50000 \
    --duplicates 0.20 \
    --nulls 0.15 \
    --wrong-ranges 0.10 \
    --wrong-timestamps 0.08 \
    --text-corruption 0.12
```

### Command Line Arguments

| Argument | Short | Description | Default | Range |
|----------|-------|-------------|---------|-------|
| `input_file` | - | Path to input CSV/JSON file | Required | - |
| `--output` | `-o` | Output file path | `messy_data.csv` | - |
| `--rows` | `-r` | Target number of output rows | `10000` | 1+ |
| `--duplicates` | `-d` | Duplicate rate (fraction) | `0.15` | 0.0-1.0 |
| `--nulls` | `-n` | Null value rate (fraction) | `0.10` | 0.0-1.0 |
| `--wrong-ranges` | `-w` | Wrong range value rate | `0.08` | 0.0-1.0 |
| `--wrong-timestamps` | `-t` | Invalid timestamp rate | `0.05` | 0.0-1.0 |
| `--text-corruption` | `-c` | Text corruption rate | `0.05` | 0.0-1.0 |

### Programmatic Usage

```python
import pandas as pd
from python_standalone import AdvancedMessyDataGenerator

# Load your clean data
clean_df = pd.read_csv('clean_data.csv')

# Initialize generator
generator = AdvancedMessyDataGenerator(clean_df)

# Generate messy data
messy_df = generator.generate_messy_data(
    target_rows=15000,
    duplicate_rate=0.18,
    null_rate=0.12,
    wrong_range_rate=0.10,
    wrong_timestamp_rate=0.06,
    text_corruption_rate=0.08
)

# Analyze the results
analysis = generator.analyze_data_quality(messy_df)

# Save results
messy_df.to_csv('generated_messy_data.csv', index=False)
```

## 🔧 Functionality Details

### Data Type Detection
The generator automatically identifies and handles:

- **Numeric Columns**: Integers, floats, percentages
- **Datetime Columns**: Timestamps, dates, times
- **Categorical Columns**: Limited unique values, categories
- **Text Columns**: Free-form text, names, descriptions

### Messiness Types Generated

#### 1. Smart Duplicates (15% default)
- **Exact Duplicates**: Perfect copies of existing rows
- **Near Duplicates**: Rows with subtle differences like:
  - Trailing/leading spaces
  - Case variations (UPPER, lower, Mixed)
  - Missing spaces or punctuation
  - Minor spelling variations

#### 2. Strategic Null Values (10% default)
- **Higher probability** in text and categorical columns
- **Clustered patterns** mimicking real-world data loss
- **Random distribution** across all column types

#### 3. Range Violations (8% default)
- **Below minimum**: Values lower than expected range
- **Above maximum**: Values higher than expected range
- **Extreme outliers**: Clearly invalid values (-999999, 999999)
- **Edge cases**: Zero values where inappropriate

#### 4. Timestamp Corruption (5% default)
- **Historical dates**: Years like 1900, 1970 (epoch)
- **Future dates**: Unrealistic future timestamps
- **Invalid dates**: NaT (Not a Time) values
- **Format inconsistencies**: Mixed date formats

#### 5. Text Corruption (5% default)
- **Case corruption**: Random upper/lowercase changes
- **Character replacement**: Random character substitution
- **Text reversal**: Backwards text strings
- **Empty strings**: Blank values
- **Special characters**: Addition of ???, !!!, etc.
- **Text duplication**: Repeated content

## 📊 Output Files

### Generated Files
1. **Main Output**: `messy_data.csv` (or specified filename)
   - Contains the generated messy dataset
   - Same column structure as input
   - Expanded to specified row count

2. **Analysis Report**: `messy_data_analysis.txt`
   - Data quality summary
   - Duplicate counts and percentages
   - Null value statistics by column
   - Memory usage information
   - Data type analysis

### Analysis Report Example
```
Data Quality Analysis Report
==============================
Original file: clean_sales.csv
Generated file: messy_sales.csv
Dataset shape: (10000, 8)
Duplicates: 1500
Null counts: {'customer_name': 450, 'email': 380, 'phone': 290}
Memory usage: 2.34 MB
```

## 🎛️ Configuration Examples

### Light Messiness (Testing)
```bash
python python_standalone.py data.csv \
    --duplicates 0.05 \
    --nulls 0.03 \
    --wrong-ranges 0.02 \
    --wrong-timestamps 0.01 \
    --text-corruption 0.02
```

### Heavy Messiness (Stress Testing)
```bash
python python_standalone.py data.csv \
    --duplicates 0.30 \
    --nulls 0.25 \
    --wrong-ranges 0.20 \
    --wrong-timestamps 0.15 \
    --text-corruption 0.20
```

### Large Dataset Generation
```bash
python python_standalone.py small_sample.csv \
    --rows 1000000 \
    --output large_messy_dataset.csv
```

## 🚨 Troubleshooting

### Common Issues

#### Memory Errors
**Problem**: Out of memory errors with large datasets
**Solution**: 
- Reduce `--rows` parameter
- Process in smaller batches
- Increase system RAM
- Use more efficient data types

#### File Format Errors
**Problem**: "Unsupported file format" error
**Solution**:
- Ensure input file is `.csv` or `.json`
- Check file encoding (UTF-8 recommended)
- Verify file is not corrupted

#### Performance Issues
**Problem**: Slow generation speed
**Solution**:
- Reduce target row count
- Lower messiness rates
- Use SSD storage
- Close other applications

#### Invalid Parameters
**Problem**: Rate parameters outside valid range
**Solution**:
- Keep all rates between 0.0 and 1.0
- Sum of all rates should be reasonable (<2.0)

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ValueError: Please provide a sample DataFrame` | No input data | Check input file path |
| `FileNotFoundError` | File doesn't exist | Verify file path and name |
| `MemoryError` | Insufficient RAM | Reduce dataset size |
| `UnicodeDecodeError` | File encoding issue | Convert to UTF-8 encoding |

## 📈 Performance Guidelines

### Dataset Size Recommendations

| Input Size | Output Size | RAM Required | Processing Time |
|------------|-------------|--------------|-----------------|
| < 1MB | < 100K rows | 2GB | < 1 minute |
| 1-10MB | 100K-500K rows | 4GB | 1-5 minutes |
| 10-100MB | 500K-1M rows | 8GB | 5-15 minutes |
| > 100MB | > 1M rows | 16GB+ | 15+ minutes |

### Optimization Tips
- **Use appropriate data types** in your input CSV
- **Remove unnecessary columns** before processing
- **Start with smaller samples** for testing
- **Monitor memory usage** during generation
- **Use SSDs** for faster I/O operations

## 🔬 Use Cases

### Data Engineering
```bash
# Test ETL pipeline with realistic messy data
python python_standalone.py clean_transactions.csv \
    --rows 100000 \
    --output etl_test_data.csv \
    --duplicates 0.20 \
    --nulls 0.15
```

### Machine Learning
```bash
# Generate training data for data cleaning models
python python_standalone.py labeled_dataset.csv \
    --rows 50000 \
    --output ml_training_messy.csv \
    --text-corruption 0.15
```

### Quality Assurance
```bash
# Create stress test data for validation systems
python python_standalone.py production_sample.csv \
    --rows 25000 \
    --output qa_stress_test.csv \
    --wrong-ranges 0.25 \
    --wrong-timestamps 0.20
```

## 🤝 Contributing

### Reporting Issues
1. Check existing issues first
2. Provide input file sample (if possible)
3. Include full error message
4. Specify Python version and OS

### Feature Requests
- Additional messiness types
- New file format support
- Performance improvements
- Additional analysis features

## 📝 License

This project is open source. Please check the license file for details.

## 🆘 Support

For support and questions:
1. Check this README first
2. Review the troubleshooting section
3. Create an issue with detailed information
4. Include sample data and error messages

---

**Happy Data Messing! 🎲**
