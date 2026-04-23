import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(layout="wide")

st.title("Retail Sales Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("online_retail.csv", encoding='ISO-8859-1')
    df = df.dropna().drop_duplicates()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']
    df['Month'] = df['InvoiceDate'].dt.month
    return df

df = load_data()

# Tabs
tab1, tab2, tab3 = st.tabs([" Dashboard", "Report", "Resources"])

# ================= DASHBOARD =================
with tab1:

    st.sidebar.header("Filters")

    country = st.sidebar.multiselect("Country", df['Country'].unique(), df['Country'].unique())
    month = st.sidebar.multiselect("Month", df['Month'].unique(), df['Month'].unique())

    filtered_df = df[(df['Country'].isin(country)) & (df['Month'].isin(month))]

    total_sales = filtered_df['TotalSales'].sum()

    st.metric("Total Sales", f"{total_sales:,.0f}")

    # Charts
    top_products = filtered_df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10)

    st.subheader("Top Products")
    st.bar_chart(top_products)

    st.subheader("Sales by Country")
    st.bar_chart(filtered_df.groupby('Country')['TotalSales'].sum())

    # =========================
# 🗄️ SQL Analysis Panel
# =========================
st.markdown("---")
st.subheader("🗄️ SQL Analysis Panel")

query_option = st.selectbox(
    "Choose Analysis",
    [
        "Total Sales",
        "Sales by Country",
        "Top Products",
        "Monthly Sales"
    ]
)

if query_option == "Total Sales":
    query = "SELECT SUM(Quantity * UnitPrice) AS TotalSales FROM sales;"
    result = filtered_df['TotalSales'].sum()

    st.code(query, language="sql")
    st.success(f" Result: {result:,.0f}")

elif query_option == "Sales by Country":
    query = """
    SELECT Country, SUM(Quantity * UnitPrice) AS TotalSales
    FROM sales
    GROUP BY Country
    ORDER BY TotalSales DESC;
    """
    result = filtered_df.groupby('Country')['TotalSales'].sum().reset_index()

    st.code(query, language="sql")
    st.dataframe(result)

elif query_option == "Top Products":
    query = """
    SELECT Description, SUM(Quantity * UnitPrice) AS TotalSales
    FROM sales
    GROUP BY Description
    ORDER BY TotalSales DESC
    LIMIT 10;
    """
    result = (
        filtered_df.groupby('Description')['TotalSales']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.code(query, language="sql")
    st.dataframe(result)

elif query_option == "Monthly Sales":
    query = """
    SELECT strftime('%m', InvoiceDate) AS Month,
           SUM(Quantity * UnitPrice) AS TotalSales
    FROM sales
    GROUP BY Month;
    """
    result = (
        filtered_df.groupby('Month')['TotalSales']
        .sum()
        .reset_index()
    )

    st.code(query, language="sql")
    st.dataframe(result)

# ================= REPORT =================
with tab2:

    st.title("📄 Project Report")

    # ABSTRACT
    st.subheader("Abstract")
    st.write("""
    This project focuses on analyzing retail sales data using Python, SQL, and Excel.
    The objective is to extract meaningful insights that support business decision-making.
    An interactive dashboard is developed using Streamlit for real-time data visualization.
    """)

    # INTRODUCTION
    st.subheader("Introduction")
    st.write("""
    Retail businesses generate large volumes of transactional data. Analyzing this data
    helps identify trends, understand customer behavior, and improve business strategies.
    This project demonstrates how data analytics tools can transform raw data into insights.
    """)

    # OBJECTIVES
    st.subheader("Objectives")
    st.write("""
    - Analyze retail sales data
    - Perform data cleaning and preprocessing
    - Generate insights using SQL and Excel
    - Develop an interactive dashboard
    """)

    # TOOLS
    st.subheader("Tools & Technologies")
    st.write("""
    - Python (Pandas, Plotly, Streamlit)
    - SQL (SQLite)
    - Excel
    """)

    # DATA DESCRIPTION
    st.subheader("Dataset Description")
    st.write("""
    The dataset contains retail transaction records including product details,
    quantity, price, and country. It is used to analyze sales patterns and trends.
    """)

    # DATA CLEANING
    st.subheader("Data Cleaning")
    st.write("""
    - Removed missing values
    - Removed duplicate entries
    - Filtered invalid data (negative values)
    """)

    # RESULTS
    st.subheader("Results & Findings")

    if not filtered_df.empty:
        total_sales = filtered_df['TotalSales'].sum()
        top_product = filtered_df.groupby('Description')['TotalSales'].sum().idxmax()
        top_country = filtered_df.groupby('Country')['TotalSales'].sum().idxmax()

        st.write(f" Total Sales: {total_sales:,.0f}")
        st.write(f" Top Product: {top_product}")
        st.write(f"Top Country: {top_country}")

        st.info("These results dynamically update based on selected filters.")

    # CONCLUSION
    st.subheader("Conclusion")
    st.write("""
    The project successfully demonstrates how retail data can be analyzed using
    modern tools. The insights generated help improve decision-making and business performance.
    """)

# ================= RESOURCES =================
with tab3:

    st.subheader("Excel Dashboard")

    
    try:
        excel_df = pd.read_excel("automated_dashboard.xlsx", sheet_name="Dashboard")
        st.dataframe(excel_df)
    except:
        st.warning(" Run analysis.py to generate updated Excel")
    

    try:
        with open("automated_dashboard.xlsx", "rb") as f:
            st.download_button("Download Excel", f, "dashboard.xlsx")
    except:
        pass

    st.subheader("PPT")

    try:
        with open("presentation.pptx", "rb") as f:
            st.download_button("Download PPT", f, "presentation.pptx")
    except:
        st.warning("Upload PPT file")