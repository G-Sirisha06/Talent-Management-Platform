# 🚀 Talent Management Platform

An AI-powered **Talent Management Platform** designed to help students and users improve their learning, technical skills, assessment performance, and interview preparation through an integrated platform.

---

## 📌 About the Project

The **Talent Management Platform** provides a structured environment where users can learn from study materials, attend assessments, interact with an AI assistant, analyze their resumes, and prepare for interviews.

The platform also includes an **Admin module** that allows administrators to manage users, documents, exams, and announcements.

---

## ✨ Key Features

### 👤 User Features

- 🔐 Secure User Login
- 📚 36-Day Learning Portal
- 📄 Day-wise Learning Materials
- 📝 Online Assessments and Exams
- 🤖 AI Assistant
- 📄 Resume Analyzer
- 🔍 Semantic Document Search
- 🎤 AI Voice Mock Interview
- 📊 Learning Progress Tracking
- 📢 Announcements

### ⚙️ Admin Features

- 👥 User Management
- 📥 Document Ingestion
- 📝 Exam Management
- 🤖 AI Assistant
- 📢 Announcement Management
- 📊 Platform Overview

---

## 📚 Learning Portal

The Learning Portal provides a structured **36-day learning journey**.

Users can:

1. Select a learning day.
2. Open the corresponding PDF material.
3. Study the provided content.
4. Mark the lesson as completed.
5. Unlock the next learning day.
6. Attend assessments after completing the required lessons.
7. Unlock the AI Voice Mock Interview based on assessment performance.

### 🔄 Learning Flow

```text
Day 01
  ↓
Day 02
  ↓
Day 03
  ↓
Day 04
  ↓
Day 05 Assessment
  ↓
Score > 70%
  ↓
Day 06 AI Voice Mock Interview
This pattern continues throughout the 36-day learning journey.
📝 Assessment System
The platform provides assessments based on the learning materials.
Students must complete the required learning content before accessing the assessment.
The assessment result determines whether the next stage of interview preparation can be unlocked.
🎤 AI Voice Mock Interview
The AI Voice Mock Interview helps users practice real interview situations.
It includes:
Basic introduction questions
HR-related questions
Technical questions
Voice-based answers
AI-based response evaluation
Performance feedback
📊 AI Feedback
After the interview, the system provides feedback on:
Technical Knowledge
Communication Skills
Strengths
Areas for Improvement
Overall Performance
Final Recommendations
🛠️ Technologies Used
Python
Streamlit
SQLite
HTML
CSS
Machine Learning
Natural Language Processing
Generative AI
PDF Processing
Semantic Search
Voice Processing
Groq LLM
📂 Project Structure
Talent-Management-Platform/
│
├── app.py
│
├── pages/
│   ├── Dashboard
│   ├── Learning Portal
│   ├── Exams
│   ├── Resume Analyzer
│   ├── AI Assistant
│   └── Voice Mock Interview
│
├── src/
│   └── Supporting modules
│
├── Documents/
│   └── Day-wise learning materials
│
├── data/
│   └── Application data
│
├── assets/
│   └── Images and resources
│
├── requirements.txt
├── README.md
└── .gitignore
🔐 Security
Sensitive information such as API keys, passwords, environment variables, database files, and audio files are excluded from the GitHub repository.
The .gitignore file contains:
.env
*.pyc
env/
.venv/
*.db
*.mp3
*.webm
__pycache__/
🎯 Project Objective
The main objective of this project is to create a single platform for learning, assessment, and interview preparation.
The platform follows the journey:
Learn
  ↓
Practice
  ↓
Assess
  ↓
Improve
  ↓
Prepare for Interviews
🚀 Future Enhancements
Advanced AI-based performance analytics
Personalized learning recommendations
Improved voice conversation
Advanced resume-job matching
Real-time interview scoring
More learning courses and assessments
Personalized career recommendations
👩‍💻 Project
Talent Management Platform
An AI-powered platform for:
Learning • Assessment • Skill Development • Interview Preparation
Learn → Practice → Assess → Improve → Succeed 🚀
