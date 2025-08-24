import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime

# ✅ Required Scopes for Google Sheets & Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    """Create and return a Google Sheets client."""
    try:
        # ✅ Streamlit Cloud secrets
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
        sheet_id = st.secrets["GOOGLE_SHEETS_SPREADSHEET_ID"]
    except Exception as e:
        st.error(f"⚠️ Failed to load Streamlit secrets: {e}. Trying local fallback...")
        # ✅ Local fallback for development
        try:
            with open("credentials.json") as f:
                creds_info = json.load(f)
            creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
            sheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
            if not sheet_id:
                sheet_id = "13_CB5OT4HfAuoPNYW9CoahU6oNhv_L6mgdIcrhmJZhI"  # Default sheet ID
        except Exception as e_local:
            st.error(f"❌ Failed to load local credentials: {e_local}")
            raise e_local

    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)

def get_sheet():
    """Return the 'Chats' worksheet."""
    try:
        client = get_client()
        return client.worksheet("Chats")  # Ensure tab is named 'Chats'
    except Exception as e:
        st.error(f"❌ Error accessing 'Chats' sheet: {e}")
        raise e

def log_chat(user_message, bot_response, skills="", interests=""):
    """Log chat message with optional skills & interests."""
    try:
        sheet = get_sheet()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Convert any complex data to strings
        if isinstance(bot_response, (list, dict)):
            bot_response = json.dumps(bot_response, ensure_ascii=False)
        if isinstance(skills, (list, dict)):
            skills = ", ".join(map(str, skills))
        if isinstance(interests, (list, dict)):
            interests = ", ".join(map(str, interests))

        sheet.append_row([timestamp, str(user_message), str(bot_response), str(skills), str(interests)])
        st.success("✅ Chat logged successfully!")
    except Exception as e:
        st.error(f"⚠️ Could not log chat: {e}")

def log_feedback(feedback_text, rating):
    """Log feedback in the 'Feedback' sheet (second tab)."""
    try:
        client = get_client()
        feedback_sheet = client.worksheet("Feedback")  # Ensure tab is named 'Feedback'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_sheet.append_row([timestamp, str(feedback_text), str(rating)])
        st.success("✅ Feedback logged successfully!")
    except Exception as e:
        st.error(f"⚠️ Could not log feedback: {e}")


