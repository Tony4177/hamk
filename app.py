import streamlit as st
from datetime import datetime
from database import medicines_collection
from auth import register_user, login_user
from reminder import check_reminders

# ---------------- SIMPLE BUILT-IN AI ----------------
def get_ai_response(question):
    q = question.lower()

    if "miss dose" in q:
        return "Take it as soon as you remember. Skip if near next dose."

    elif "side effect" in q:
        return "Side effects depend on the medicine. Consult a doctor."

    elif "safe" in q:
        return "Medicine safety depends on dosage and condition."

    elif "when" in q:
        return "Check your scheduled medicines in dashboard."

    else:
        return "Consult a healthcare professional for serious concerns."

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Medicine Reminder", layout="centered")

# ---------------- LIME GREEN UI ----------------
st.markdown("""
<style>
body { background-color: white; }
.stApp { background-color: white; }
.stButton>button {
    background-color: #32CD32;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
    border: none;
}
.stButton>button:hover {
    background-color: #28a428;
}
section[data-testid="stSidebar"] {
    background-color: #f2fff2;
}
h1, h2, h3 { color: #228B22; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

st.title("💊 Medicine Reminder System")

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
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
if st.session_state.user:

    st.sidebar.success("Logged in as " + st.session_state.user["email"])

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.header("➕ Add Medicine")
    med_name = st.text_input("Medicine Name")
    med_time = st.time_input("Select Time")

    if st.button("Add Medicine"):
        if med_name.strip() != "":
            medicines_collection.insert_one({
                "user_id": st.session_state.user["_id"],
                "medicine_name": med_name,
                "time": med_time.strftime("%H:%M")
            })
            st.success("Medicine Added!")
            st.rerun()
        else:
            st.warning("Enter medicine name")

    st.header("📋 Your Medicines")

    user_meds = list(medicines_collection.find({
        "user_id": st.session_state.user["_id"]
    }))

    if user_meds:
        for med in user_meds:
            col1, col2 = st.columns([4,1])
            with col1:
                st.write(f"💊 {med['medicine_name']}  |  ⏰ {med['time']}")
            with col2:
                if st.button("❌", key=str(med["_id"])):
                    medicines_collection.delete_one({"_id": med["_id"]})
                    st.rerun()
    else:
        st.info("No medicines added yet.")

    st.header("⏰ Reminder Status")
    due = check_reminders(st.session_state.user["_id"])

    if due:
        for med in due:
            st.warning(f"Time to take {med}!")
    else:
        st.success("No medicines due right now.")

    st.header("🤖 Medicine Assistant")
    question = st.text_input("Ask about dosage, missed dose, safety etc")

    if st.button("Ask AI"):
        if question.strip() != "":
            response = get_ai_response(question)
            st.info(response)
        else:
            st.warning("Please enter a question")
