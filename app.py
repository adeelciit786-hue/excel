import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO, BytesIO
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Excel Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 20px;
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
    .recommendation-box {
        background-color: #e7f3ff;
        border-left: 5px solid #1f77b4;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📊 Excel Analyzer Pro")
st.markdown("### *Intelligent Data Analysis & Recommendations Platform*")
st.divider()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# Function to generate detailed recommendations with reasoning
def generate_recommendations(df):
    """Generate detailed recommendations with reasoning and actionable insights"""
    recommendations = []
    
    # Rule 1: Data Completeness
    missing_data = df.isnull().sum()
    completeness = (1 - missing_data.sum() / (len(df) * len(df.columns))) * 100
    
    if completeness >= 95:
        recommendations.append({
            'priority': 'high',
            'type': 'success',
            'icon': '✅',
            'title': 'Excellent Data Completeness',
            'score': f'{completeness:.1f}%',
            'issue': 'None detected',
            'reasoning': f'Your dataset has {completeness:.1f}% completeness, which is excellent. This means {missing_data.sum()} out of {len(df) * len(df.columns)} total cells are empty.',
            'impact': 'High quality data enables accurate analysis and reliable insights',
            'action': 'Continue with confidence - your data quality is excellent!',
            'benefit': 'More reliable analytics, better decision-making'
        })
    elif completeness >= 80:
        recommendations.append({
            'priority': 'medium',
            'type': 'warning',
            'icon': '⚠️',
            'title': 'Good Data Completeness',
            'score': f'{completeness:.1f}%',
            'issue': f'{missing_data.sum()} missing values detected',
            'reasoning': f'Your dataset has {completeness:.1f}% completeness. {missing_data.sum()} cells are empty, which may affect analysis accuracy.',
            'impact': 'Missing data can skew statistical results and reduce model accuracy',
            'action': 'Consider these strategies: (1) Drop rows with missing values (2) Fill with mean/median (3) Use advanced imputation methods',
            'benefit': 'Improved data quality leads to more accurate insights'
        })
    else:
        recommendations.append({
            'priority': 'critical',
            'type': 'danger',
            'icon': '🚨',
            'title': 'Low Data Completeness',
            'score': f'{completeness:.1f}%',
            'issue': f'{missing_data.sum()} missing values ({100-completeness:.1f}%)',
            'reasoning': f'Your dataset has only {completeness:.1f}% completeness. {missing_data.sum()} cells are empty, which significantly impacts analysis.',
            'impact': 'Low completeness severely affects statistical reliability and model performance',
            'action': '(1) Investigate why data is missing (2) Remove incomplete columns/rows (3) Use imputation if justified (4) Collect missing data if possible',
            'benefit': 'Addressing data completeness is crucial for meaningful analysis'
        })
    
    # Rule 2: Duplicate Detection
    dup_count = df.duplicated().sum()
    dup_percent = (dup_count / len(df)) * 100
    
    if dup_percent == 0:
        recommendations.append({
            'priority': 'high',
            'type': 'success',
            'icon': '✅',
            'title': 'No Duplicate Records Found',
            'score': '0%',
            'issue': 'None detected',
            'reasoning': f'All {len(df)} records in your dataset are unique. No duplicate rows were found.',
            'impact': 'Ensures each observation is counted only once, preventing bias',
            'action': 'No action needed - your data is clean!',
            'benefit': 'Accurate counts and reliable statistical analysis'
        })
    elif dup_percent < 5:
        recommendations.append({
            'priority': 'medium',
            'type': 'warning',
            'icon': '⚠️',
            'title': 'Minor Duplicate Records',
            'score': f'{dup_percent:.1f}%',
            'issue': f'{dup_count} duplicate rows ({dup_percent:.1f}% of data)',
            'reasoning': f'Found {dup_count} duplicate rows, which is {dup_percent:.1f}% of your {len(df)} total records.',
            'impact': 'Small percentage of duplicates may slightly bias analysis results',
            'action': 'Review duplicates: (1) Use df.duplicated() to identify (2) Decide if legitimate or errors (3) Remove if unneeded',
            'benefit': 'Cleaner data improves accuracy of metrics and statistical tests'
        })
    else:
        recommendations.append({
            'priority': 'critical',
            'type': 'danger',
            'icon': '🚨',
            'title': 'High Duplicate Rate',
            'score': f'{dup_percent:.1f}%',
            'issue': f'{dup_count} duplicate rows ({dup_percent:.1f}%)',
            'reasoning': f'Your dataset contains {dup_count} duplicate rows, which is {dup_percent:.1f}% of total records.',
            'impact': 'High duplication severely skews analysis - counts are inflated, statistics are unreliable',
            'action': '(1) Investigate root cause (2) Remove obvious duplicates (3) Keep domain-specific duplicates if valid (4) Prevent future duplicates',
            'benefit': 'Removing duplicates significantly improves data integrity'
        })
    
    # Rule 3: Dataset Size
    if len(df) < 50:
        recommendations.append({
            'priority': 'high',
            'type': 'info',
            'icon': 'ℹ️',
            'title': 'Small Sample Size',
            'score': f'{len(df)} rows',
            'issue': 'Limited statistical power',
            'reasoning': f'Your dataset has only {len(df)} rows, which is quite small for statistical analysis.',
            'impact': 'Small samples have high sampling error and low statistical power',
            'action': '(1) Collect more data if possible (2) Use methods suited for small samples (3) Increase precision of measurements',
            'benefit': 'Larger samples provide more reliable and generalizable results'
        })
    elif len(df) > 100000:
        recommendations.append({
            'priority': 'medium',
            'type': 'info',
            'icon': 'ℹ️',
            'title': 'Large Dataset Detected',
            'score': f'{len(df):,} rows',
            'issue': 'May require optimization',
            'reasoning': f'Your dataset contains {len(df):,} rows, which is quite large.',
            'impact': 'Large datasets need optimized processing and may have different characteristics',
            'action': '(1) Consider sampling for exploratory analysis (2) Use aggregation for visualization (3) Profile data performance',
            'benefit': 'Proper handling of large data enables powerful insights from scale'
        })
    else:
        recommendations.append({
            'priority': 'high',
            'type': 'success',
            'icon': '✅',
            'title': 'Optimal Dataset Size',
            'score': f'{len(df):,} rows',
            'issue': 'None',
            'reasoning': f'Your dataset has {len(df):,} rows, which is ideal for comprehensive analysis.',
            'impact': 'Good balance between statistical power and practical manageability',
            'action': 'Proceed with full analysis - your data size is ideal!',
            'benefit': 'Sufficient data for reliable statistical inference and insights'
        })
    
    # Rule 4: Data Type Diversity
    numeric_cols_list = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols_list = df.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = len(numeric_cols_list)
    categorical_cols = len(categorical_cols_list)
    
    if numeric_cols == 0:
        recommendations.append({
            'priority': 'critical',
            'type': 'warning',
            'icon': '⚠️',
            'title': 'No Numeric Data Found',
            'score': '0 numeric columns',
            'issue': 'Limited quantitative analysis possible',
            'reasoning': f'Your dataset contains only {categorical_cols} text/categorical columns and no numeric columns.',
            'impact': 'Restricts ability to perform statistical analysis, correlation studies, or quantitative modeling',
            'action': '(1) Convert categorical to numeric (2) Add numeric measurements (3) Create calculated fields (4) Use text analysis if appropriate',
            'benefit': 'Adding numeric data enables statistical analysis, trends, and predictions'
        })
    elif numeric_cols > 0 and categorical_cols == 0:
        recommendations.append({
            'priority': 'medium',
            'type': 'info',
            'icon': 'ℹ️',
            'title': 'Purely Numeric Dataset',
            'score': f'{numeric_cols} numeric columns',
            'issue': 'No categorical context',
            'reasoning': f'Your dataset has {numeric_cols} numeric columns but no categorical columns for grouping/segmentation.',
            'impact': 'Good for quantitative analysis but lacks dimensions for segmentation or classification',
            'action': '(1) Add categorical identifiers if available (2) Create categories from numeric ranges (3) Focus on correlation/trends',
            'benefit': 'Numeric data enables powerful statistical and mathematical analysis'
        })
    else:
        recommendations.append({
            'priority': 'high',
            'type': 'success',
            'icon': '✅',
            'title': 'Good Data Type Mix',
            'score': f'{numeric_cols} numeric + {categorical_cols} categorical',
            'issue': 'None',
            'reasoning': f'Your dataset has {numeric_cols} numeric columns and {categorical_cols} categorical columns.',
            'impact': 'Balanced mix enables both quantitative analysis and segmentation',
            'action': 'Excellent mix - use numeric for analytics and categorical for grouping!',
            'benefit': 'Enables comprehensive analysis including aggregation, comparison, and modeling'
        })
    
    # Rule 5: Outliers Detection
    outlier_cols = []
    for col_name in numeric_cols_list:
        try:
            Q1 = df[col_name].quantile(0.25)
            Q3 = df[col_name].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col_name] < Q1 - 1.5*IQR) | (df[col_name] > Q3 + 1.5*IQR)]
            if len(outliers) > len(df) * 0.05:
                outlier_cols.append((col_name, len(outliers)))
        except:
            pass
    
    if outlier_cols:
        recommendations.append({
            'priority': 'medium',
            'type': 'info',
            'icon': 'ℹ️',
            'title': 'Outliers Detected',
            'score': f'{len(outlier_cols)} columns with outliers',
            'issue': f'Found outliers in {len(outlier_cols)} numeric columns',
            'reasoning': f'Detected potential outliers (values > 1.5×IQR) in columns: {", ".join([col[0] for col in outlier_cols[:3]])}',
            'impact': 'Outliers can skew means, inflate standard deviations, and affect models',
            'action': '(1) Visualize with box plots (2) Verify if valid or errors (3) Decide: keep, transform, or remove (4) Document decisions',
            'benefit': 'Proper outlier handling improves statistical reliability and model performance'
        })
    else:
        recommendations.append({
            'priority': 'high',
            'type': 'success',
            'icon': '✅',
            'title': 'No Significant Outliers',
            'score': '0 columns flagged',
            'issue': 'None detected',
            'reasoning': 'No significant outliers detected in your numeric columns using IQR method.',
            'impact': 'Clean data without extreme values enables more reliable statistical analysis',
            'action': 'Continue analysis with confidence - data is well-behaved!',
            'benefit': 'No outlier handling needed - focus on insights'
        })
    
    return sorted(recommendations, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2}.get(x['priority'], 3))

