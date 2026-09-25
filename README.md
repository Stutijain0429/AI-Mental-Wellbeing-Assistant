# 💙 MindEase – AI Mental Wellbeing Assistant

### Understand Your Emotions. Reflect. Feel Supported.

---

## 📌 Overview

MindEase is an AI-powered mental wellbeing assistant that helps users understand and reflect on their emotions through text.

The application uses a fine-tuned DistilBERT emotion classification model to detect emotions from user input and provides supportive responses, wellbeing suggestions, mood history, and an emotion distribution dashboard.

It also includes a basic safety layer that identifies high-risk expressions and provides an appropriate support message.

---

## ✨ Features

* 🧠 AI-based Emotion Detection
* 💬 Emotional Support
* 🌱 Wellbeing Suggestions
* ❤️ 6 Emotion Classes
* 📊 Mood History Tracking
* 📈 Emotion Distribution Dashboard
* 🛡️ Basic Safety Detection
* ⚡ Interactive Streamlit Interface
* 🎯 Prediction Confidence Score
* 🔄 Randomized Support Responses
* 💙 Clean and Minimal UI

---

## 🧠 Supported Emotions

| Label | Emotion  |
| ----: | -------- |
|     0 | Sadness  |
|     1 | Joy      |
|     2 | Love     |
|     3 | Anger    |
|     4 | Fear     |
|     5 | Surprise |

---

## 🏗️ Architecture

```text
User Input
    │
    ▼
Safety Check
    │
    ├── High-Risk Input
    │       │
    │       ▼
    │   Safety Response
    │
    └── Normal Input
            │
            ▼
      DistilBERT Model
            │
            ▼
      Emotion Detection
            │
            ▼
     Wellbeing Response
            │
            ▼
       Mood History
            │
            ▼
     Emotion Dashboard
            │
            ▼
       Streamlit UI
```

---

## 🛠️ Tech Stack

| Category        | Technology                |
| --------------- | ------------------------- |
| Language        | Python                    |
| UI              | Streamlit                 |
| NLP Model       | DistilBERT                |
| Deep Learning   | PyTorch                   |
| Transformers    | Hugging Face Transformers |
| Dataset         | DAIR-AI Emotion Dataset   |
| Data Processing | Pandas, NumPy             |
| Evaluation      | Scikit-learn              |
| Visualization   | Plotly                    |
| Development     | Jupyter Notebook          |

---

## 📊 Model Performance

The emotion classification model was fine-tuned using the DAIR-AI Emotion Dataset containing six emotion classes.

| Metric          |     Score |
| --------------- | --------: |
| Accuracy        | **74.2%** |
| Precision       | **74.1%** |
| Recall          | **74.2%** |
| F1 Score        | **69.2%** |
| Validation Loss | **0.856** |

---

## 📂 Project Structure

```text
AI-Mental-Wellbeing-Assistant/
│
├── app/
│   ├── models/
│   │   └── text_emotion.py
│   │
│   ├── services/
│   │   └── wellbeing.py
│   │
│   ├── ui/
│   │   └── streamlit_app.py
│   │
│   └── utils/
│       └── safety.py
│
├── assets/
├── Data/
├── notebooks/
│   └── text_emotion_training.ipynb
├── tests/
├── requirements.txt
├── test_setup.py
├── .gitignore
└── README.md
```

> Note: Trained model files are excluded from GitHub because of their size and are stored locally.

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/Stutijain0429/AI-Mental-Wellbeing-Assistant.git
cd AI-Mental-Wellbeing-Assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

**Windows:**

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app/ui/streamlit_app.py
```

---

## 💡 How It Works

### 1. User Input

The user writes how they are feeling or what is currently on their mind.

### 2. Safety Check

The application checks the input for predefined high-risk expressions.

### 3. Emotion Detection

For normal inputs, the text is passed to the fine-tuned DistilBERT model.

### 4. Support Response

Based on the detected emotion, MindEase provides a supportive message and a simple wellbeing suggestion.

### 5. Mood History

Analyzed emotions are stored during the current session.

### 6. Mood Dashboard

The dashboard displays total analyses, the most detected emotion, and emotion distribution.

---

## 🛡️ Safety

MindEase includes a basic keyword-based safety layer for detecting certain high-risk expressions.

When a high-risk expression is detected, the application does not continue with normal emotion analysis. Instead, it displays a supportive safety message encouraging the user to contact appropriate emergency services, a trusted person, or a qualified mental-health professional when necessary.

**MindEase is not a replacement for professional mental health care.**

---

## 🔮 Future Improvements

* 🎤 Voice Emotion Detection
* 🧠 Improved Emotion Classification
* 📱 Mobile Application
* 👤 Personalized User Profiles
* 📊 Long-Term Mood Analytics
* 🔐 Secure Mood History Storage
* 🌍 Multilingual Emotion Detection
* 🤖 Conversational AI Support
* ☁️ Cloud Deployment

---

## 👩‍💻 Author

**Stuti Jain**

B.Tech CSE (AI/ML) Student | AI/ML Enthusiast

---

⭐ If you like this project, consider giving it a star!
