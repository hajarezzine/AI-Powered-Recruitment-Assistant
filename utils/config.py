import os
import streamlit as st

# Job roles and required keywords
roles = {
    "ai_ml_engineer": ["machine learning", "python", "deep learning", "pandas", "tensorflow"],
    "frontend_engineer": ["javascript", "react", "css", "html", "typescript"],
    "backend_engineer": ["java", "python", "node.js", "rest api", "sql"]
}

# utils/config.py

# Replace these with your email credentials
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-email-password"  # Consider using environment variables for better security