# Sidebar
with st.sidebar:
    st.header("📁 File Upload")
    uploaded_file = st.file_uploader(
        "Upload your Excel file",
        type=['xlsx', 'xls', 'csv'],
        help="Supported formats: Excel (.xlsx, .xls) and CSV"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)
            st.session_state.filename = uploaded_file.name
            st.success("✅ File loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")

# Main content
if st.session_state.df is None:
    st.info("👈 Please upload an Excel or CSV file to get started!")
    st.markdown("""
    ### Features:
    - 📈 **Data Overview** - Quick statistics and summary
    - 🔍 **Data Quality Analysis** - Identify missing values and duplicates
    - 📊 **Visualization** - Interactive charts and graphs
    - 💡 **Smart Recommendations** - Data-driven insights
    - 🎯 **Column Analysis** - Detailed column-by-column breakdown
    """)
else:
    df = st.session_state.df
    
    # Generate recommendations
    recommendations = generate_recommendations(df)
    
    # Display top recommendations on main screen
    st.markdown("## 🎯 **KEY RECOMMENDATIONS**")
    st.markdown("---")
    
    # Show top 2-3 critical/high priority recommendations
    top_recs = [r for r in recommendations if r['priority'] in ['critical', 'high']][:3]
    
    for rec in top_recs:
        color_map = {
            'success': '🟢',
            'warning': '🟡',
            'danger': '🔴',
            'info': '🔵'
        }
        
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"## {rec['icon']}")
            with col2:
                st.markdown(f"### {rec['title']}")
            
            col1, col2 = st.columns([2, 3])
            with col1:
                st.markdown(f"**Priority:** `{rec['priority'].upper()}`")
                st.markdown(f"**Score:** `{rec['score']}`")
            with col2:
                if rec.get('issue'):
                    st.markdown(f"**Issue:** {rec['issue']}")
            
            st.markdown(f"**Reasoning:**\n{rec['reasoning']}")
            st.markdown(f"**Impact:** {rec['impact']}")
            st.markdown(f"**Recommended Action:** {rec['action']}")
            st.markdown(f"**Benefit:** {rec['benefit']}")
            st.divider()
    
    # Create tabs for detailed analysis
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Overview", "🔍 Quality", "📊 Visualize", "💡 All Insights", "⚙️ Advanced"]
    )
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 Total Rows", f"{len(df):,}")
        with col2:
            st.metric("📋 Total Columns", f"{len(df.columns)}")
        with col3:
            st.metric("🔢 Numeric Columns", f"{len(df.select_dtypes(include=[np.number]).columns)}")
        with col4:
            st.metric("🔤 Text Columns", f"{len(df.select_dtypes(include=['object']).columns)}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
        
        with col2:
            st.subheader("📈 Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
        
        st.divider()
        st.subheader("📋 Column Information")
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)
    
    # ==================== TAB 2: DATA QUALITY ====================
    with tab2:
        st.subheader("🔍 Data Quality Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df)) * 100
        
        with col1:
            st.metric("⚠️ Missing Values", missing_data.sum())
        with col2:
            st.metric("👥 Duplicate Rows", df.duplicated().sum())
        with col3:
            st.metric("✅ Data Completeness", f"{(1 - missing_data.sum() / (len(df) * len(df.columns))) * 100:.1f}%")
        
        st.divider()
        
        # Missing values analysis
        if missing_data.sum() > 0:
            st.markdown('<div class="warning-box">⚠️ <b>Missing Values Detected</b></div>', unsafe_allow_html=True)
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing Percentage': missing_percent.values
            }).sort_values('Missing Count', ascending=False)
            missing_df = missing_df[missing_df['Missing Count'] > 0]
            
            fig = px.bar(missing_df, x='Column', y='Missing Percentage', 
                         title='Missing Data Distribution', color='Missing Percentage')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.markdown('<div class="success-box">✅ <b>No Missing Values Found</b></div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Duplicate analysis
        if df.duplicated().sum() > 0:
            st.markdown('<div class="warning-box">⚠️ <b>Duplicate Rows Detected</b></div>', unsafe_allow_html=True)
            st.write(f"Found {df.duplicated().sum()} duplicate rows")
        else:
            st.markdown('<div class="success-box">✅ <b>No Duplicate Rows Found</b></div>', unsafe_allow_html=True)
    
    # ==================== TAB 3: VISUALIZATION ====================
    with tab3:
        st.subheader("📊 Data Visualization")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Distribution Analysis")
            if numeric_cols:
                selected_col = st.selectbox("Select numeric column:", numeric_cols, key="dist_col")
                fig = px.histogram(df, x=selected_col, nbins=30, title=f"Distribution of {selected_col}")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Category Counts")
            if categorical_cols:
                selected_cat = st.selectbox("Select categorical column:", categorical_cols, key="cat_col")
                cat_counts = df[selected_cat].value_counts().head(10)
                fig = px.bar(x=cat_counts.index, y=cat_counts.values, 
                            title=f"Top 10 {selected_cat} Values")
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Correlation heatmap
        if len(numeric_cols) > 1:
            st.markdown("#### Correlation Matrix")
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                           title="Correlation Heatmap", color_continuous_scale="RdBu")
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 4: ALL INSIGHTS & DETAILED RECOMMENDATIONS ====================
    with tab4:
        st.subheader("💡 All Recommendations (Detailed)")
        st.write("Below are all recommendations for your dataset, sorted by priority:")
        st.divider()
        
        # Display all recommendations with detailed reasoning
        for i, rec in enumerate(recommendations, 1):
            priority_color = {
                'critical': '🔴',
                'high': '🟢',
                'medium': '🟡',
            }
            
            with st.container():
                st.markdown(f"### {i}. {priority_color.get(rec['priority'], 'ℹ️')} {rec['title']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Priority", rec['priority'].upper(), delta_color="off")
                with col2:
                    st.metric("Score", rec['score'], delta_color="off")
                with col3:
                    if rec.get('issue'):
                        st.metric("Issue", rec['issue'], delta_color="off")
                
                st.markdown(f"**📝 Reasoning:**")
                st.write(rec['reasoning'])
                
                st.markdown(f"**⚡ Impact:**")
                st.write(rec['impact'])
                
                st.markdown(f"**✅ Recommended Actions:**")
                st.write(rec['action'])
                
                st.markdown(f"**💰 Expected Benefit:**")
                st.write(rec['benefit'])
                
                st.divider()
    
    # ==================== TAB 5: ADVANCED ANALYSIS ====================
    with tab5:
        st.subheader("⚙️ Advanced Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Outlier Detection")
            if numeric_cols:
                col = st.selectbox("Select column for outlier detection:", numeric_cols)
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers_mask = (df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)
                outlier_count = outliers_mask.sum()
                
                fig = px.box(df, y=col, title=f"Box Plot: {col}")
                st.plotly_chart(fig, use_container_width=True)
                st.write(f"**Outliers detected:** {outlier_count} ({outlier_count/len(df)*100:.2f}%)")
        
        with col2:
            st.markdown("#### Statistical Tests")
            if numeric_cols:
                col = st.selectbox("Select column for statistics:", numeric_cols, key="stat_col")
                stats = {
                    'Mean': df[col].mean(),
                    'Median': df[col].median(),
                    'Std Dev': df[col].std(),
                    'Skewness': df[col].skew(),
                    'Kurtosis': df[col].kurtosis()
                }
                stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
                st.dataframe(stats_df, use_container_width=True)
        
        st.divider()
        
        # Export options
        st.markdown("#### 📥 Export Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"analysis_{st.session_state.filename}.csv",
                mime="text/csv"
            )
        
        with col2:
            xlsx_io = BytesIO()
            with pd.ExcelWriter(xlsx_io, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            xlsx_io.seek(0)
            st.download_button(
                label="📥 Download as Excel",
                data=xlsx_io.getvalue(),
                file_name=f"analysis_{st.session_state.filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            st.write("✅ Analysis Complete")

# Footerst.divider()st.divider()
st.markdown("""
---
<div style='text-align: center; color: #888;'>
    <p>Excel Analyzer Pro © 2025 | Powered by Streamlit</p>
    <p>📊 Data Analysis | 💡 Insights | 🎯 Recommendations</p>
</div>
""", unsafe_allow_html=True)
