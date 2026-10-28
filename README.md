# Multilingual Spam Shield (Streamlit version)

Detects spam/scam messages in English, Hindi and Telugu with an N-Gram model
and cross-lingual (shared concept token) processing.

## Run on your computer
1. Install Python 3.9 or newer (https://www.python.org/downloads/ - tick "Add Python to PATH").
2. Open a terminal in this folder.
3. (Optional) create a virtual environment:
       python -m venv venv
       venv\Scripts\activate          (Windows)
       source venv/bin/activate       (Mac/Linux)
4. Install Streamlit:
       pip install -r requirements.txt
5. Start the app:
       streamlit run app.py
   If "streamlit" is not recognised, use:
       python -m streamlit run app.py
6. Your browser opens http://localhost:8501

Stop the app with Ctrl+C in the terminal.
Light/dark theme: top-right menu (three dots) -> Settings -> Theme.

## Files
- app.py          Streamlit page (user interface)
- spam_model.py   language detection, tokenising, n-grams, training, scoring
- requirements.txt

## Easiest way (Windows)
Double-click run.bat. It installs Streamlit if needed and starts the app.
