import streamlit as st
import os
from datetime import datetime
from database import medicines_collection
from auth import register_user, login_user
from reminder import check_reminders
from ai_assistant import get_ai_response

st.set_page_config(page_title="Medicine Reminder", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

st.title("💊 Medicine Reminder App")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(email, password):
            st.success("Account created successfully!")
        else:
            st.error("User already exists")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.success("Logged in successfully")
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
if st.session_state.user:
    st.sidebar.success("Logged in as " + st.session_state.user["email"])

    st.header("Add Medicine")
    med_name = st.text_input("Medicine Name")
    med_time = st.time_input("Select Time")

    if st.button("Add Medicine"):
        medicines_collection.insert_one({
            "user_id": st.session_state.user["_id"],
            "medicine_name": med_name,
            "time": med_time.strftime("%H:%M")
        })
        st.success("Medicine Added!")

    st.header("Your Medicines")
    user_meds = medicines_collection.find({"user_id": st.session_state.user["_id"]})
    
    for med in user_meds:
        st.write(f"{med['medicine_name']} - {med['time']}")
        if st.button(f"Delete {med['_id']}"):
            medicines_collection.delete_one({"_id": med["_id"]})
            st.experimental_rerun()

    st.header("Reminder Check")
    due = check_reminders(st.session_state.user["_id"])
    if due:
        for med in due:
            st.warning(f"⏰ Time to take {med}!")

    st.header("AI Assistant 🤖")
    question = st.text_input("Ask something about your medicine")
    if question:
        response = get_ai_response(question)
        st.info(response)