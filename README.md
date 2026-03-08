# 🎯 Quotes Recommendation Chatbot using NLP (Rasa + Streamlit)

An intelligent conversational AI chatbot that recommends personalized quotes based on user intent and emotions — built using **Rasa NLU** for natural language understanding and **Streamlit** for the web interface.

---

## 📌 Project Overview

The Quotes Recommendation Chatbot is an NLP-powered conversational system designed to provide personalized quotes based on user mood, interests, and preferences. The chatbot understands natural language input and responds with motivational, inspirational, love, success, humorous, life, happiness, or wisdom quotes through interactive conversation.

This project demonstrates the practical implementation of **Natural Language Processing (NLP)** and **Conversational AI** using the Rasa framework, with a modern **Streamlit** web frontend replacing the traditional Flask approach.

---

## 🚀 Key Features

- ✅ **15 Intent Classifications** using Rasa NLU (improved from 9)
- ✅ **8 Quote Categories**: Motivation, Inspiration, Love, Success, Funny, Life, Happiness, Wisdom
- ✅ **80+ Quote Variations** in domain responses (improved from 10)
- ✅ **Optimized NLU Pipeline** with character n-grams for better accuracy
- ✅ **Emotional Support**: Detects when users feel sad or stressed
- ✅ **Fallback Mechanism** for unrecognized inputs
- ✅ **Interactive Feedback System** (satisfied / not satisfied flows)
- ✅ **Dynamic Category Switching** when user wants different quotes
- ✅ **Streamlit Frontend** with premium dark theme UI
- ✅ **REST API Integration** between Streamlit and Rasa
- ✅ **Real-time Chat Interface** with session management
- ✅ **350+ Training Examples** for high intent accuracy

---

## 🏗️ System Architecture

```
User → Streamlit UI → REST API → Rasa NLU → Rasa Core → Response → Streamlit UI → User
```

### Architecture Diagram:
```
┌──────────────┐
│     User     │
└──────┬───────┘
       │  (types message)
       ▼
┌──────────────────┐
│  Streamlit UI    │
│  (app.py :8501)  │
└──────┬───────────┘
       │  HTTP POST (REST API)
       ▼
┌──────────────────┐
│  Rasa Server     │
│  (:5005)         │
├──────────────────┤
│  Rasa NLU        │  ← Intent Classification
│  (config.yml)    │    (WhitespaceTokenizer → CountVectors
│                  │     → DIETClassifier → FallbackClassifier)
├──────────────────┤
│  Rasa Core       │  ← Dialogue Management
│  (stories.yml,   │    (MemoizationPolicy → RulePolicy
│   rules.yml)     │     → TEDPolicy)
├──────────────────┤
│  Domain          │  ← Response Selection
│  (domain.yml)    │    (80+ quote variations)
└──────┬───────────┘
       │  JSON Response
       ▼
┌──────────────────┐
│  Streamlit UI    │  ← Displays quote to user
└──────────────────┘
```

