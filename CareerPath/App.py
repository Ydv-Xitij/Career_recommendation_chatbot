import google.generativeai as genai
import os
import PyPDF2
import docx
import spacy
import streamlit as st
from logic.rules import recommend
from services.sheets import log_chat, log_feedback

# ✅ Load NLP model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("⚠ SpaCy model not found. Run: python -m spacy download en_core_web_sm")
    st.stop()

# ✅ Get Gemini API Key
gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("❌ Gemini API Key not found. Add it in `.streamlit/secrets.toml` or environment variables.")
    st.stop()

# ✅ Configure Gemini
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# ✅ Page settings
st.set_page_config(page_title="Career Chatbot", page_icon="💼", layout="centered")

# ✅ Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""
if "profile_skills" not in st.session_state:
    st.session_state["profile_skills"] = ""
if "profile_interests" not in st.session_state:
    st.session_state["profile_interests"] = ""

# ✅ Title
st.title("💼 Career Recommendation Chatbot")
st.write("Chat with me to explore career paths, skills, and learning resources! 🤖")

# ✅ Sidebar: Resume Upload
st.sidebar.subheader("📂 Upload Your Resume")
uploaded_file = st.sidebar.file_uploader("Choose file", type=["pdf", "docx"], label_visibility="collapsed")

# ✅ Extract text from resume
def extract_text_from_resume(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text.strip()

# ✅ Extract entities (skills, interests)
def extract_entities(text):
    doc = nlp(text)
    skills = [token.text.capitalize() for token in doc if token.pos_ == "NOUN" and len(token.text) > 2]
    return list(set(skills))[:10], []  # No NLP for interests yet

# ✅ Process uploaded resume
if uploaded_file:
    resume_text = extract_text_from_resume(uploaded_file)
    st.session_state["resume_text"] = resume_text

    extracted_skills, extracted_interests = extract_entities(resume_text)

    if st.session_state["profile_skills"].strip() == "":
        st.session_state["profile_skills"] = ", ".join(extracted_skills)
        st.sidebar.success(f"✅ Extracted Skills: {st.session_state['profile_skills']}")

    if st.session_state["profile_interests"].strip() == "":
        st.session_state["profile_interests"] = ", ".join(extracted_interests)

# ✅ Gemini response with fallback
def get_gemini_response(user_message, resume_text="", profile_skills="", profile_interests="", work_style=""):
    context_prompt = f"""
You are a professional career advisor.
User message: {user_message}

User Profile:
- Skills: {profile_skills if profile_skills else "Not provided"}
- Interests: {profile_interests if profile_interests else "Not provided"}
- Preferred Work Style: {work_style}

Resume Content:
{resume_text if resume_text else "No resume uploaded"}

"""

    try:
        response = model.generate_content(context_prompt)
        if response and response.text:
            return response.text
        else:
            return None
    except Exception:
        return None  # Signal failure

# ✅ Chat Input
user_input = st.chat_input("Type your message here...")

if user_input and user_input.strip():
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        # Try Gemini first
        gemini_reply = get_gemini_response(
            user_message=user_input,
            resume_text=st.session_state["resume_text"],
            profile_skills=st.session_state["profile_skills"],
            profile_interests=st.session_state["profile_interests"],
            work_style=""
        )

        if gemini_reply:
            bot_reply = gemini_reply
        else:
            # Fallback logic
            profile = {
                "skills": st.session_state["profile_skills"],
                "interests": st.session_state["profile_interests"],
                "style": ""
            }
            bot_reply = f"⚠ Gemini failed. Rule-based suggestion:\n\n{recommend(profile)}"

    # Add assistant response to history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # ✅ Log chat
    try:
        log_chat(user_input, bot_reply, st.session_state["profile_skills"], st.session_state["profile_interests"])
    except Exception as e:
        st.error(f"⚠️ Logging failed: {e}")

# ✅ Display ALL chat messages
with st.container():
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ✅ Sidebar: Feedback section
st.sidebar.subheader("📢 Feedback")
feedback_text = st.sidebar.text_area("Your Feedback")
rating = st.sidebar.slider("Rate your experience", 1, 5, 3)

if st.sidebar.button("Submit Feedback"):
    try:
        log_feedback(feedback_text, rating)
        st.sidebar.success("✅ Feedback saved to Google Sheets!")
    except Exception as e:
        st.sidebar.error(f"⚠️ Could not save feedback: {e}")

# ✅ Sidebar: Export chat
if st.sidebar.button("📥 Export Chat"):
    chat_text = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["messages"]])
    st.sidebar.download_button("Download Chat", data=chat_text, file_name="chat_history.txt")

st.sidebar.caption("🔒 Your data is private and not shared externally.")








