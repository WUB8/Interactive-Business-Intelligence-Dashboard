# 🛍️ Interactive Business Intelligence Dashboard

## Retail Analytics Platform

A professional Business Intelligence dashboard built with Python and Gradio, utilizing the **Strategy Design Pattern** for scalable data analysis. This application allows users to upload retail data, perform automated profiling, filter records, visualize trends, and extract actionable insights.

## 📋 Project Overview

- **Domain:** E-commerce / Retail
- **Architecture:** Modular design using the Strategy Pattern
- **Key Capabilities:** Data Profiling, Interactive Filtering, Advanced Visualization, Automated Insights
- **Course:** CS5130 - Final Project

## ✨ Key Features

### 1. Data Management (Foundation)

- ✅ **Upload & Validation:** Supports CSV and Excel files with automatic type detection.
- ✅ **Data Preview:** Interactive pagination for raw data viewing.
- ✅ **Export:** Download filtered datasets as CSV.

### 2. Data Profiling (Strategy Pattern)

The application dynamically selects algorithms to analyze data structure:

- ✅ **Basic Statistics:** Row/column counts, memory usage, data type breakdown.
- ✅ **Missing Values:** Identification and quantification of null values.
- ✅ **Numeric Summary:** Statistical distribution (Mean, Median, Skewness, Kurtosis).
- ✅ **Categorical Summary:** Value counts and frequency analysis.
- ✅ **Data Quality:** Completeness scores, duplicate detection, and outlier scanning.

### 3. Interactive Filtering

- ✅ **Dynamic Controls:** Filter data based on column values.
- ✅ **Operations:** Support for `Equals`, `Greater Than`, `Less Than`, and `Contains`.
- ✅ **Real-time Updates:** Statistics and visuals update instantly when filters are applied.

### 4. Visualizations

Four distinct visualization strategies implemented using Plotly:

- ✅ **Time Series Analysis:** Tracks trends over time (e.g., Revenue per day).
- ✅ **Distribution Plot:** Analyzes numeric spreads (Box plots/Histograms).
- ✅ **Category Analysis:** Bar charts with aggregation controls (Sum, Mean, Median).
- ✅ **Correlation Heatmap:** Identifies relationships between numerical variables.

### 5. Automated Insights

- ✅ **Top Performers:** Automatically identifies top categories or items by value.
- ✅ **Anomaly Detection:** Uses IQR (Interquartile Range) method to detect statistical outliers.

## 🏗️ Project Structure

```text
retail-bi-dashboard/
│
├── app.py                          # Main Gradio application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── QUICKSTART.md                   # Quick start guide
│
├── data/                           # Data directory
│   ├── online_retail.csv           # Sample dataset (5,000 records)
│   └── generate_sample_data.py     # Script to generate fresh sample data
│
└── src/                            # Source code package
    ├── strategies/                 # Strategy Pattern Implementations
    │   ├── base_strategy.py        # Abstract Base Classes (Interfaces)
    │   ├── profiling_strategies.py # Profiling logic (Stats, Quality, etc.)
    │   ├── visualization_strategies.py # Plotting logic (Time series, Corr, etc.)
    │   └── insight_strategies.py   # Analysis logic (Anomalies, Rankings)
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

- [x] Complete data profiling and statistics
- [x] Create filtering interface
- [x] Begin visualization implementations

### Week 3: Visualizations & Features

- [x] Complete all 4 visualization types
- [x] Add insights generation
- [x] Add export functionality
- [x] Polish user interface

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

## 📚 Resources

- [Gradio Documentation](https://www.gradio.app/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Strategy Pattern Explained](https://refactoring.guru/design-patterns/strategy)
- [UCI Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail)

## 📄 License

This project is created for educational purposes as part of a course assignment.

---

**Developer:** Bijun Wu  
**Course:** Interactive Business Intelligence Dashboard  
**Date:** November 2025  
**Version:** 3.0
