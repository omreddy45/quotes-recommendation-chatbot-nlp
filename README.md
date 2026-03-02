# Quotes Recommendation Chatbot using Rasa NLU

A smart chatbot that recommends quotes based on user mood, interests, and preferences — built using Rasa NLU for natural language understanding.

---

## 📋 Prerequisites

Before getting started, make sure you have the following tools and technologies set up on your system. All items are also listed in the `Prerequisites.txt` file for quick reference.

---

### 1. Python Virtual Environment

A virtual environment isolates your project's dependencies from the system-wide Python installation, preventing version conflicts between different projects.

**Why it's needed:** Rasa has specific dependency versions that may conflict with other Python packages on your system. A virtual environment keeps everything clean and reproducible.

**Setup:**
```bash
# Create a virtual environment named 'rasa_env' with Python 3.9
conda create --name rasa_env python=3.9 -y

# Activate the environment
conda activate rasa_env
```

> ⚠️ Always activate the virtual environment before working on the project.

---

### 2. Anaconda Navigator & Python

**Anaconda Navigator** is a desktop GUI for managing conda packages, environments, and channels without using the command line. It bundles Python along with many useful data science libraries.

- **Python Version:** 3.8 to 3.10 (3.9 recommended)
- **Download Anaconda:** [https://www.anaconda.com/download](https://www.anaconda.com/download)

**Why it's needed:** Anaconda simplifies environment and package management, making it easy to create isolated Python environments for the project. It also comes pre-installed with essential scientific computing libraries.

**Installation Steps:**
1. Download Anaconda from the link above.
2. Run the installer and follow on-screen instructions.
3. After installation, open **Anaconda Prompt** (Windows) or your terminal (Mac/Linux).
4. Verify installation:
   ```bash
   conda --version
   python --version
   ```

---

### 3. Rasa NLU Library

**Rasa** is an open-source machine learning framework for building AI-powered chatbots and voice assistants. Rasa NLU handles **Natural Language Understanding** — it interprets user messages to detect intents and extract entities.

- **Documentation:** [https://rasa.com/docs/rasa/](https://rasa.com/docs/rasa/)

**Why it's needed:** Rasa NLU is the core engine of this chatbot. It processes user input, classifies the intent (e.g., "ask for a motivational quote"), and enables the bot to respond intelligently.

**Installation** (inside your virtual environment):
```bash
# Upgrade pip first
pip install --upgrade pip

# Install Rasa
pip install rasa

# Verify installation
rasa --version
```

**Initialize the project:**
```bash
rasa init
```
This creates the foundational project structure including `data/nlu.yml`, `config.yml`, `domain.yml`, and more.

---

### 4. Text Data

Text data refers to the **raw quote content** and **user utterances** that the chatbot will use. This includes:

- **Quote collections** categorized by themes such as motivation, love, success, happiness, etc.
- **User message examples** that represent how users might interact with the chatbot (e.g., *"I'm feeling sad"*, *"Give me a motivational quote"*).

**Why it's needed:** The chatbot needs a rich set of text data to understand user requests and to have a pool of quotes to recommend. The quality and variety of this data directly impacts how well the chatbot performs.

**Where it's stored:** Text data is typically stored in:
- `data/nlu.yml` — User training examples
- Custom data files — Quote collections (JSON/CSV/YAML format)

---

### 5. Training Data Format

Rasa uses **YAML format** for all training data. The training data defines **intents** (what the user wants) and **examples** (how they might say it).

**Why it's needed:** Properly formatted training data is essential for Rasa NLU to learn and accurately classify user intents. The more diverse and well-structured your examples, the better the chatbot performs.

**Example — `data/nlu.yml`:**
```yaml
version: "3.1"
nlu:
  - intent: ask_motivation
    examples: |
      - give me a motivational quote
      - i need some motivation
      - inspire me
      - share something motivational

  - intent: ask_love_quote
    examples: |
      - tell me a love quote
      - i want to hear about love
      - share a romantic quote

  - intent: greet
    examples: |
      - hello
      - hi
      - hey there
      - good morning
```

---

### 6. NLU Pipeline Configuration

The NLU pipeline defines **how user messages are processed** step-by-step — from raw text to classified intent. This is configured in `config.yml`.

**Why it's needed:** The pipeline determines the accuracy and behavior of the chatbot's language understanding. Each component in the pipeline handles a specific part of the NLU process (tokenization, featurization, classification).

**Example — `config.yml`:**
```yaml
language: en
pipeline:
  - name: WhitespaceTokenizer       # Splits text into words
  - name: RegexFeaturizer           # Detects patterns using regex
  - name: LexicalSyntacticFeaturizer # Adds word-level features
  - name: CountVectorsFeaturizer    # Converts text to numerical vectors
  - name: DIETClassifier            # Classifies intent & extracts entities
    epochs: 100
```

**Pipeline Components Explained:**

| Component | Role |
|---|---|
| `WhitespaceTokenizer` | Splits user messages into individual tokens (words) |
| `RegexFeaturizer` | Creates features based on regex patterns for entity extraction |
| `LexicalSyntacticFeaturizer` | Adds lexical and syntactic features (POS tags, word shapes) |
| `CountVectorsFeaturizer` | Transforms text into bag-of-words numerical representation |
| `DIETClassifier` | Multi-task model that classifies intents and extracts entities |

> 💡 You can customize the pipeline based on your project's complexity and requirements.

---

### 7. Development Environment (Visual Studio Code or similar IDE)

A good code editor or IDE is essential for writing, editing, and debugging the chatbot's code and configuration files.

**Recommended:** [Visual Studio Code (VS Code)](https://code.visualstudio.com/)

**Why it's needed:** An IDE provides syntax highlighting, error detection, integrated terminal, and extensions that make development faster and easier.

**Useful VS Code Extensions for this project:**
- **Python** — Python language support, IntelliSense, and debugging
- **YAML** — Syntax highlighting for Rasa's YAML configuration files
- **Rasa** — Autocomplete and validation for Rasa files (if available)
- **GitLens** — Enhanced Git integration for version control

**Other IDE options:**
- PyCharm
- Sublime Text
- Jupyter Notebook (for experimentation)

---

## 📁 Quick Start

```bash
# 1. Create and activate environment
conda create --name rasa_env python=3.9 -y
conda activate rasa_env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize project
rasa init

# 4. Train the model
rasa train

# 5. Talk to your chatbot
rasa shell
```

---

## 📄 Files

| File | Description |
|---|---|
| `Prerequisites.txt` | List of all prerequisites (downloadable) |
| `requirements.txt` | Python dependencies for pip install |
| `README.md` | This documentation file |

---

**Note:** Ensure all prerequisites are set up before moving forward with the project activities.
