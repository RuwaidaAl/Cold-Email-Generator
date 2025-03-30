import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Load environment variables (API keys, etc.)
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    layout="centered", 
    page_title="Cold Email Generator", 
    page_icon="📧"
)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
        /* Overall styling */
        body {
            background-color: #f4f6f9;
        }
        
        /* Stylish title */
        .title {
            font-size: 32px !important;
            font-weight: bold;
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }

        /* Description styling */
        .subheader {
            font-size: 18px;
            text-align: center;
            color: #555;
        }

        /* Input box styling */
        .stTextInput>div>div>input {
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #ddd;
            background: white;
        }

        /* Generate button with hover effects */
        .stButton button {
            background: linear-gradient(to right, #4CAF50, #45a049);
            color: white !important;
            font-size: 16px !important;
            padding: 12px 26px !important;
            border-radius: 8px !important;
            border: none !important;
            transition: 0.3s ease-in-out !important;
        }

        .stButton button:hover {
            background: linear-gradient(to right, #45a049, #4CAF50);
            transform: scale(1.05);
        }

        /* Email box with glassmorphism */
        .stTextArea textarea {
            font-size: 15px;
            font-family: 'Arial', sans-serif;
            white-space: pre-wrap;
            resize: none; /* Disable manual resizing */
            background: rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            padding: 15px;
            border: 2px solid #ddd;
            backdrop-filter: blur(10px);
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }

        /* Spinner animation */
        .spinner {
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<div class="title">📧 Cold Email Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Generate cold emails for job applications effortlessly!</div>', unsafe_allow_html=True)

# Input field for the job posting URL
url_input = st.text_input(
    "🔗 Enter a job posting URL:", 
    value="https://careers.nike.com/information-security-engineer-ii-eiam/job/R-43993"
)

# Button to generate email
st.markdown("<br>", unsafe_allow_html=True)
submit_button = st.button("🚀 Generate Email")

# If the button is clicked
if submit_button:
    with st.spinner("⏳ Fetching job details & crafting your email..."):
        try:
            # Load job posting data from the given URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Load portfolio data and process job information
            portfolio = Portfolio()
            portfolio.load_portfolio()
            chain = Chain()
            jobs = chain.extract_jobs(data)

            # Display generated emails
            for job in jobs:
                st.markdown("### ✉️ Your Custom Cold Email")
                
                # Get skills from job description
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)

                # Generate email content
                email = chain.write_mail(job, links)

                # Automatically adjust email box height based on content length
                email_length = len(email.split("\n")) * 20  # Adjust height per line
                st.text_area("Generated Email:", value=email, height=min(max(email_length, 200), 500))

            # Success message
            st.success("✅ Email generated successfully! 🎉")

        except FileNotFoundError as e:
            st.error(f"❌ File not found: {e}")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")

# Print API key for debugging (optional)
print("Groq API Key:", os.getenv("GROQ_API_KEY"))
