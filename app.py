import datetime
import PyPDF2
import streamlit as st
from utils.resume_parser import analyze_resume
from utils.jitsi_scheduler import schedule_jitsi_interview
from utils.email_sender import send_email
from utils.config import roles

# Function to extract text from the uploaded PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text.lower()  # Convert to lowercase for easy comparison

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
                # Extract resume text from PDF
                resume_text = extract_text_from_pdf(uploaded_resume)
                
                role_data = roles[selected_role]
                mandatory_skills = role_data["mandatory_skills"]
                role_skills = role_data["skills"]

                # Check if all mandatory skills are present in the resume
                missing_mandatory_skills = [skill for skill in mandatory_skills if skill not in resume_text]

                # Check how many total skills are found
                total_skills_found = [skill for skill in mandatory_skills + role_skills if skill in resume_text]
                
                if len(missing_mandatory_skills) == 0:
                    st.success(f"✅ Candidate is eligible for the role of {selected_role}.")
                    st.write(f"**Skills Found**: {', '.join(total_skills_found)}")
                    st.write(f"**Missing Mandatory Skills**: None")
                    st.write(f"**Total Skills Matched**: {len(total_skills_found)} out of {len(mandatory_skills + role_skills)}")

                else:
                    st.error(f"❌ Candidate does not meet all mandatory requirements for {selected_role}.")
                    st.write(f"**Skills Found**: {', '.join(total_skills_found)}")
                    st.write(f"**Missing Mandatory Skills**: {', '.join(missing_mandatory_skills)}")
                    st.write(f"**Total Skills Matched**: {len(total_skills_found)} out of {len(mandatory_skills + role_skills)}")

# Schedule Interview Page (manual scheduling)
# In the Schedule Interview section
elif app_mode == "Schedule Interview":
    st.subheader("📅 Schedule Jitsi Interview Manually")

    email_input = st.text_input("Enter Candidate Email")
    sender_email = st.text_input("Your Gmail Address")
    sender_password = st.text_input("Your Gmail Password", type="password")
    company_name = st.text_input("Company Name")
    job_role = st.text_input("Job Role")

    if st.button("Schedule Now"):
        if not email_input or not sender_email or not sender_password or not company_name or not job_role:
            st.warning("Please fill in all the fields.")
        else:
            # Schedule interview with Jitsi
            jitsi_link = schedule_jitsi_interview(email_input)
            interview_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")

            # Prepare and send email with proper formatting
            subject = f"Interview Invitation: {job_role}"
            body = f"""
Interview Details:

Company: {company_name}
Position: {job_role}
Date & Time (UTC): {interview_time}
Meeting Link: {jitsi_link}

Candidate Email: {email_input}
Meeting URL: {jitsi_link}
Scheduled Time: {interview_time}

Please join the meeting on time. We look forward to speaking with you.

Best Regards,
{company_name} Recruitment Team
"""

            result = send_email(subject, body, email_input, sender_email, sender_password)
            
            # Display formatted success message
            success_details = f"""
✅ Interview scheduled successfully!

Candidate Email: {email_input}
Meeting URL: {jitsi_link}
Scheduled Time: {interview_time}
"""
            st.success(success_details)
            st.info(result)
# About Page
elif app_mode == "About":
    st.subheader("🧠 About This App")
    st.markdown("""
    This **Resume Analyzer + Interview Scheduler** app helps recruiters streamline their recruitment process by automating resume analysis and interview scheduling.

    #### Key Features:
    - 📄 **Resume Analyzer**: Detects essential skills from resumes and matches them to job requirements.
    - 🧠 **Skill Evaluation**: Provides a detailed analysis of why a candidate fits (or doesn't fit) the role.
    - 📅 **Interview Scheduler**: Allows you to schedule interviews via Jitsi and send automated email notifications.

    #### Built with:
    - 🐍 **Python**
    - 📊 **Streamlit**
    - 🔗 **Jitsi Meet** for seamless interview scheduling

    **Creator**: Simran Shaikh  
    **GitHub**: [github.com/SimranShaikh20](https://github.com/SimranShaikh20)
    """)