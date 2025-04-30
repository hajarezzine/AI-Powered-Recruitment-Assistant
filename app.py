import datetime
import streamlit as st
from utils.resume_parser import analyze_resume
from utils.jitsi_scheduler import schedule_jitsi_interview
from utils.email_sender import send_email
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
                st.success("✅ Good choice! Candidate is selected for interview.")
                st.text_input("Candidate Status", value=analysis['message'], disabled=True)
            else:
                st.error("❌ Candidate not selected.")

# Schedule Interview Page (manual scheduling)
elif app_mode == "Schedule Interview":
    st.subheader("📅 Schedule Jitsi Interview Manually")

    email_input = st.text_input("Enter Candidate Email")
    sender_email = st.text_input("Your Gmail Address")
    sender_password = st.text_input("Your Gmail Password", type="password")

    if st.button("Schedule Now"):
        if not email_input or not sender_email or not sender_password:
            st.warning("Please fill in all the fields.")
        else:
            jitsi_link = schedule_jitsi_interview(email_input)
            interview_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")

            subject = "Your Interview Schedule"
            body = f"""
Dear Candidate,

Your interview has been scheduled.

🕑 Date & Time (UTC): {interview_time}  
🔗 Join Link: {jitsi_link}

Regards,  
Recruitment Team
"""

            result = send_email(subject, body, email_input, sender_email, sender_password)
            st.success(f"✅ Interview scheduled. [Join Link]({jitsi_link})")
            st.info(result)

# About Page
elif app_mode == "About":
    st.subheader("🧠 About This App")
    st.markdown("""
    This **Resume Analyzer + Interview Scheduler** app helps recruiters:
    - 📄 Parse resumes to detect relevant skills.
    - 🧠 Automatically decide if a candidate should move forward.
    - 📅 Schedule Jitsi interviews seamlessly.

    #### Built with:
    - 🐍 Python
    - 📊 Streamlit
    - 🔗 Jitsi Meet

    **Creator:** Simran  
    **GitHub:** [github.com/simranxyz](https://github.com/simranxyz)
    """)
