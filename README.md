# 📊 Excel Analyzer Pro

A powerful, user-friendly web application for analyzing Excel spreadsheets and providing intelligent data-driven recommendations.

## Features

✨ **Key Capabilities:**
- 📁 **File Upload** - Support for Excel (.xlsx, .xls) and CSV files
- 📋 **Data Overview** - Quick statistics, summaries, and column information
- 🔍 **Data Quality Analysis** - Identify missing values, duplicates, and data completeness
- 📊 **Interactive Visualizations** - Distribution charts, category counts, correlation heatmaps
- 💡 **Smart Recommendations** - AI-powered insights based on your data
- 🎯 **Advanced Analysis** - Outlier detection, statistical tests, and detailed metrics
- 📥 **Export Options** - Download analysis results as CSV or Excel files

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Setup

1. **Activate Virtual Environment** (if not already activated):
```bash
cd "c:\Users\adeel\Excel Analyzer"
.\venv\Scripts\Activate.ps1
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

Run the application with Streamlit:

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## How to Use

1. **Upload File**: Click the "Upload your Excel file" button in the sidebar
2. **Explore Data**: 
   - **Overview Tab** - See basic statistics and data preview
   - **Quality Tab** - Check for data issues
   - **Visualize Tab** - Generate charts and correlations
   - **Insights Tab** - Get smart recommendations
   - **Advanced Tab** - Perform statistical analysis

3. **Get Recommendations**: View actionable insights based on your data patterns

4. **Export Results**: Download your analysis as CSV or Excel

## Project Structure

```
Excel Analyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── venv/                  # Virtual environment (created during setup)
└── README.md             # This file
```

## Technologies Used

- **Streamlit** - Web app framework for data applications
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations
- **Matplotlib & Seaborn** - Statistical graphics
- **Scikit-learn** - Machine learning utilities
- **OpenPyXL** - Excel file handling

## Features in Detail

### 📋 Overview Tab
- Total rows and columns count
- Numeric and text column counts
- Data type breakdown
- Descriptive statistics
- Column information summary

### 🔍 Quality Tab
- Missing values analysis
- Duplicate detection
- Data completeness score
- Visual representation of data quality issues

### 📊 Visualize Tab
- Distribution histograms
- Category value counts
- Correlation heatmaps
- Interactive Plotly charts

### 💡 Insights Tab
Intelligent recommendations for:
- Data completeness improvements
- Duplicate handling suggestions
- Dataset size recommendations
- Data quality observations
- Outlier notifications

### ⚙️ Advanced Tab
- Outlier detection using IQR method
- Statistical summaries (Mean, Median, Std Dev, Skewness, Kurtosis)
- Box plots for distribution analysis
- Export functionality

## Supported File Formats

- ✅ Excel 2007+ (.xlsx)
- ✅ Excel 97-2003 (.xls)
- ✅ Comma-Separated Values (.csv)

## Data Limits

The application works efficiently with datasets up to:
- **500K+ rows** - Full analysis capability
- **Unlimited columns** - Handled dynamically

For very large files (>1M rows), consider preprocessing or splitting data into segments.

## Sample Usage

### Example: Sales Data Analysis
1. Upload your sales Excel file
2. Review the overview for basic statistics
3. Check the Quality tab for missing prices or incomplete records
4. Visualize sales distribution and category breakdown
5. Get recommendations for data cleaning
6. Export the cleaned analysis

## Troubleshooting

### App won't start?
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### File upload fails?
- Ensure file format is supported (.xlsx, .xls, .csv)
- Check file is not corrupted
- Try converting to CSV if Excel file has issues

### Slow performance?
- Large datasets may take time to process
- Consider splitting data or filtering before analysis

## Future Enhancements

- 🔮 Predictive analytics
- 📧 Email reports
- 🔒 Data encryption
- ☁️ Cloud storage integration
- 🤖 Advanced ML recommendations
- 📱 Mobile-responsive design

## License

This project is created for educational and professional use.

## Support

For issues or suggestions, please check the data file format and ensure all dependencies are properly installed.

---

**Created:** December 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
