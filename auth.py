import streamlit as st

USERS = {
    "hr@company.com": {"password": "123", "role": "HR", "id": 101},
    "manager@company.com": {"password": "123", "role": "Manager", "id": 201},
    "leader@company.com": {"password": "123", "role": "Leader", "id": 301},
}

def login():
    st.title("HireIQ Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = USERS.get(email)
        
        if user and user["password"] == password:
            st.session_state["user"] = email
            st.session_state["role"] = user["role"]

            # 🔥 CRITICAL FIX
            st.session_state["user_id"] = user["id"]

            st.success(f"Logged in as {user['role']}")
            st.rerun()
        else:
            st.error("Invalid credentials")