# 🛡️ Multilingual Spam Shield

Detect spam and scam messages in **English, Hindi and Telugu** using an N-gram model and cross-lingual processing.

**Live app:** https://multilingual-spam-shield.streamlit.app

---

## About

Paste an SMS, call transcript, email, chat message or link. The app finds the language, turns the text into word patterns, and shows how risky the message is.

## Features

- Detects spam and scams in English, Hindi and Telugu
- Works on 5 message types: SMS, Call, Email, Chat and Link
- Maps words from different languages to one shared concept token
- Uses single words, word pairs and word triples (N-grams)
- Built-in example messages to try quickly

## How it works

1. **Language detection:** the app identifies the language of the message.
2. **Shared tokens:** words with the same meaning in different languages are mapped to one shared concept token.
3. **N-grams:** single words, word pairs and word triples are taken from the shared tokens.
4. **Risk score:** the message is scored against patterns learned from spam and safe messages.

## Run on your computer

**Easiest way (Windows):** double-click `run.bat`. It installs Streamlit if needed and starts the app.

**Or use the terminal:**

```bash
pip install -r requirements.txt
streamlit run app.py
```

Your browser opens `http://localhost:8501`. Stop the app with `Ctrl+C`.

## Project files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit page (user interface) |
| `spam_model.py` | Language detection, tokenising, n-grams, training and scoring |
| `Lingua data.py` | Training and test messages |
| `requirements.txt` | Python packages needed |
| `run.bat` | One-click start for Windows |

## Built with

- Python
- Streamlit

## Author

Made by **farheen2101**ss