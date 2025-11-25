# 🛍️ Interactive Business Intelligence Dashboard
## Retail Analytics Platform

A sophisticated Business Intelligence dashboard built with Gradio, focusing on retail/e-commerce data analysis. This project implements professional software design patterns and provides comprehensive data profiling and visualization capabilities.

## 📋 Project Overview

**Domain:** E-commerce / Retail  
**Key Metrics:** Revenue trends, product performance, sales by category  
**Design Pattern:** Strategy Pattern for flexible data processing

## ✨ Features (Week 1 - Foundation)

### Data Management
- ✅ Upload CSV and Excel files
- ✅ Automatic data type detection
- ✅ Preview data with pagination
- ✅ Sample retail dataset included

### Data Profiling (Strategy Pattern Implementation)
- ✅ **Basic Statistics Strategy**: Row/column counts, memory usage, data types
- ✅ **Missing Values Strategy**: Identify and quantify missing data
- ✅ **Numeric Summary Strategy**: Detailed statistics (mean, median, mode, skewness, kurtosis)
- ✅ **Categorical Summary Strategy**: Value counts and distribution analysis
- ✅ **Data Quality Strategy**: Completeness, duplicates, outliers detection

## 🏗️ Project Structure

```
retail-bi-dashboard/
│
├── app.py                          # Main Gradio application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── data/                           # Data directory
│   ├── online_retail.csv          # Sample dataset (5000 records)
│   └── generate_sample_data.py    # Data generation script
│
├── src/                            # Source code
│   ├── __init__.py
│   │
│   ├── strategies/                 # Strategy Pattern implementations
│   │   ├── __init__.py
│   │   ├── base_strategy.py       # Abstract base classes
│   │   └── profiling_strategies.py # Concrete profiling strategies
│   │
│   └── utils/                      # Utility functions
│       └── __init__.py
│
└── notebooks/                      # Jupyter notebooks for exploration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd retail-bi-dashboard
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Access the dashboard:**
Open your browser and go to `http://localhost:7860`

## 📊 Sample Dataset

The project includes a sample retail dataset with:
- **5,000 transactions** from 2023
- **9 columns**: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country, Category
- **5 product categories**: Electronics, Home & Garden, Clothing, Books, Toys
- **Realistic data** including:
  - Multiple countries (primarily UK)
  - Price variations by category
  - Some cancelled orders (negative quantities)
  - Missing customer IDs (~3% missing data)

## 🎯 Strategy Pattern Implementation

This project demonstrates the **Strategy Pattern**, a behavioral design pattern that:

### Benefits
- **Flexibility**: Easy to add new profiling strategies without modifying existing code
- **Maintainability**: Each strategy is isolated and testable
- **Extensibility**: New analysis methods can be added by implementing the base interface

### Architecture

```python
# Base Strategy (Abstract Interface)
DataProcessingStrategy
  └── process(data) → Result
  └── get_description() → str

# Concrete Strategies
BasicStatisticsStrategy
MissingValuesStrategy
NumericSummaryStrategy
CategoricalSummaryStrategy
DataQualityStrategy
```

### Example Usage
```python
from strategies.profiling_strategies import BasicStatisticsStrategy

# Use a specific strategy
strategy = BasicStatisticsStrategy()
results = strategy.process(dataframe)
print(strategy.get_description())
```

## 🔧 Usage Guide

1. **Upload Data:**
   - Click "Upload Dataset" button
   - Select CSV or Excel file
   - Click "Load and Analyze Data"

2. **Explore Profiling Results:**
   - **Data Preview**: View first 20 rows
   - **Basic Statistics**: Overview of dataset structure
   - **Missing Values**: Identify data completeness issues
   - **Numeric Summary**: Statistical analysis of numeric columns
   - **Categorical Summary**: Distribution of categorical values
   - **Data Quality**: Overall quality assessment
   - **Column Details**: Comprehensive column information

## 📈 Development Timeline

### Week 1: Foundation ✅ (Current)
- [x] Set up project structure
- [x] Choose domain and dataset
- [x] Implement data upload and preview
- [x] Start data profiling features
- [x] Implement Strategy Pattern

### Week 2: Core Features (Next)
- [ ] Complete data profiling and statistics
- [ ] Create filtering interface
- [ ] Begin visualization implementations

### Week 3: Visualizations & Features
- [ ] Complete all 4 visualization types
- [ ] Add insights generation
- [ ] Add export functionality
- [ ] Polish user interface

### Week 4: Documentation & Submission
- [ ] Test thoroughly with multiple datasets
- [ ] Write technical report
- [ ] Record demo video
- [ ] Final code cleanup and documentation

## 🛠️ Technical Stack

- **Frontend/UI**: Gradio 4.0+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn (Week 2+)
- **Design Pattern**: Strategy Pattern
- **Language**: Python 3.8+

## 📝 Key Metrics for Retail Analysis

The dashboard is designed to analyze:
- **Revenue Trends**: Sales over time, seasonal patterns
- **Product Performance**: Top sellers, category distribution
- **Customer Behavior**: Purchase patterns, geographic distribution
- **Operational Metrics**: Order volumes, average order values

## 🎓 Learning Objectives

This project demonstrates:
1. **Software Design Patterns**: Strategy Pattern implementation
2. **Data Engineering**: ETL processes, data quality assessment
3. **Business Intelligence**: KPI tracking, data profiling
4. **UI/UX Design**: Interactive dashboard development
5. **Clean Code Practices**: Modular, maintainable architecture

## 🤝 AI Tool Usage

This project was developed with assistance from AI tools (Claude) for:
- ✅ Brainstorming dashboard structure
- ✅ Generating boilerplate code for Strategy Pattern
- ✅ Debugging data processing issues
- ✅ Creating sample dataset generator
- ✅ Writing comprehensive documentation

All code has been reviewed, understood, validated, and customized for this specific use case.

## 📚 Resources

- [Gradio Documentation](https://www.gradio.app/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Strategy Pattern Explained](https://refactoring.guru/design-patterns/strategy)
- [UCI Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail)

## 📄 License

This project is created for educational purposes as part of a course assignment.

---

**Developer:** [Your Name]  
**Course:** Interactive Business Intelligence Dashboard  
**Date:** November 2025  
**Version:** 1.0 (Week 1 Foundation)