### Components:
| Component | Role |
|-----------|------|
| **Rasa NLU** | Intent classification & entity extraction |
| **Rasa Core** | Dialogue management & conversation flow |
| **Streamlit** | Web-based chat interface (replaces Flask) |
| **REST API** | Communication between frontend & backend |
| **domain.yml** | Intents, responses & configuration |
| **stories.yml** | Conversation flow training data |
| **rules.yml** | Fixed conversation rules |
| **config.yml** | NLU pipeline & dialogue policies |
| **models/** | Trained chatbot model storage |

---

## 🛠️ Technologies Used

- **Python** 3.8–3.10 (3.9 recommended)
- **Rasa** 3.6.21 (NLU + Core)
- **Streamlit** ≥1.28.0 (Web Frontend)
- **REST API** (Rasa webhook)
- **YAML** Configuration Files
- **scikit-learn** (via Rasa pipeline)
- **TensorFlow** (via Rasa DIET Classifier)

---

## 📂 Project Structure

```
QUOTES-RECOMMENDATION-CHATBOT/
│
├── actions/
│   ├── __init__.py
│   └── actions.py              # Custom actions (extendable)
│
├── data/
│   ├── nlu.yml                 # Training data (350+ examples, 15 intents)
│   ├── stories.yml             # Conversation flows (35+ stories)
│   └── rules.yml               # Fixed conversation rules (6 rules)
│
├── models/                     # Trained model storage (auto-generated)
│
├── tests/
│   └── test_stories.yml        # Automated test stories (14 tests)
│
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
│
├── app.py                      # Streamlit frontend application
├── config.yml                  # NLU pipeline & policies (optimized)
├── credentials.yml             # REST API channel configuration
├── domain.yml                  # Intents, responses, session config
├── endpoints.yml               # Service endpoints
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── Prerequisites.txt           # Setup prerequisites
└── README.md                   # This documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment
```bash
conda create --name rasa_env python=3.9 -y
conda activate rasa_env
```

### 2️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install rasa[full] streamlit requests
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

### 3️⃣ Initialize Rasa Project (if starting fresh)
```bash
rasa init
```
> **Note:** This project already includes all required files.

---

## 🧠 Model Training

Train the chatbot model:
```bash
rasa train
```

This trains both:
- **NLU model** — for intent classification
- **Dialogue model** — for conversation management

The trained model is saved in the `models/` directory.

---

## 🧪 Testing

### Test via Rasa Shell (CLI)
```bash
rasa shell
```

Test inputs:
- `hi` → Greeting response
- `give me motivation` → Motivational quote
- `inspire me` → Inspirational quote
- `love quote` → Love quote
- `make me laugh` → Funny quote
- `success quote` → Success quote
- `quote about life` → Life quote
- `happiness quote` → Happiness quote
- `wise words` → Wisdom quote
- `i am feeling sad` → Emotional support
- `i am stressed` → Stress support
- `help` → Category listing
- `bye` → Goodbye

### Test Using Test Stories
```bash
rasa test
```

---

## 🌐 Web Deployment with Streamlit

### Step 1: Enable REST API
Ensure `credentials.yml` contains:
```yaml
rest:
```

### Step 2: Run Rasa Server
```bash
rasa run --enable-api --cors "*"
```

### Step 3: Run Streamlit App
Open a **new terminal** and run:
```bash
streamlit run app.py
```

The app opens at: `http://localhost:8501`

---

## 📊 Improvements Over Reference Project

| Aspect | Original | Improved |
|--------|----------|----------|
| **Intents** | 9 | 15 (+67%) |
| **Training Examples** | ~55 | 350+ (+536%) |
| **Quote Categories** | 5 | 8 (+60%) |
| **Quotes per Category** | 2 | 10 (+400%) |
| **Total Quotes** | ~10 | 80+ (+700%) |
| **Conversation Stories** | 8 | 35+ (+337%) |
| **Rules** | 2 | 6 (+200%) |
| **NLU Pipeline** | Default (null) | Optimized explicit |
| **DIET Epochs** | 100 | 150 (+50%) |
| **Fallback Threshold** | 0.3 | 0.4 (stricter) |
| **Frontend** | Flask + HTML/JS | Streamlit |
| **Emotional Support** | ❌ | ✅ (sad & stressed) |
| **Help System** | ❌ | ✅ |
| **Test Stories** | ❌ | ✅ (14 tests) |

---

## 🎯 Business Impact

- Promotes **mental well-being** through instant motivational support
- Provides **24/7 emotional support** for sad or stressed users
- Enhances **user engagement** with interactive conversations
- Demonstrates practical **Conversational AI** application
- **Scalable** to wellness, education, and customer service domains

---

## 📚 Dataset

Quotes used in this chatbot are collected from **publicly available motivational quote datasets** and **manually curated lists** from well-known authors, leaders, and thinkers including:

- Winston Churchill, Steve Jobs, Mahatma Gandhi, Albert Einstein
- Aristotle, Confucius, Socrates, Buddha, Rumi
- Mark Twain, Ralph Waldo Emerson, Theodore Roosevelt
- Dalai Lama, Oprah Winfrey, Maya Angelou
- And many more renowned personalities

The quotes are organized into **8 categories** with **10 variations each**, stored in `domain.yml` as Rasa response templates. Training examples in `data/nlu.yml` cover **15 intents** with **350+ user query variations** to ensure high intent recognition accuracy.

---

## 🔮 Future Enhancements

- Emotion Detection using Sentiment Analysis
- Machine Learning-based Personalization
- Multilingual Support (Hindi, Telugu, etc.)
- Voice-based Interaction
- Social Media Integration (WhatsApp, Telegram)
- Dynamic Quote APIs
- Analytics Dashboard
- Transformer-based NLP Models (BERT integration)

---

## 👨‍💻 Author

Developed as part of the **Artificial Intelligence & Machine Learning** module project.

## 📜 License

This project is developed for academic and educational purposes.
