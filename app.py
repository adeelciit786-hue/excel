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
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Overview", "🔍 Quality", "📊 Visualize", "💡 Insights", "⚙️ Advanced"]
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
    
    # ==================== TAB 4: INSIGHTS & RECOMMENDATIONS ====================
    with tab4:
        st.subheader("💡 Smart Recommendations")
        
        recommendations = []
        
        # Rule 1: Data Completeness
        completeness = (1 - missing_data.sum() / (len(df) * len(df.columns))) * 100
        if completeness < 95:
            recommendations.append({
                'type': 'warning',
                'title': 'Data Completeness Issue',
                'message': f'Your data completeness is {completeness:.1f}%. Consider handling missing values or removing incomplete records.'
            })
        else:
            recommendations.append({
                'type': 'success',
                'title': 'Excellent Data Completeness',
                'message': f'Your data completeness is {completeness:.1f}% - Great job maintaining data quality!'
            })
        
        # Rule 2: Duplicates
        dup_percent = (df.duplicated().sum() / len(df)) * 100
        if dup_percent > 5:
            recommendations.append({
                'type': 'warning',
                'title': 'High Duplicate Rate',
                'message': f'{dup_percent:.1f}% of your data contains duplicates. Consider removing or investigating these entries.'
            })
        
        # Rule 3: Data Size
        if len(df) < 100:
            recommendations.append({
                'type': 'warning',
                'title': 'Small Dataset',
                'message': f'Your dataset has only {len(df)} rows. For better analysis, consider collecting more data.'
            })
        elif len(df) > 100000:
            recommendations.append({
                'type': 'info',
                'title': 'Large Dataset',
                'message': f'Your dataset has {len(df):,} rows. Consider breaking it into segments for targeted analysis.'
            })
        
        # Rule 4: Column consistency
        if len(numeric_cols) == 0:
            recommendations.append({
                'type': 'warning',
                'title': 'No Numeric Data',
                'message': 'Your dataset contains no numeric columns. Add numerical data for deeper analysis.'
            })
        
        # Rule 5: Outliers in numeric data
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
            if len(outliers) > len(df) * 0.05:
                recommendations.append({
                    'type': 'info',
                    'title': f'Outliers in {col}',
                    'message': f'Found {len(outliers)} potential outliers ({len(outliers)/len(df)*100:.1f}%) in column "{col}". Review these values.'
                })
        
        # Display recommendations
        for rec in recommendations:
            if rec['type'] == 'success':
                st.markdown(f'<div class="success-box">✅ <b>{rec["title"]}</b><br/>{rec["message"]}</div>', unsafe_allow_html=True)
            elif rec['type'] == 'warning':
                st.markdown(f'<div class="warning-box">⚠️ <b>{rec["title"]}</b><br/>{rec["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="recommendation-box">ℹ️ <b>{rec["title"]}</b><br/>{rec["message"]}</div>', unsafe_allow_html=True)
    
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
