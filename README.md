# 🧠 Streamlit SpaCy NER App

A powerful and user-friendly web app built with **Streamlit** and **SpaCy** to perform **Named Entity Recognition (NER)** on customer queries.

This app is created as part of **Task 2: Extracting Key Information (NER)** — to help AI assistants quickly identify key entities (like product names, order numbers, dates, people, companies, and locations) from user queries.

---

## 🚀 Features

- 🖊️ **Text Input Box** – Enter any customer query to analyze
- 🤖 **Named Entity Extraction** – Detects entities using SpaCy's `en_core_web_sm` model
- 🌈 **Colorful displaCy Visualization** – Highlights entities inline in the text
- 📋 **Entities Table** – Clean tabular view of all entities and their labels
- 🔎 **Entity Filter** – Filter entities by their type (PERSON, ORG, GPE, PRODUCT, etc.)
- 💾 **Download Entities CSV** – Export all detected entities as a CSV file
- 🕘 **History Panel** – View previously analyzed queries and their results
- 🧹 **Clear Chat** – Clear the entire history in one click
- ✨ **New Chat** – Start a completely fresh analysis
- ⚡ **Fast Performance** – Uses in-memory session state for quick switching between queries

---

## 💡 Why This App is Useful

- ⚡ **Saves time** by instantly extracting key information from long customer queries  
- 📑 **Helps AI assistants** understand user intent by finding important entities  
- 📊 **Improves productivity** by allowing CSV export of extracted entities  
- 💻 **Easy-to-use interface** suitable for both technical and non-technical users  
- 🌐 **Can be used by customer support teams, analysts, or chatbot developers**

---

## 🖥️ How to Use

1. Type your query in the **"Enter Text"** box  
2. Click the **Analyze** button  
3. See:
   - Colorful entity highlights using **displaCy**
   - A detailed **Entities Table** with all extracted items
4. Use:
   - **History panel** to load past queries
   - **Clear Chat / New Chat** buttons to start fresh
   - **Download CSV** button to save results

---

## ⚙️ Installation

```bash
# Clone this repo
git clone https://github.com/<your-username>/Streamlit_SpaCy_NER_App.git

cd Streamlit_SpaCy_NER_App

# Install dependencies
pip install -r requirements.txt

# Download SpaCy model
python -m spacy download en_core_web_sm

# Run the app
streamlit run app.py
