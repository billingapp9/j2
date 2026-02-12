import streamlit as st

st.set_page_config(page_title="Distributor ERP", layout="wide")

# ---- HEADER ----
st.title("🏢 Distributor ERP System")
st.caption("Business Management Dashboard")

# ---- SIDEBAR MENU ----
menu = st.sidebar.radio(
    "📂 Navigation",
    [
        "Dashboard",
        "Item Master",
        "Customer Master",
        "Supplier Master",
        "Purchase",
        "Sales",
        "Collections",
        "Stock Report",
        "Outstanding Report",
        "GST Report"
    ]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Today Sales", "₹ 25,000")
    col2.metric("Monthly Sales", "₹ 4,50,000")
    col3.metric("Outstanding", "₹ 1,20,000")
    col4.metric("Stock Value", "₹ 8,75,000")

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Top Customers")
        st.write("1. Sai Traders")
        st.write("2. Lakshmi Stores")
        st.write("3. Ramesh Kirana")

    with col6:
        st.subheader("Low Stock Alerts")
        st.warning("🔴 Parle-G 100g - Low Stock")
        st.warning("🔴 Sunflower Oil 1L - Low Stock")


# ---------------- ITEM MASTER ----------------
elif menu == "Item Master":
    st.subheader("📦 Item Master")

    col1, col2, col3 = st.columns(3)

    col1.text_input("Item Code")
    col2.text_input("Item Name")
    col3.text_input("Category")

    col4, col5, col6 = st.columns(3)

    col4.selectbox("Unit", ["Nos", "Kg", "Litre", "Box"])
    col5.number_input("Purchase Price")
    col6.number_input("Selling Price")

    col7, col8, col9 = st.columns(3)

    col7.number_input("MRP")
    col8.number_input("GST %")
    col9.number_input("Minimum Stock Level")

    st.toggle("Active", value=True)

    st.button("💾 Save Item")


# ---------------- CUSTOMER MASTER ----------------
elif menu == "Customer Master":
    st.subheader("🏪 Customer Master")

    col1, col2 = st.columns(2)
    col1.text_input("Customer Name")
    col2.text_input("Outlet Name")

    col3, col4 = st.columns(2)
    col3.text_input("Mobile Number")
    col4.text_input("Route")

    col5, col6 = st.columns(2)
    col5.number_input("Credit Limit")
    col6.number_input("Credit Days")

    st.toggle("Active", value=True)

    st.button("💾 Save Customer")


# ---------------- SALES ----------------
elif menu == "Sales":
    st.subheader("🧾 Sales Invoice")

    col1, col2, col3 = st.columns(3)
    col1.text_input("Invoice Number")
    col2.date_input("Invoice Date")
    col3.selectbox("Customer", ["Sai Traders", "Lakshmi Stores"])

    st.divider()

    st.markdown("### Add Items")

    col4, col5, col6, col7 = st.columns(4)
    col4.selectbox("Item", ["Parle-G", "Oil 1L"])
    col5.number_input("Quantity")
    col6.number_input("Rate")
    col7.number_input("Discount")

    st.button("➕ Add Item")

    st.divider()

    col8, col9, col10 = st.columns(3)
    col8.number_input("Tax Amount")
    col9.number_input("Total Amount")
    col10.selectbox("Payment Mode", ["Cash", "Credit", "UPI", "Bank"])

    st.button("🧾 Save Invoice")


# ---------------- STOCK REPORT ----------------
elif menu == "Stock Report":
    st.subheader("📦 Stock Report")

    st.dataframe({
        "Item": ["Parle-G", "Oil 1L"],
        "Opening": [100, 50],
        "Purchase": [200, 100],
        "Sales": [150, 60],
        "Damage": [5, 2],
        "Closing": [145, 88]
    })


# ---------------- OUTSTANDING REPORT ----------------
elif menu == "Outstanding Report":
    st.subheader("💳 Outstanding Report")

    st.dataframe({
        "Customer": ["Sai Traders", "Lakshmi Stores"],
        "Opening": [10000, 5000],
        "Sales": [25000, 12000],
        "Collections": [20000, 8000],
        "Outstanding": [15000, 9000]
    })


# ---------------- GST REPORT ----------------
elif menu == "GST Report":
    st.subheader("🧾 GST Summary")

    st.dataframe({
        "Tax Slab": ["5%", "12%", "18%"],
        "Taxable Amount": [50000, 80000, 120000],
        "Output GST": [2500, 9600, 21600],
        "Input GST": [2000, 7000, 18000],
        "Net GST Payable": [500, 2600, 3600]
    })
