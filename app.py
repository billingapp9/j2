import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Attendance Demo", layout="wide")

st.title("🚀 Distributor Attendance & Payroll Demo System")

# ------------------ SESSION STORAGE ------------------

if "employees" not in st.session_state:
    st.session_state.employees = pd.DataFrame(columns=["Name", "Role", "Department", "Salary"])

if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(columns=[
        "Name", "Date", "In Time", "Out Time",
        "Working Hours", "Status", "Overtime"
    ])

if "advances" not in st.session_state:
    st.session_state.advances = pd.DataFrame(columns=["Name", "Amount", "Date"])

# ------------------ RESET BUTTON ------------------

if st.sidebar.button("🔄 Reset Demo"):
    st.session_state.employees = pd.DataFrame(columns=["Name", "Role", "Department", "Salary"])
    st.session_state.attendance = pd.DataFrame(columns=[
        "Name", "Date", "In Time", "Out Time",
        "Working Hours", "Status", "Overtime"
    ])
    st.session_state.advances = pd.DataFrame(columns=["Name", "Amount", "Date"])
    st.sidebar.success("Demo Reset Done")

# ------------------ SIDEBAR MENU ------------------

menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Employees",
    "Attendance",
    "Advances",
    "Payroll"
])

# =====================================================
# 1️⃣ DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.header("📊 Live Dashboard")

    total_emp = len(st.session_state.employees)
    today = str(date.today())

    today_att = st.session_state.attendance[
        st.session_state.attendance["Date"] == today
    ]

    present = len(today_att[today_att["Status"] == "Present"])
    half = len(today_att[today_att["Status"] == "Half Day"])
    absent = total_emp - present - half

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", total_emp)
    col2.metric("Present Today", present)
    col3.metric("Half Day", half)
    col4.metric("Absent Today", absent)

    if total_emp > 0:
        chart_data = pd.DataFrame({
            "Count": [present, half, absent]
        }, index=["Present", "Half Day", "Absent"])

        st.bar_chart(chart_data)

# =====================================================
# 2️⃣ EMPLOYEES
# =====================================================

elif menu == "Employees":

    st.header("👥 Employee Management")

    # ---------------- ADD EMPLOYEE ----------------

    with st.form("Add Employee"):
        name = st.text_input("Employee Name")
        role = st.selectbox("Role", [
            "Salesman",
            "Computer Operator",
            "Helper",
            "Driver"
        ])
        salary = st.number_input("Monthly Salary", min_value=0)
        status = st.selectbox("Status", ["Active", "Inactive"])

        submit = st.form_submit_button("Add Employee")

        if submit and name != "":
            new_row = pd.DataFrame([[name, role, salary, status]],
                                   columns=["Name", "Role", "Salary", "Status"])

            st.session_state.employees = pd.concat(
                [st.session_state.employees, new_row],
                ignore_index=True
            )

            st.success("Employee Added Successfully")

    st.markdown("---")

    # ---------------- EDIT EMPLOYEE ----------------

    st.subheader("Edit Employees")

    if not st.session_state.employees.empty:

        # Create a copy for editing
        if "temp_edit" not in st.session_state:
            st.session_state.temp_edit = st.session_state.employees.copy()

        edited_df = st.data_editor(
            st.session_state.temp_edit,
            use_container_width=True,
            num_rows="dynamic"
        )

        col1, col2 = st.columns(2)

        if col1.button("✅ Update Changes"):
            st.session_state.employees = edited_df
            st.session_state.temp_edit = edited_df.copy()
            st.success("Employee Data Updated Successfully")

        if col2.button("❌ Cancel Changes"):
            st.session_state.temp_edit = st.session_state.employees.copy()
            st.warning("Changes Cancelled")

# =====================================================
# 3️⃣ ATTENDANCE
# =====================================================

elif menu == "Attendance":

    st.header("🕒 Mark Attendance")

    if st.session_state.employees.empty:
        st.warning("Please add employees first.")
    else:
        emp_list = st.session_state.employees["Name"].tolist()
        selected = st.selectbox("Select Employee", emp_list)

        col1, col2 = st.columns(2)
        in_time = col1.time_input("In Time")
        out_time = col2.time_input("Out Time")

        if st.button("Mark Attendance"):

            in_dt = datetime.combine(date.today(), in_time)
            out_dt = datetime.combine(date.today(), out_time)

            hours = (out_dt - in_dt).total_seconds() / 3600

            if hours >= 8:
                status = "Present"
            elif hours >= 4:
                status = "Half Day"
            else:
                status = "Absent"

            overtime = max(0, hours - 8)

            new_row = pd.DataFrame([[
                selected,
                str(date.today()),
                str(in_time),
                str(out_time),
                round(hours, 2),
                status,
                round(overtime, 2)
            ]], columns=[
                "Name", "Date", "In Time", "Out Time",
                "Working Hours", "Status", "Overtime"
            ])

            st.session_state.attendance = pd.concat(
                [st.session_state.attendance, new_row], ignore_index=True
            )

            st.success(f"Attendance Marked: {status}")

    st.subheader("Attendance Records")
    st.dataframe(st.session_state.attendance, use_container_width=True)

# =====================================================
# 4️⃣ ADVANCES
# =====================================================

elif menu == "Advances":

    st.header("💵 Give Advance")

    if st.session_state.employees.empty:
        st.warning("Add employees first.")
    else:
        emp_list = st.session_state.employees["Name"].tolist()
        selected = st.selectbox("Select Employee", emp_list)
        amount = st.number_input("Advance Amount", min_value=0)

        if st.button("Give Advance"):
            new_row = pd.DataFrame([[selected, amount, str(date.today())]],
                                   columns=["Name", "Amount", "Date"])
            st.session_state.advances = pd.concat(
                [st.session_state.advances, new_row], ignore_index=True)
            st.success("Advance Recorded")

    st.subheader("Advance Records")
    st.dataframe(st.session_state.advances, use_container_width=True)

# =====================================================
# 5️⃣ PAYROLL
# =====================================================

elif menu == "Payroll":

    st.header("💰 Payroll Calculation")

    if st.session_state.employees.empty:
        st.warning("Add employees first.")
    else:
        for _, emp in st.session_state.employees.iterrows():

            name = emp["Name"]
            salary = emp["Salary"]

            emp_att = st.session_state.attendance[
                st.session_state.attendance["Name"] == name
            ]

            present_days = len(emp_att[emp_att["Status"] == "Present"])
            half_days = len(emp_att[emp_att["Status"] == "Half Day"])

            earned_days = present_days + (half_days * 0.5)

            per_day_salary = salary / 30 if salary else 0
            earned_salary = earned_days * per_day_salary

            emp_adv = st.session_state.advances[
                st.session_state.advances["Name"] == name
            ]["Amount"].sum()

            final_salary = earned_salary - emp_adv

            st.subheader(f"Employee: {name}")
            st.write("Present Days:", present_days)
            st.write("Half Days:", half_days)
            st.write("Earned Days:", earned_days)
            st.write("Earned Salary: ₹", round(earned_salary, 2))
            st.write("Advance Deduction: ₹", emp_adv)
            st.write("Final Salary: ₹", round(final_salary, 2))
            st.markdown("---")


