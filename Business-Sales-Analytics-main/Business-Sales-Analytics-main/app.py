import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Business Sales Analytics",
    layout="wide"
)

st.title("Business Sales Analytics")

file = st.file_uploader("Upload Sales CSV file", type=["csv"])

required_cols = [
    'date','product_id','product_name',
    'category','outlet','quantity','unit_price'
]

if file:

    df = pd.read_csv(file)


    if not all(col in df.columns for col in required_cols):
        st.error("CSV format incorrect")
        st.stop()

   
    df["date"] = pd.to_datetime(df["date"])
    df["revenue"] = df["quantity"] * df["unit_price"]

    df["month"] = df["date"].dt.to_period("M").astype(str)  #gives period
    df["year"] = df["date"].dt.year     #gives integer

    st.success("File uploaded successfully!")

    
    total_revenue = df["revenue"].sum()
    total_orders = len(df)
    total_qty = df["quantity"].sum()
    avg_order_value = total_revenue / total_orders

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("Orders", total_orders)
    col3.metric("Units Sold", total_qty)
    col4.metric("Avg Order Value", f"₹{avg_order_value:.2f}")

    
    st.sidebar.header("Choose Analysis")

    option = st.sidebar.selectbox(
        "Select",
        [
            "Overall Sales",
            "Growth Analysis",
            "Product Analysis",
            "Category Analysis",
            "Outlet Analysis",
            "Top Days/Months",
        ]
    )
    
    if option == "Overall Sales":

        st.subheader("Filters")

        min_date = df["date"].min()
        max_date = df["date"].max()

        col1, col2, col3, col4 = st.columns(4)

        start_date = col1.date_input("Start Date", min_date)
        end_date = col2.date_input("End Date", max_date)

        product_filter = col3.multiselect(
            "Product",
            df["product_name"].unique(),
            default=df["product_name"].unique()
        )

        outlet_filter = col4.multiselect(
            "Outlet",
            df["outlet"].unique(),
            default=df["outlet"].unique()
        )

        category_filter = st.multiselect(
            "Category",
            df["category"].unique(),
            default=df["category"].unique()
        )

        
        filtered_df = df[
            (df["date"] >= pd.to_datetime(start_date)) &
            (df["date"] <= pd.to_datetime(end_date)) &
            (df["product_name"].isin(product_filter)) &
            (df["outlet"].isin(outlet_filter)) &
            (df["category"].isin(category_filter))
        ]

        st.markdown("---")

        
        st.subheader("Summary (Filtered Data)")

        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue", f"₹{filtered_df['revenue'].sum():,.0f}")
        c2.metric("Units Sold", filtered_df["quantity"].sum())
        c3.metric("Transactions", len(filtered_df))

        st.markdown("---")

        
        st.subheader("Daily Sales")

        daily = (filtered_df.groupby("date")["revenue"].sum().reset_index())

        st.line_chart(daily.set_index("date"))

        

        st.subheader("Monthly Sales")

        monthly = (filtered_df.groupby(filtered_df["date"].dt.to_period("M").dt.to_timestamp())["revenue"].sum().reset_index())

        monthly.columns = ["month", "revenue"]

        st.bar_chart(monthly.set_index("month"))


        
        st.subheader("Yearly Sales")

        yearly = (filtered_df.groupby(filtered_df["date"].dt.year)["revenue"].sum())

        st.bar_chart(yearly)

        
        st.download_button(
            "⬇ Download Filtered Data",
            filtered_df.to_csv(index=False),
            file_name="filtered_sales.csv",
        )

    # if option == "Overall Sales":

    #     st.subheader("Filters")

    #     min_date = df["date"].min()
    #     max_date = df["date"].max()

    #     col1, col2, col3, col4 = st.columns(4)

    #     start_date = col1.date_input("Start Date", min_date)
    #     end_date = col2.date_input("End Date", max_date)

    #     product_filter = col3.multiselect(
    #         "Product",
    #         df["product_name"].unique()
    #     )

    #     outlet_filter = col4.multiselect(
    #         "Outlet",
    #         df["outlet"].unique()
    #     )

    #     category_filter = st.multiselect(
    #         "Category",
    #         df["category"].unique()
    #     )


    #     filtered_df = df.copy()

    #     filtered_df = filtered_df[
    #         (filtered_df["date"] >= pd.to_datetime(start_date)) &
    #         (filtered_df["date"] <= pd.to_datetime(end_date))
    #     ]

    #     if product_filter:
    #         filtered_df = filtered_df[filtered_df["product_name"].isin(product_filter)]

    #     if outlet_filter:
    #         filtered_df = filtered_df[filtered_df["outlet"].isin(outlet_filter)]

    #     if category_filter:
    #         filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

    #     st.markdown("---")

    #     st.subheader("Summary (Filtered Data)")

    #     c1, c2, c3 = st.columns(3)
    #     c1.metric("Revenue", f"₹{filtered_df['revenue'].sum():,.0f}")
    #     c2.metric("Units Sold", filtered_df["quantity"].sum())
    #     c3.metric("Transactions", len(filtered_df))

    #     st.markdown("---")

    #     st.subheader("Daily Sales")

    #     daily = (filtered_df.groupby("date")["revenue"].sum().reset_index())

    #     st.line_chart(daily.set_index("date"))

    #     st.subheader("Monthly Sales")

    #     monthly = (filtered_df.groupby(filtered_df["date"].dt.to_period("M").dt.to_timestamp())["revenue"].sum().reset_index())

    #     monthly.columns = ["month", "revenue"]

    #     st.bar_chart(monthly.set_index("month"))

    #     st.subheader("Yearly Sales")

    #     yearly = (filtered_df.groupby(filtered_df["date"].dt.year)["revenue"].sum())

    #     st.bar_chart(yearly)

    #     st.download_button(
    #         "⬇ Download Data",
    #         filtered_df.to_csv(index=False),
    #         file_name="sales_data.csv",
    #     )



    elif option == "Growth Analysis":

        st.subheader("Month-over-Month Growth Analysis")

        min_date = df["date"].min()
        max_date = df["date"].max()

        col1, col2, col3 = st.columns(3)

        start_date = col1.date_input("Start Date", min_date, key="g1")
        end_date = col2.date_input("End Date", max_date, key="g2")

        category_filter = col3.multiselect(
            "Category",
            df["category"].unique(),
            default=df["category"].unique(),
            key="g3"
        )

        filtered_df = df[
            (df["date"] >= pd.to_datetime(start_date)) &
            (df["date"] <= pd.to_datetime(end_date)) &
            (df["category"].isin(category_filter))
        ]

        monthly = (filtered_df.groupby(filtered_df["date"].dt.to_period("M").dt.to_timestamp())["revenue"].sum().reset_index())

        monthly.columns = ["month", "revenue"]

        monthly["growth_%"] = monthly["revenue"].pct_change() * 100     #(pct_change = (current - previous)/previous)


        if len(monthly) > 1:
            latest_growth = monthly["growth_%"].iloc[-1]

            st.metric(
                "Latest MoM Growth",
                f"{latest_growth:.2f}%",
                delta=f"{latest_growth:.2f}%"
            )

        st.subheader("Monthly Revenue + Growth %")
        st.dataframe(monthly)

        st.subheader("Revenue Trend")
        st.line_chart(monthly.set_index("month")["revenue"])

        st.subheader("Growth % Trend")
        st.line_chart(monthly.set_index("month")["growth_%"])



    elif option == "Product Analysis" :
        product_sales = (df.groupby("product_name")["revenue"].sum().sort_values(ascending=False))

        st.subheader("Top Selling Products")
        st.dataframe(product_sales.head(10))

        st.bar_chart(product_sales.head(10))


    elif option == "Category Analysis":

        category_sales = (
            df.groupby("category")["revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("Category Performance")
        st.bar_chart(category_sales)


    elif option == "Outlet Analysis":

        outlet_sales = (
            df.groupby("outlet")["revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("Outlet Performance")
        st.bar_chart(outlet_sales)


    elif option == "Top Days/Months":

        daily = df.groupby("date")["revenue"].sum()
        monthly = df.groupby("month")["revenue"].sum()

        st.subheader("Top 5 Sales Days")
        st.dataframe(daily.sort_values(ascending=False).head(5))

        st.subheader("Top 5 Sales Months")
        st.dataframe(monthly.sort_values(ascending=False).head(5))


    st.sidebar.markdown("---")
    st.sidebar.subheader("Export Report")


    def create_summary_csv(df):

        output = io.StringIO()

        kpi_df = pd.DataFrame({
            "Metric": [
                "Total Revenue",
                "Total Orders",
                "Units Sold",
                "Average Order Value",
                "Start Date",
                "End Date"
            ],
            "Value": [
                df["revenue"].sum(),
                len(df),
                df["quantity"].sum(),
                round(df["revenue"].sum()/len(df), 2),
                df["date"].min(),
                df["date"].max()
            ]
        })

        output.write("===== SUMMARY =====\n")
        kpi_df.to_csv(output, index=False)
        output.write("\n\n")


        daily = df.groupby("date").agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum")
        ).reset_index()

        output.write("===== DAILY SALES =====\n")
        daily.to_csv(output, index=False)
        output.write("\n\n")


        monthly = df.groupby(df["date"].dt.to_period("M")).agg(
            revenue=("revenue", "sum")
        ).reset_index()

        output.write("===== MONTHLY SALES =====\n")
        monthly.to_csv(output, index=False)
        output.write("\n\n")


        yearly = df.groupby(df["date"].dt.year).agg(
            revenue=("revenue", "sum")
        ).reset_index()

        output.write("===== YEARLY SALES =====\n")
        yearly.to_csv(output, index=False)
        output.write("\n\n")


        top_products = (
            df.groupby("product_name")
            .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
            .sort_values("revenue", ascending=False)
            .head(10)
            .reset_index()
        )

        output.write("===== TOP PRODUCTS =====\n")
        top_products.to_csv(output, index=False)
        output.write("\n\n")


        category = (
            df.groupby("category")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        output.write("===== CATEGORY PERFORMANCE =====\n")
        category.to_csv(output, index=False)
        output.write("\n\n")


        outlet = (
            df.groupby("outlet")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        output.write("===== OUTLET PERFORMANCE =====\n")
        outlet.to_csv(output, index=False)


        return output.getvalue()


    summary_data = filtered_df if "filtered_df" in locals() else df

    csv_file = create_summary_csv(summary_data)


    st.sidebar.download_button(
        label="⬇ Download Sales Summary Report (CSV)",
        data=csv_file,
        file_name="Sales_Analytics_Summary_Report.csv",
    )



else:
    st.info("Upload your CSV file to begin.")
    st.info('the uploaded file should follow the following format : \ndate , product_id , product_name , category , outlet , quantity , unit_price')
