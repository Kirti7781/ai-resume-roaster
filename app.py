import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
import re

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# =========================
# GROQ CLIENT
# =========================
client = Groq(api_key=api_key)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Resume Roaster",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# MODERN AESTHETIC UI
# =========================
st.markdown("""
<style>

/* Background */

.stApp {
    background: linear-gradient(
        135deg,
        #0f0c29,
        #302b63,
        #24243e
    );
    color: white;
}

/* Main container */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 8%;
    padding-right: 8%;
}

/* Title */

.main-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(to right, #ff9966, #ff5e62);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2em;
}

.subtitle {
    text-align: center;
    color: #cfcfcf;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Glassmorphism cards */

.glass {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 16px;
    height: 3.3em;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(
        to right,
        #ff512f,
        #dd2476
    );
    color: white;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 20px rgba(255,94,98,0.6);
}

/* Upload box */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Metrics */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
}

/* Progress bar */

.stProgress > div > div > div > div {
    background: linear-gradient(
        to right,
        #ff9966,
        #ff5e62
    );
}

/* Text */

h1, h2, h3 {
    color: white;
}

p, label {
    color: #e5e5e5;
}

/* Selectbox */

div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.08);
    border-radius: 12px;
}

/* Download button */

.stDownloadButton > button {
    background: linear-gradient(
        to right,
        #00c6ff,
        #0072ff
    );
    color: white;
    border-radius: 14px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown(
    """
    <div class='main-title'>
        🔥 AI Resume Roaster
    </div>

    <div class='subtitle'>
        ATS Analyzer • JD Matcher • Recruiter Simulation • Gen-Z Roast AI
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# INPUT SECTION
# =========================
st.markdown("<div class='glass'>", unsafe_allow_html=True)

level = st.slider(
    "🔥 Roast Level",
    1,
    10,
    5
)

recruiter_mode = st.selectbox(
    "😈 Recruiter Personality",
    [
        "FAANG Recruiter 👔",
        "Startup Founder 🚀",
        "Toxic HR 💀",
        "Gen-Z Recruiter 🔥",
        "ATS Bot 🤖"
    ]
)

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "💼 Paste Job Description",
    height=250,
    placeholder="""
Example:

We are looking for a frontend developer skilled in:
React.js
Next.js
Tailwind CSS
TypeScript
REST APIs
Git
Deployment
"""
)

st.markdown("</div>", unsafe_allow_html=True)

resume_text = ""

# =========================
# PDF EXTRACTION
# =========================
if uploaded_file is not None:

    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text

    st.success("✅ Resume uploaded successfully!")

# =========================
# ANALYZE BUTTON
# =========================
if st.button("🚀 Analyze My Resume"):

    if resume_text.strip() == "":
        st.warning("Please upload a resume first.")

    else:

        prompt = f"""
        You are acting as:

        {recruiter_mode}

        Analyze this resume dynamically.

        If recruiter mode is Gen-Z:
        Use meme humor, internet slang, sarcasm,
        and funny Gen-Z style roasting.

        Compare the uploaded resume with the provided job description.

        Generate realistic and dynamic analysis.

        Return EXACTLY in this format:

        ATS SCORE: <number>

        SHORTLIST CHANCE: <percentage>

        INTERVIEW CHANCE: <percentage>

        GHOSTING PROBABILITY: <percentage>

        CORPORATE SURVIVAL RATING: <rating>

        MATCH SCORE: <percentage>

        RECRUITER REACTION:
        <reaction>

        ROAST:
        <funny roast>

        GOOD THINGS:
        <good things>

        PROBLEMS:
        <problems>

        MISSING KEYWORDS:
        <missing keywords>

        JOB FIT ANALYSIS:
        <analysis>

        TAILORED IMPROVEMENTS:
        <specific suggestions>

        FINAL VERDICT:
        <verdict>

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Roast Level:
        {level}/10
        """

        try:

            with st.spinner(
                "💀 Recruiters are judging your existence..."
            ):

                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama-3.1-8b-instant",
                )

            roast = response.choices[0].message.content

            # =========================
            # REGEX EXTRACTION
            # =========================
            score_match = re.search(
                r"ATS SCORE:\s*(\d+)",
                roast
            )

            shortlist_match = re.search(
                r"SHORTLIST CHANCE:\s*(\d+%)",
                roast
            )

            interview_match = re.search(
                r"INTERVIEW CHANCE:\s*(\d+%)",
                roast
            )

            ghost_match = re.search(
                r"GHOSTING PROBABILITY:\s*(\d+%)",
                roast
            )

            survival_match = re.search(
                r"CORPORATE SURVIVAL RATING:\s*(.*)",
                roast
            )

            match_score_match = re.search(
                r"MATCH SCORE:\s*(\d+%)",
                roast
            )

            score = int(score_match.group(1)) if score_match else 50

            shortlist = (
                shortlist_match.group(1)
                if shortlist_match else "50%"
            )

            interview = (
                interview_match.group(1)
                if interview_match else "50%"
            )

            ghosting = (
                ghost_match.group(1)
                if ghost_match else "50%"
            )

            survival = (
                survival_match.group(1)
                if survival_match else "Average Human"
            )

            match_score = (
                match_score_match.group(1)
                if match_score_match else "50%"
            )

            # =========================
            # ATS SCORE SECTION
            # =========================
            st.markdown("<div class='glass'>", unsafe_allow_html=True)

            st.subheader("📊 ATS Resume Score")

            st.progress(score)

            st.metric(
                "ATS Score",
                f"{score}/100"
            )

            if score >= 80:
                st.success("🔥 Excellent Resume")

            elif score >= 60:
                st.info("👍 Decent Resume")

            else:
                st.error("💀 Resume needs serious improvements")

            st.markdown("</div>", unsafe_allow_html=True)

            # =========================
            # JD MATCH SECTION
            # =========================
            st.markdown("<div class='glass'>", unsafe_allow_html=True)

            st.subheader("🎯 Job Description Match")

            st.metric(
                "💼 Resume Match Score",
                match_score
            )

            match_number = int(
                match_score.replace("%", "")
            )

            if match_number >= 80:
                st.success("🔥 Strong Match for this role")

            elif match_number >= 60:
                st.info("👍 Decent match but can improve")

            else:
                st.error("💀 Recruiter rejection speedrun")

            st.markdown("</div>", unsafe_allow_html=True)

            # =========================
            # REALITY CHECK
            # =========================
            st.subheader("📡 Resume Reality Check")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "📄 Shortlist Chance",
                    shortlist
                )

                st.metric(
                    "🎤 Interview Chance",
                    interview
                )

            with col2:

                st.metric(
                    "👻 Ghosting Probability",
                    ghosting
                )

                st.metric(
                    "🏢 Corporate Survival",
                    survival
                )

            # =========================
            # ANALYSIS OUTPUT
            # =========================
            st.markdown("<div class='glass'>", unsafe_allow_html=True)

            st.subheader(
                f"🧠 Recruiter Mode: {recruiter_mode}"
            )

            st.subheader("🤖 AI Analysis")

            st.write(roast)

            st.download_button(
                label="📥 Download Report",
                data=roast,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:

            st.error(f"❌ Error: {e}")