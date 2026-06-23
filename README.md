# 🤖 AI Resume & Portfolio Builder

An **AI-assisted Resume, Portfolio, and Cover Letter Generator** built using **Python and Streamlit**.
This application helps **students, freshers, and job seekers** create **ATS-friendly resumes**, showcase **projects**, and evaluate resume strength against job descriptions — all from a simple web interface.

---

## 📌 Why This Project?

Many students rely on generic resume templates that:

* Don’t highlight individual strengths
* Are not optimized for Applicant Tracking Systems (ATS)
* Don’t match job-specific requirements

This project solves that problem by providing:
✔ Personalized resume content
✔ Keyword-based resume analysis
✔ Smart text enhancement
✔ Instant PDF generation

---

## ✨ Key Features

### 📝 Resume Builder

* Professional summary section
* Work experience management
* Skills section (comma-separated)
* Education details

### 🚀 Portfolio / Projects

* Add multiple projects
* Include GitHub or live project links
* Automatically included in resume PDF

### ✉️ Cover Letter Generator

* Job-specific cover letter draft
* Uses target role and company name
* Editable output

### 🧠 Smart AI-Assisted Tools

* Action-verb based bullet polishing
* Skill-based professional bio generation
* Offline AI logic (no API required)

### 📊 Resume Strength Analyzer

* Extracts keywords from job description
* Matches resume content against keywords
* Generates a **match score (%)**
* Helps improve ATS compatibility

### 📄 PDF Resume Export

* Clean, professional PDF layout
* One-click download
* Automatically structured sections

---

## 🛠️ Technology Stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| Frontend         | Streamlit               |
| Backend          | Python                  |
| PDF Engine       | FPDF                    |
| Text Analysis    | Regex                   |
| State Management | Streamlit Session State |

---

## 📂 Project Structure

```
AI_Resume_Builder/
│
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/AI_Resume_Builder.git
cd AI_Resume_Builder
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser.

---

## 📦 Requirements

```
streamlit
fpdf
```

> Optional (for real AI integration):

```
transformers
torch
```

---

## 🔍 How the Resume Match Score Works

1. Job description text is analyzed
2. Important keywords are extracted
3. Resume content is scanned for keyword presence
4. Match percentage is calculated
5. Suggestions are provided to improve alignment

This simulates **ATS screening behavior**.

---

## 🧠 AI Design Approach

This project currently uses:

* Rule-based NLP techniques
* Action verb enhancement
* Keyword density analysis

### 🔄 Scalability

The architecture allows easy integration with:

* OpenAI GPT models
* Hugging Face LLMs
* Gemini / LLaMA models

---

## 🎓 Academic Relevance

* Suitable for **Mini Projects**
* Final Year / Capstone Project
* Demonstrates:

  * NLP concepts
  * Resume optimization
  * PDF automation
  * UI development
  * Software design principles

---

## 🚀 Future Enhancements

* Multiple resume templates
* DOCX resume export
* Real-time AI suggestions
* LinkedIn profile import
* Cloud deployment (Streamlit Cloud)
* Database support (user profiles)

---

## 🧪 Example Use Case

> A student pastes a job description →
> Builds resume content →
> Checks match score →
> Polishes bullet points →
> Generates PDF →
> Applies with confidence

---
