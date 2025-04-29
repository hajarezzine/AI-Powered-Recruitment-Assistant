import datetime
import streamlit as st
from utils.resume_parser import analyze_resume
from utils.jitsi_scheduler import schedule_jitsi_interview  # Using Jitsi for scheduling
from utils.config import roles

# Page config
st.set_page_config(page_title="Resume Analyzer + Interview Scheduler", layout="wide")
st.title("📄 Resume Analyzer + Interview Scheduler")

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
app_mode = st.sidebar.radio("Go to", ["Resume Analyzer", "Schedule Interview", "About"])

# Resume Analyzer Page
if app_mode == "Resume Analyzer":
    st.subheader("📑 Analyze Resume and Auto-Schedule Interview")

    uploaded_resume = st.file_uploader("Upload Candidate Resume (PDF)", type=["pdf"])
    selected_role = st.selectbox("Select Job Role", list(roles.keys()))

    if st.button("Analyze Resume"):
        if not uploaded_resume:
            st.warning("Please provide the resume.")
        else:
            with st.spinner("Analyzing resume..."):
                analysis = analyze_resume(uploaded_resume, selected_role)

            st.write(analysis['message'])

            if analysis['status'] == "selected":
                # Assuming you have candidate email input here
                candidate_email = st.text_input("Enter Candidate Email for Interview")
                if candidate_email:
                    jitsi_link = schedule_jitsi_interview(candidate_email)  # Scheduling interview with email
                    # Assuming interview time is scheduled 1 day later
                    interview_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")
                    st.success(f"✅ Interview scheduled. [Join Link]({jitsi_link})")
                else:
                    st.warning("Please enter the candidate's email to schedule the interview.")
            else:
                st.error("❌ Candidate not selected.")

# Schedule Interview Page (for manual use if needed)
elif app_mode == "Schedule Interview":
    st.subheader("📅 Schedule Jitsi Interview Manually")
    email_input = st.text_input("Enter Candidate Email for Scheduling")

    if st.button("Schedule Now"):
        if not email_input:
            st.warning("Please enter an email.")
        else:
            jitsi_link = schedule_jitsi_interview(email_input)  # Scheduling interview with email
            # Send the interview details (you can customize this as needed)
            interview_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")
            st.success(f"✅ Interview scheduled. [Join Link]({jitsi_link})")

# About Page
elif app_mode == "About":
    st.subheader("🧠 About This App")
    st.markdown("""
    This **Resume Analyzer + Interview Scheduler** app helps recruiters:
    - Parse resumes to detect relevant skills.
    - Automatically decide if a candidate should move forward.
    - Schedule Jitsi interviews seamlessly.

    #### Built with:
    - 🐍 Python
    - 📊 Streamlit
    - 📅 Jitsi

    **Creator:** Simran  
    **GitHub:** [github.com/simranxyz](https://github.com/simranxyz)
    """)
