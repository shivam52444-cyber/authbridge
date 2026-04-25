# dashboards/manager_dashboard.py
import streamlit as st
from databasesetup import SessionLocal
from schema import Candidate

def manager_dashboard():
    st.title("Manager Review")
    
    db = SessionLocal()
    
    candidates = db.query(Candidate).filter_by(status="shortlisted").all()
    
    for c in candidates:
        st.subheader(c.name)
        st.write(c.summary)
        
        if st.button(f"Approve {c.id}"):
            c.status = "approved"
            db.commit()
        
        if st.button(f"Reject {c.id}"):
            c.status = "rejected"
            db.commit()