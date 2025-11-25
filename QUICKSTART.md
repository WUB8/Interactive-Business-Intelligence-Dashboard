# 🚀 Quick Start Guide

## Running the Dashboard

1. **Navigate to the project directory:**
```bash
cd retail-bi-dashboard
```

2. **Install dependencies** (if not already installed):
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser** and navigate to:
```
http://localhost:7860
```

## Using the Dashboard

### Step 1: Load Data
- Click on "📁 Upload Dataset" 
- Select `data/online_retail.csv` from the project folder
- Click "🚀 Load and Analyze Data"

### Step 2: Explore Tabs
- **Data Preview**: See your data structure
- **Basic Statistics**: Get dataset overview
- **Missing Values**: Check data completeness
- **Numeric Summary**: View statistical summaries
- **Categorical Summary**: Click button to analyze categories
- **Data Quality**: Review overall quality metrics
- **Column Details**: Click button for detailed info

## Testing with Sample Data

The included sample dataset (`data/online_retail.csv`) contains:
- 5,000 retail transactions
- 5 product categories
- 9 data columns
- Realistic e-commerce patterns

## Troubleshooting

### Port Already in Use
If port 7860 is busy, edit `app.py` line 330 and change the port:
```python
app.launch(share=False, server_name="0.0.0.0", server_port=7861)  # Changed to 7861
```

### Import Errors
Make sure you're running from the project root directory where `app.py` is located.

### Module Not Found
Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Week 1 Checklist

- ✅ Project structure created
- ✅ Domain selected (Retail)
- ✅ Sample dataset generated
- ✅ Data upload implemented
- ✅ Data preview working
- ✅ Data profiling features completed:
  - ✅ Basic statistics
  - ✅ Missing values analysis
  - ✅ Numeric summary
  - ✅ Categorical summary
  - ✅ Data quality assessment
- ✅ Strategy Pattern implemented
- ✅ Documentation created

## Next Steps (Week 2)

1. Add filtering capabilities
2. Implement first visualizations
3. Create interactive charts
4. Add date range filters

---
Happy analyzing! 📊
