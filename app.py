import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Dashboard", layout="wide")

# ----------------------------
#  Glass UI Styling
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.glass {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title(" Retail Sales Intelligence Dashboard")

# ----------------------------
# 📥 Load Data
# ----------------------------
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

# ----------------------------
#  Tabs
# ----------------------------
tab1, tab2 = st.tabs([" Dashboard", " Report"])

# ============================
#  DASHBOARD TAB
# ============================
with tab1:

    # Sidebar Filters
    st.sidebar.header(" Filters")

    country = st.sidebar.multiselect(
        "Country", df['Country'].unique(), default=df['Country'].unique()
    )

    month = st.sidebar.multiselect(
        "Month", df['Month'].unique(), default=df['Month'].unique()
    )

    start_date = st.sidebar.date_input("Start Date", df['InvoiceDate'].min())
    end_date = st.sidebar.date_input("End Date", df['InvoiceDate'].max())

    # Apply filters
    filtered_df = df[
        (df['Country'].isin(country)) &
        (df['Month'].isin(month)) &
        (df['InvoiceDate'] >= pd.to_datetime(start_date)) &
        (df['InvoiceDate'] <= pd.to_datetime(end_date))
    ]

    # 🔎 Search
    search = st.text_input("🔎 Search Product")

    if search:
        filtered_df = filtered_df[
            filtered_df['Description'].str.contains(search, case=False, na=False)
        ]

    # KPIs
    col1, col2, col3 = st.columns(3)

    col1.metric(" Total Sales", f"{filtered_df['TotalSales'].sum():,.0f}")
    col2.metric(" Orders", filtered_df['InvoiceNo'].nunique())
    col3.metric(" Countries", filtered_df['Country'].nunique())

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("Top Products")

        top_products = (
            filtered_df.groupby('Description')['TotalSales']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig1 = px.bar(
            top_products,
            x='TotalSales',
            y='Description',
            orientation='h',
            hover_data=['TotalSales']
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader("🌍 Sales by Country")

        country_sales = (
            filtered_df.groupby('Country')['TotalSales']
            .sum()
            .reset_index()
        )

        fig2 = px.pie(country_sales, names='Country', values='TotalSales')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Monthly Trend
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader(" Monthly Sales Trend")

    monthly_sales = (
        filtered_df.groupby('Month')['TotalSales']
        .sum()
        .reset_index()
    )

    fig3 = px.line(monthly_sales, x='Month', y='TotalSales', markers=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Insights
    st.markdown("---")
    st.subheader(" Live Insight")

    if not filtered_df.empty:
        best_country = filtered_df.groupby('Country')['TotalSales'].sum().idxmax()
        top_product = filtered_df.groupby('Description')['TotalSales'].sum().idxmax()

        st.success(f" Top Country: {best_country}")
        st.info(f" Most Sold Product: {top_product}")
    else:
        st.warning("No data available for selected filters")

    # Product Drilldown
    st.markdown("---")
    st.subheader("Explore Product")

    if not filtered_df.empty:
        product = st.selectbox("Select Product", filtered_df['Description'].unique())
        product_df = filtered_df[filtered_df['Description'] == product]
        st.dataframe(product_df.head())

    # Download
    st.download_button(
        label="📥 Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )


with tab2:

    st.title(" Project Report")

    st.subheader("Abstract")
    st.write("""
    This project analyzes retail sales data to extract meaningful insights
    using Python, SQL, and Excel. An interactive dashboard is built using
    Streamlit for real-time data visualization and decision-making.
    """)

    st.subheader("Introduction")
    st.write("""
    Retail businesses generate large volumes of data. Analyzing this data
    helps identify trends, improve inventory management, and enhance
    decision-making processes.
    """)

    st.subheader("Objectives")
    st.write("""
    - Analyze retail sales data  
    - Perform data cleaning and preprocessing  
    - Generate insights using SQL and Excel  
    - Build an interactive dashboard  
    """)

    st.subheader("Results & Findings")

    total_sales = df['TotalSales'].sum()
    top_product = df.groupby('Description')['TotalSales'].sum().idxmax()
    top_country = df.groupby('Country')['TotalSales'].sum().idxmax()

    st.write(f" Total Sales: {total_sales:,.0f}")
    st.write(f" Top Product: {top_product}")
    st.write(f" Top Country: {top_country}")

    st.subheader("Conclusion")
    st.write("""
    The project successfully demonstrates how data analysis tools can be used
    to extract insights from retail data and support business decisions.
    """)