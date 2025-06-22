import streamlit as st
import hashlib
from firebase_admin import firestore
import pandas as pd
import altair as alt

st.set_page_config(page_title="Welcome to ChatterFix", page_icon="public/favicon.ico", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .main {
        text-align: center;
        margin-top: 80px;
    }
    .logo {
        width: 80px;
        margin-bottom: 20px;
    }
    .title {
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 10px;
        color: #222;
    }
    .subtitle {
        font-size: 1.2em;
        color: #555;
        margin-bottom: 30px;
    }
    .button {
        font-size: 1.1em;
        background-color: #0072e3;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        text-decoration: none;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.image("public/logo.png", width=80)
st.markdown("<div class='title'>ChatterFix</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smarter Maintenance, Training, and Troubleshooting — Powered by AI</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# --- Helper function for avatar ---
def get_avatar_url(email, user_data=None):
    if user_data and "photoUrl" in user_data:
        return user_data["photoUrl"]
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=https://cdn-icons-png.flaticon.com/512/847/847969.png"

# --- Role check function ---
def get_user_role(email):
    if email.endswith("@gringosgambit.com"):
        return "admin"
    else:
        return "tech"

role = None
if "user" in st.session_state:
    email = st.session_state["user"]["email"]
    db = firestore.client()
    user_doc = db.collection("users").document(email)
    all_users = db.collection("users").stream()

    # Aggregate data
    total_users = 0
    login_count = 0
    last_login = "N/A"

    for user in all_users:
        data = user.to_dict()
        total_users += 1
        if data.get("usage", {}).get("lastLogin"):
            login_count += 1
        if data.get("email") == email:
            last_login = data.get("usage", {}).get("lastLogin", "Unknown")
            personal_logins = data.get("usage", {}).get("logins", 0)
        else:
            personal_logins = 0

    role = get_user_role(email)
    st.image(get_avatar_url(email, st.session_state["user"]), width=60)
    st.success(f"🔐 {email} ({role})")
    if st.button("🚪 Sign Out"):
        del st.session_state["user"]
        st.markdown(
            '<meta http-equiv="Set-Cookie" content="id_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT">',
            unsafe_allow_html=True
        )
        st.experimental_rerun()

    if role == "admin":
        st.markdown("### 👤 Admin Dashboard")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Users", total_users)
        with col2:
            st.metric("Logins This Week", login_count)

        st.markdown("#### 🔍 Management Modules")
        st.markdown("#### 📊 User Activity Overview")

        # Load user analytics from Firestore
        activity_data = []
        all_users = db.collection("users").stream()
        for user in all_users:
            info = user.to_dict()
            usage = info.get("usage", {})
            if "lastLogin" in usage:
                activity_data.append({
                    "email": info.get("email", "N/A"),
                    "role": info.get("role", "tech"),
                    "logins": usage.get("logins", 0),
                    "lastLogin": usage.get("lastLogin", "N/A")
                })

        if activity_data:
            df = pd.DataFrame(activity_data)
            st.dataframe(df)

            st.altair_chart(
                alt.Chart(df).mark_bar().encode(
                    x=alt.X("email", sort="-y"),
                    y="logins",
                    color="role"
                ).properties(title="Login Frequency by User"),
                use_container_width=True
            )
        if st.button("Launch Main Assistant"):
            st.switch_page("app.py")
        if st.button("Work Order Review"):
            st.switch_page("work_order.py")
        if st.button("Reports & Analytics"):
            st.switch_page("reports.py")

    else:
        st.markdown("### 🛠 Technician Dashboard")

        st.markdown("#### Your Stats")
        st.metric("Logins", personal_logins)
        st.metric("Last Login", last_login)

        st.markdown("#### Tools")
        if st.button("Open Technician Dashboard"):
            st.switch_page("technician.py")
else:
    from firebase_admin import auth as admin_auth, credentials, initialize_app
    import firebase_admin
    import os
    import json
    if not firebase_admin._apps:
        firebase_key = json.loads(os.environ["FIREBASE_KEY_JSON"])
        cred = credentials.Certificate(firebase_key)
        initialize_app(cred)

    if "id_token" not in st.session_state:
        import streamlit.runtime.scriptrunner.script_run_context as src
        from http.cookies import SimpleCookie

        try:
            ctx = src.get_script_run_ctx()
            headers = ctx.request.headers
            if "cookie" in headers:
                cookie = SimpleCookie()
                cookie.load(headers["cookie"])
                if "id_token" in cookie:
                    st.session_state["id_token"] = cookie["id_token"].value
        except Exception:
            pass

    if "id_token" not in st.session_state:
        st.warning("Redirecting to login...")
        st.markdown('<meta http-equiv="refresh" content="0;url=/public/login.html">', unsafe_allow_html=True)
        st.stop()

    try:
        decoded_token = admin_auth.verify_id_token(st.session_state["id_token"])
        email = decoded_token["email"]
        photo_url = decoded_token.get("picture", "")
        st.session_state["user"] = {
            "email": email,
            "photoUrl": photo_url
        }
        st.experimental_rerun()
    except Exception as e:
        st.error("Invalid login. Please try again.")
        st.markdown('<meta http-equiv="refresh" content="0;url=/public/login.html">', unsafe_allow_html=True)
        st.stop()