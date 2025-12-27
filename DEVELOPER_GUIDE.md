# 👨‍💻 Developer Guide - Excel Analyzer Pro

## Project Overview

Excel Analyzer Pro is a Streamlit-based data analysis application that enables users to upload Excel/CSV files and receive intelligent, data-driven recommendations.

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Analytics**: Scikit-learn, SciPy
- **File Handling**: OpenPyXL (Excel), built-in CSV

## Project Structure

```
Excel Analyzer/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # User documentation
├── QUICKSTART.md         # Quick start guide
├── FEATURES.md           # Detailed features documentation
├── .gitignore            # Git ignore rules
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── create_sample.py      # Sample data generator
├── sample_data.xlsx      # Sample test file
└── venv/                 # Virtual environment (auto-created)
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment support

### Setup Steps

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run app.py
```

## Code Structure

### Main Application (app.py)

#### 1. **Configuration Section**
```python
st.set_page_config(...)  # Page settings
st.markdown(...)         # Custom CSS styling
```

#### 2. **Session State Management**
```python
if 'df' not in st.session_state:
    st.session_state.df = None
```
Maintains dataframe across app reruns.

#### 3. **File Upload Sidebar**
- File uploader widget
- Support for .xlsx, .xls, .csv
- Error handling and success messages

#### 4. **Tab-based Interface**
- **Tab 1 (📋 Overview)**: Basic statistics and preview
- **Tab 2 (🔍 Quality)**: Data quality analysis
- **Tab 3 (📊 Visualize)**: Interactive charts
- **Tab 4 (💡 Insights)**: Recommendations
- **Tab 5 (⚙️ Advanced)**: Statistical analysis

## Key Functions & Logic

### Data Loading
```python
if uploaded_file.name.endswith('.csv'):
    st.session_state.df = pd.read_csv(uploaded_file)
else:
    st.session_state.df = pd.read_excel(uploaded_file)
```

### Metrics Calculation
- Row/column counts
- Data type analysis
- Missing value analysis
- Duplicate detection

### Recommendation Engine
Rules-based system that checks:
1. Data completeness (target: > 95%)
2. Duplicate percentage (warning if > 5%)
3. Dataset size (too small/large warning)
4. Data type presence (check for numeric data)
5. Outlier percentage (flag if > 5%)

### Visualization Methods
- **Plotly Express**: Interactive bar charts, histograms
- **Plotly Graph Objects**: Heatmaps
- **Streamlit**: Native dataframe display

## Dependencies & Purpose

```
streamlit          # Web application framework
pandas             # Data manipulation & analysis
numpy              # Numerical computing
plotly             # Interactive visualizations
matplotlib         # Static charts
seaborn            # Statistical graphics
scikit-learn       # Machine learning utilities
openpyxl           # Excel file reading/writing
```

## Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

### Performance Optimization
- Cache heavy computations: `@st.cache_data`
- Use vectorized operations with pandas/numpy
- Avoid unnecessary dataframe copies
- Optimize visualizations for large datasets

### Error Handling
```python
try:
    st.session_state.df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"❌ Error loading file: {str(e)}")
```

## Adding New Features

### Example: Adding a New Tab

```python
# In the tabs definition
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview", "🔍 Quality", "📊 Visualize", 
    "💡 Insights", "⚙️ Advanced", "🆕 New Tab"
])

# Add content in with block
with tab6:
    st.subheader("New Analysis Feature")
    # Your code here
```

### Example: Adding a New Recommendation Rule

```python
# In the Insights tab, add to recommendations list
if some_condition:
    recommendations.append({
        'type': 'warning',  # or 'success', 'info'
        'title': 'Issue Title',
        'message': 'Detailed explanation'
    })
```

### Example: Adding a New Visualization

```python
# Use Plotly for interactive charts
fig = px.histogram(df, x=column, nbins=30, title="Title")
st.plotly_chart(fig, use_container_width=True)

# Or use native Streamlit
st.bar_chart(df.groupby('Category').size())
```

## Testing

### Manual Testing Checklist

1. **File Upload**
   - [ ] .xlsx files load correctly
   - [ ] .xls files load correctly
   - [ ] .csv files load correctly
   - [ ] Large files (100K+ rows) don't crash
   - [ ] Corrupted files show error message

2. **Data Display**
   - [ ] All tabs load without errors
   - [ ] Charts render correctly
   - [ ] Numbers are formatted properly
   - [ ] Text doesn't overflow

3. **Recommendations**
   - [ ] Rules trigger correctly
   - [ ] Messages are clear
   - [ ] Color coding is consistent

