# 🚀 HireIQ — AI-Powered Recruitment Intelligence System

HireIQ is an end-to-end AI-driven recruitment platform designed to automate and optimize the hiring pipeline using LLMs, structured scoring, and decision analytics.

It enables:

* HRs to post and analyze job descriptions
* Automated resume scoring using AI
* Managers to review shortlisted candidates
* Leaders to monitor hiring quality and HR performance

---

# 🧠 System Architecture (High-Level)

* **Frontend:** Streamlit dashboards (HR / Manager / Leader)
* **Backend:** Python + SQLAlchemy ORM
* **AI Layer:** LangChain + Groq LLM (JD analysis + resume scoring)
* **Database:** SQLite (lightweight, local)

---

# 📂 Project Structure

```
.
├── main_app.py
├── auth.py
├── databasesetup.py
├── initdb.py
├── schema.py
├── hr_dashboard.py
├── managerdashboard.py
├── leaderdashboard.py
├── jd_analysis_chain.py
├── resume_scoringchain.py
├── parser.py
├── resumeparser.py
├── requirements.txt
└── hrms.db (auto-created)
```

---

# ⚙️ Setup Instructions (Step-by-Step)

## 1️⃣ Clone / Download Project

```bash
git clone <your-repo-url>
cd HireIQ
```

---

## 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup Environment Variables

Create a `.env` file in root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

## 5️⃣ Initialize Database

```bash
python initdb.py
```

This will:

* Create all tables (users, jobs, candidates)
* Initialize SQLite DB (`hrms.db`)

---

## 6️⃣ Run the Application

```bash
streamlit run main_app.py
```

---

# 🔐 Default Login Credentials

| Role    | Email                                             | Password |
| ------- | ------------------------------------------------- | -------- |
| HR      | [hr@company.com](mailto:hr@company.com)           | 123      |
| Manager | [manager@company.com](mailto:manager@company.com) | 123      |
| Leader  | [leader@company.com](mailto:leader@company.com)   | 123      |

---

# 💡 Features Breakdown

## 👩‍💼 HR Dashboard

* Post Job Descriptions
* AI-based JD analysis (difficulty + skill breakdown)
* Upload multiple resumes (PDF)
* Automated resume scoring
* Candidate shortlisting/rejection with reasons

---

## 👨‍💼 Manager Dashboard

* Review shortlisted candidates
* Approve or reject candidates

---

## 📊 Leader Dashboard

* HR performance analytics:

  * Shortlist vs reject trends
  * Average scoring patterns
  * Quality score (decision intelligence)
* AI alerts for poor hiring decisions

---

# 🧠 AI Components

### 1. JD Analysis

* Extracts:

  * Must-have skills
  * Good-to-have skills
  * Soft skills
* Assigns weighted importance

---

### 2. Resume Scoring

* Computes:

  * Overall score (0–100)
  * Strengths & gaps
  * Hiring recommendation

---

# 📊 Key Metrics (Leader Layer)

* **Shortlist Rate**
* **Average Candidate Score**
* **HR Quality Score = (Shortlisted Avg - Rejected Avg)**

👉 This is where your system becomes *decision intelligence*, not just automation.

---

# ⚠️ Important Notes

* Only **PDF resumes** are supported
* Ensure `.env` is correctly configured
* SQLite is used → for production, migrate to PostgreSQL

---

# 🚀 Future Improvements

* JWT Authentication
* Role-based access control (RBAC)
* PostgreSQL / cloud DB
* Real-time analytics (Plotly / dashboards)
* Feedback loop for model improvement
* Bias detection in hiring decisions

---

# 🧩 Tech Stack Summary

* Python
* Streamlit
* SQLAlchemy
* LangChain
* Groq LLM
* Pandas + Matplotlib
* PyMuPDF

---

# 📌 Final Note

This project is not just a CRUD app — it’s a **decision intelligence system** for hiring.

It combines:

* AI reasoning
* Structured evaluation
* Human-in-the-loop decision making

---

🔥 Built for scalable, data-driven hiring systems.
