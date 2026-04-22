import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Dashboard", layout="wide")

# Glass UI
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

st.title("✨ Retail Sales Dashboard")

# Load Data
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

# Sidebar
st.sidebar.header("🔍 Filters")
country = st.sidebar.multiselect("Country", df['Country'].unique(), default=df['Country'].unique())
month = st.sidebar.multiselect("Month", df['Month'].unique(), default=df['Month'].unique())

filtered_df = df[(df['Country'].isin(country)) & (df['Month'].isin(month))]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"{filtered_df['TotalSales'].sum():,.0f}")
col2.metric("📦 Orders", filtered_df['InvoiceNo'].nunique())
col3.metric("🌍 Countries", filtered_df['Country'].nunique())

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Products")
    top_products = filtered_df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10)
    fig1 = px.bar(top_products, orientation='h')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌍 Sales by Country")
    country_sales = filtered_df.groupby('Country')['TotalSales'].sum().reset_index()
    fig2 = px.pie(country_sales, names='Country', values='TotalSales')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Monthly Trend
st.subheader("📈 Monthly Sales Trend")
monthly_sales = filtered_df.groupby('Month')['TotalSales'].sum().reset_index()
fig3 = px.line(monthly_sales, x='Month', y='TotalSales', markers=True)
st.plotly_chart(fig3, use_container_width=True)

# Insight
st.markdown("---")
st.subheader("🧠 Insight")

best_country = filtered_df.groupby('Country')['TotalSales'].sum().idxmax()
st.success(f"🚀 Top performing country: {best_country}")

# Data View
with st.expander("📂 View Data"):
    st.dataframe(filtered_df)