4. **Export**
   - [ ] CSV downloads with correct data
   - [ ] Excel downloads with correct data
   - [ ] Filenames are valid

### Creating Test Files

```python
# Run create_sample.py to generate test data
python create_sample.py
```

## Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment Options

#### 1. **Streamlit Cloud** (Recommended)
```bash
# Push to GitHub, connect Streamlit Cloud
# Auto-deploys on each push
```

#### 2. **Heroku**
```bash
# Requires Procfile and setup.sh
heroku create your-app-name
git push heroku main
```

#### 3. **Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## Troubleshooting

### Common Issues

#### App crashes on large files
**Solution**: Implement data chunking or sampling
```python
if len(df) > 100000:
    df = df.sample(n=100000, random_state=42)
```

#### Slow visualizations
**Solution**: Use Plotly's aggregation or reduce data
```python
fig = px.histogram(df.sample(10000), x=col)
```

#### Memory issues
**Solution**: Clear cache or optimize dtypes
```python
@st.cache_data(ttl=3600)
def load_data(file):
    # Load and process data
    pass
```

## Future Enhancement Ideas

### Short-term (v1.1)
- [ ] Data export to SQL database
- [ ] Custom chart builder
- [ ] Filtering/sorting interface
- [ ] Column statistics sidebar

### Medium-term (v2.0)
- [ ] Predictive analytics (forecasting)
- [ ] Machine learning model training
- [ ] Data transformation pipeline
- [ ] Scheduled analysis reports
- [ ] Multi-file comparison

### Long-term (v3.0)
- [ ] Real-time data streaming
- [ ] Cloud data source integration
- [ ] Advanced ML models (clustering, classification)
- [ ] API for programmatic access
- [ ] Team collaboration features

## Dependencies Management

### Updating Packages
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade pandas

# Freeze current versions
pip freeze > requirements.txt
```

### Version Compatibility

| Package | Min Version | Latest | Status |
|---------|------------|--------|--------|
| Streamlit | 1.0 | 1.28+ | ✅ Latest |
| Pandas | 1.3 | 2.1+ | ✅ Latest |
| NumPy | 1.21 | 2.0+ | ✅ Latest |
| Plotly | 5.0 | 6.0+ | ✅ Latest |

## Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Session State
```python
with st.sidebar:
    st.write("### Debug Info")
    st.write(f"Session state: {st.session_state}")
```

### Profile Performance
```python
import time

start = time.time()
# Code to profile
end = time.time()
print(f"Took {end-start:.2f} seconds")
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add: description of changes"

# Push to remote
git push origin feature/new-feature

# Create pull request
# Review and merge
```

## Documentation Guidelines

- Update README.md for user-facing changes
- Update FEATURES.md for feature additions
- Add docstrings to new functions
- Include usage examples in comments
- Keep documentation in sync with code

## Performance Benchmarks

Target performance metrics:

| Operation | Target | Status |
|-----------|--------|--------|
| File load (10K rows) | < 1s | ✅ |
| Analysis (10K rows) | < 2s | ✅ |
| Visualization (10K rows) | < 1s | ✅ |
| Export to CSV | < 2s | ✅ |
| Export to Excel | < 3s | ✅ |

## Support & Maintenance

### Regular Maintenance
- [ ] Update dependencies monthly
- [ ] Review and fix bugs
- [ ] Optimize slow features
- [ ] Clean up obsolete code

### User Support
- Maintain FAQ document
- Track user issues
- Provide timely updates
- Gather feature requests

---

## Quick Reference

### Useful Streamlit Components
```python
st.write()              # Display text/objects
st.metric()             # Display KPI
st.dataframe()          # Display table
st.bar_chart()          # Native bar chart
st.line_chart()         # Native line chart
st.plotly_chart()       # Plotly chart
st.selectbox()          # Dropdown
st.multiselect()        # Multi-select
st.file_uploader()      # File upload
st.columns()            # Layout columns
st.tabs()               # Tab interface
st.divider()            # Horizontal line
st.markdown()           # Markdown text
st.error()              # Error message
st.success()            # Success message
st.warning()            # Warning message
st.info()               # Info message
```

### Pandas Quick Reference
```python
df.head()               # First 5 rows
df.describe()           # Statistics
df.dtypes               # Data types
df.isnull().sum()       # Missing values
df.duplicated().sum()   # Duplicates
df.corr()               # Correlation matrix
df.select_dtypes()      # Filter by type
df.groupby()            # Group data
df.loc[], df.iloc[]     # Indexing
```

---

**Last Updated**: December 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team
