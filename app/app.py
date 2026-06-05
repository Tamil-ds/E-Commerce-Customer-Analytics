import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce Customer Analytics")
st.markdown("UCI Online Retail Dataset · 2010–2011")
st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("sample_data.csv")
    df['InvoiceDate'] = pd.to_datetime(
        df['InvoiceDate'], errors='coerce'
    )
    return df

try:
    df = load_data()
    st.success(f"Data loaded: {len(df):,} rows")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Total Revenue",
        f"£{df['TotalPrice'].sum():,.0f}"
    )
    col2.metric(
        "Total Orders",
        f"{df['InvoiceNo'].nunique():,}"
    )
    col3.metric(
        "Customers",
        f"{df['CustomerID'].nunique():,}"
    )
    col4.metric(
        "Avg Order Value",
        f"£{df.groupby('InvoiceNo')['TotalPrice'].sum().mean():,.0f}"
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "Revenue", "Products", "Patterns"
    ])

    with tab1:
        monthly = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
        monthly.columns = ['Month', 'Revenue']
        fig = px.line(
            monthly,
            x='Month',
            y='Revenue',
            title='Monthly Revenue Trend',
            color_discrete_sequence=['#185FA5']
        )
        st.plotly_chart(fig, use_container_width=True)

        country = df.groupby('Country')['TotalPrice'].sum().nlargest(10).reset_index()
        country.columns = ['Country', 'Revenue']
        fig2 = px.bar(
            country,
            x='Revenue',
            y='Country',
            orientation='h',
            title='Revenue by Country — Top 10',
            color_discrete_sequence=['#185FA5']
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        top10 = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
        top10.columns = ['Product', 'Revenue']
        fig3 = px.bar(
            top10.sort_values('Revenue'),
            x='Revenue',
            y='Product',
            orientation='h',
            title='Top 10 Products by Revenue',
            color_discrete_sequence=['#185FA5']
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            hourly = df.groupby('Hour')['InvoiceNo'].nunique().reset_index()
            hourly.columns = ['Hour', 'Orders']
            fig4 = px.bar(
                hourly,
                x='Hour',
                y='Orders',
                title='Orders by Hour of Day',
                color_discrete_sequence=['#185FA5']
            )
            st.plotly_chart(fig4, use_container_width=True)

        with col_b:
            dow = [
                'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday'
            ]
            daily = df.groupby('DayOfWeek')['InvoiceNo'].nunique().reset_index()
            daily.columns = ['Day', 'Orders']
            daily['Day'] = pd.Categorical(
                daily['Day'],
                categories=dow,
                ordered=True
            )
            daily = daily.sort_values('Day')
            fig5 = px.bar(
                daily,
                x='Day',
                y='Orders',
                title='Orders by Day of Week',
                color_discrete_sequence=['#185FA5']
            )
            st.plotly_chart(fig5, use_container_width=True)

    st.divider()
    st.markdown(
        "Built by **Tamil** | "
        "[GitHub](https://github.com/Tamil-ds/"
        "E-Commerce-Customer-Analytics)"
    )

except Exception as e:
    st.error(f"Error: {e}")
    st.info(
        "Make sure sample_data.csv is uploaded to GitHub root folder"
    )