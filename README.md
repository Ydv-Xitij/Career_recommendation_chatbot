# 💼 Career Recommendation Chatbot

A Streamlit-based chatbot powered by **Google Gemini API** and **rule-based logic** that helps users explore career paths, skills, and learning resources. Users can upload their resumes for personalized recommendations.

---

## ✅ Features
- Chat interface for career guidance
- Upload resume (PDF/DOCX) for AI-based analysis
- Extract key skills from resume using **SpaCy**
- Generate smart career suggestions using **Google Gemini**
- Fallback to **rule-based recommendations** if Gemini API fails
- Google Sheets integration for:
  - Logging chats
  - Storing user feedback
- Dark-themed, responsive UI

---

## 📂 Project Structure
```
CareerPath/
│
├── .streamlit/
│   └── secrets.toml       # API keys & config (not pushed to GitHub)
│
├── logic/
│   └── rules.py           # Rule-based career recommendation logic
│
├── services/
│   └── sheets.py          # Google Sheets integration
│
├── data/
│   └── careers.csv        # Career-related dataset
│
├── App.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignore sensitive files & caches
└── credentials.json       # Google API credentials (not pushed to GitHub)
```

---

## ⚙️ Setup Instructions

### **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/career-path-chatbot.git
cd career-path-chatbot
```

### **2. Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Add your secrets**
- Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your-google-gemini-api-key"
GOOGLE_SHEETS_SPREADSHEET_ID = "your-google-sheet-id"
```

- Add `credentials.json` (Google API OAuth file) to the root folder.

### **5. Run the app**
```bash
streamlit run App.py
```

---

## 🧠 How It Works
1. **Chat Input** → Sends user query & resume text to Gemini API.
2. **Gemini Response** → Provides personalized career advice.
3. **Fallback Mode** → If Gemini fails, rule-based logic provides suggestions.
4. **Google Sheets** → Logs chat history & feedback.

---

## 🚀 Deployment
You can deploy this app for free on:
- **Streamlit Cloud** → [https://streamlit.io/cloud](https://streamlit.io/cloud)
- **Render**
- **Heroku**

---

## 🙌 Contributions
Feel free to fork this repo and submit pull requests for improvements!

---

## 📜 License
MIT License © 2025 Kshitij Kumar
