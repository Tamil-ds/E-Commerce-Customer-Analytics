import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv(
        r'D:\E-Commerce-Customer-Analytics\data\processed\cleaned_retail.csv'
    )
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

df = load_data()

st.title("📊 E-Commerce Customer Analytics")
st.markdown("**UCI Online Retail Dataset** · 3,97,884 transactions · 2010–2011")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"£{df['TotalPrice'].sum():,.0f}")
col2.metric("Total Orders", f"{df['InvoiceNo'].nunique():,}")
col3.metric("Customers", f"{df['CustomerID'].nunique():,}")
col4.metric(
    "Avg Order Value",
    f"£{df.groupby('InvoiceNo')['TotalPrice'].sum().mean():,.0f}"
)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "Revenue Trends",
    "Top Products",
    "Customer Analysis",
    "Order Patterns"
])

with tab1:
    monthly = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
    monthly.columns = ['Month', 'Revenue']
    fig = px.line(
        monthly, x='Month', y='Revenue',
        title='Monthly Revenue Trend — Nov 2011 shows 40% holiday spike',
        color_discrete_sequence=['#185FA5']
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (£)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

    country = df.groupby('Country')['TotalPrice'].sum().nlargest(10).reset_index()
    country.columns = ['Country', 'Revenue']
    fig2 = px.bar(
        country, x='Revenue', y='Country',
        orientation='h',
        title='UK Dominates with 82% of Total Revenue',
        color_discrete_sequence=['#185FA5']
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    top10 = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
    top10.columns = ['Product', 'Revenue']
    fig3 = px.bar(
        top10.sort_values('Revenue'),
        x='Revenue', y='Product',
        orientation='h',
        title='Top 3 Products Contribute 25% of All Revenue',
        color_discrete_sequence=['#185FA5']
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Product Summary Table")
    prod_table = df.groupby('Description').agg(
        Revenue=('TotalPrice', 'sum'),
        Units_Sold=('Quantity', 'sum'),
        Orders=('InvoiceNo', 'nunique')
    ).sort_values('Revenue', ascending=False).head(20).reset_index()
    prod_table['Revenue'] = prod_table['Revenue'].apply(lambda x: f"£{x:,.0f}")
    st.dataframe(prod_table, use_container_width=True)

with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        cust = df.groupby('CustomerID').agg(
            Orders=('InvoiceNo', 'nunique'),
            Revenue=('TotalPrice', 'sum')
        ).sort_values('Revenue', ascending=False).head(10).reset_index()
        fig4 = px.bar(
            cust, x='CustomerID', y='Revenue',
            title='Top 10 Customers by Revenue',
            color_discrete_sequence=['#185FA5']
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_b:
        country_cust = df.groupby('Country')['CustomerID'].nunique().nlargest(10).reset_index()
        country_cust.columns = ['Country', 'Customers']
        fig5 = px.bar(
            country_cust, x='Customers', y='Country',
            orientation='h',
            title='Customers by Country',
            color_discrete_sequence=['#378ADD']
        )
        st.plotly_chart(fig5, use_container_width=True)

with tab4:
    col_c, col_d = st.columns(2)

    with col_c:
        hourly = df.groupby('Hour')['InvoiceNo'].nunique().reset_index()
        hourly.columns = ['Hour', 'Orders']
        fig6 = px.bar(
            hourly, x='Hour', y='Orders',
            title='Peak Orders: 10am–2pm Every Day',
            color_discrete_sequence=['#185FA5']
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col_d:
        dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        daily = df.groupby('DayOfWeek')['InvoiceNo'].nunique().reset_index()
        daily.columns = ['Day', 'Orders']
        daily['Day'] = pd.Categorical(daily['Day'], categories=dow_order, ordered=True)
        daily = daily.sort_values('Day')
        fig7 = px.bar(
            daily, x='Day', y='Orders',
            title='Thursday Busiest — Weekend Drops 85%',
            color_discrete_sequence=['#185FA5']
        )
        st.plotly_chart(fig7, use_container_width=True)

st.divider()
st.markdown(
    "Built by **Tamil** | "
    "[GitHub](https://github.com/Tamil-ds/E-Commerce-Customer-Analytics) | "
    "Data: UCI Online Retail Dataset"
)