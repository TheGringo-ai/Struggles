# utils/firebase_config.py
# Add Firebase authentication and Streamlit UI
import streamlit as st
import pyrebase
from firebase_admin import firestore
from utils.firebase_config import db

# Firebase Web config (replace with your actual credentials)
firebase_config = {
    "apiKey": "your-web-api-key",
    "authDomain": "chatterfix-ui.firebaseapp.com",
    "projectId": "chatterfix-ui",
    "storageBucket": "chatterfix-ui.appspot.com",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "measurementId": "YOUR_MEASUREMENT_ID",
    "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Login UI
if "user" not in st.session_state:
    st.title("🔐 Sign in to Struggles AI")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state["user"] = user
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")
    st.stop()

user_email = st.session_state["user"]["email"]
st.sidebar.success(f"👋 Logged in as {user_email}")

try:
    doc_ref = db.collection("user_sessions").document(user_email).collection("sessions").document()
    doc_ref.set({
        "agent": agent_role,
        "prompt": user_input,
        "response": response,
        "model": st.session_state["model"],
        "timestamp": firestore.SERVER_TIMESTAMP
    })
except Exception as e:
    st.warning(f"⚠️ Firestore logging failed: {e}")