import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000"

st.title("Student Management System")

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API}/login", json={"username": user, "password": pwd})

        data = res.json()

        if res.status_code == 200 and "token" in data:
            st.session_state.token = data["token"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error(data.get("error", "Login failed"))

        st.write(res.status_code)
        st.write(res.json())

else:
    menu = st.sidebar.selectbox("Menu", ["Add", "View", "Update", "Delete"])

    if menu == "Add":
        st.subheader("Add Student")
        roll = st.text_input("Roll")
        name = st.text_input("Name")

        mar = st.number_input("Marathi", 0, 100)
        eng = st.number_input("English", 0, 100)
        mat = st.number_input("Maths", 0, 100)
        es1 = st.number_input("Env", 0, 100)
        arts = st.number_input("Arts", 0, 100)
        prac = st.number_input("Prac", 0, 100)
        pe = st.number_input("PE", 0, 100)

        if st.button("Submit"):
            requests.post(f"{API}/add_student", json=locals())
            st.success("Added")

    elif menu == "View":
        res = requests.get(f"{API}/students")
        df = pd.DataFrame(res.json())
        st.dataframe(df)

    elif menu == "Update":
        st.subheader("Update Student")
        roll = st.text_input("Roll")

        name = st.text_input("New Name")
        mar = st.number_input("Marathi", 0, 100)
        eng = st.number_input("English", 0, 100)
        mat = st.number_input("Maths", 0, 100)
        es1 = st.number_input("Env", 0, 100)
        arts = st.number_input("Arts", 0, 100)
        prac = st.number_input("Prac", 0, 100)
        pe = st.number_input("PE", 0, 100)

        if st.button("Update"):
            requests.put(f"{API}/update_student", json=locals())
            st.success("Updated")

    elif menu == "Delete":
        roll = st.text_input("Roll")
        if st.button("Delete"):
            requests.delete(f"{API}/delete_student/{roll}")
            st.success("Deleted")
