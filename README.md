# ✦ ExamIQ — AI Exam Analyzer

> Upload your past exams. Get topic predictions and AI-generated practice questions.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?style=flat-square&logo=streamlit)
![Mistral AI](https://img.shields.io/badge/Mistral-AI-orange?style=flat-square)
![OCR](https://img.shields.io/badge/Tesseract-OCR-green?style=flat-square)

**[🌐 Live Demo](https://examiq.streamlit.app)**

---

## What is ExamIQ?

ExamIQ is an AI-powered exam preparation tool that helps students study smarter. Upload your past exam PDFs and the app automatically extracts topics, analyzes difficulty, predicts what's likely on your next exam, and generates practice questions in your professor's exact style.

---

## Features

- **Multi-format PDF support** — handles both text-based and scanned/photographed PDFs
- **Multilingual OCR** — reads French, Arabic, and English exam papers
- **Topic extraction** using TF-IDF + Mistral AI cleanup
- **Difficulty analysis** — classifies each question as Easy, Medium, or Hard
- **AI topic prediction** — predicts which topics are most likely on your next exam
- **Practice question generation** — generates questions matching your professor's style
- **Multi-exam analysis** — upload several past papers for better pattern detection
- **Progress bar** with real-time status during analysis

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web interface |
| PyMuPDF (fitz) | PDF text extraction |
| Tesseract OCR | Reading scanned/photographed PDFs |
| pytesseract | Python wrapper for Tesseract |
| scikit-learn | TF-IDF topic extraction |
| Mistral AI | Topic cleaning + question generation |
| python-dotenv | API key management |

---

## How It Works

1. User uploads past exam PDFs and enters the subject name
2. `extractor.py` reads each PDF — uses direct extraction for text PDFs, Tesseract OCR for scanned ones
3. `analyzer.py` runs TF-IDF to extract raw topics and classifies question difficulty
4. Mistral AI cleans the raw topics — removes verbs and noise, keeps only real academic topics
5. Results displayed: stats, topic pills, difficulty breakdown per exam
6. User clicks "Predict Likely Topics" → Mistral analyzes patterns and predicts next exam content
7. User clicks "Generate Practice Questions" → Mistral generates questions matching past exam style

---

## Supported Languages

| Language | Text PDF | Scanned PDF |
|----------|----------|-------------|
| French | ✅ | ✅ |
| Arabic | ✅ | ✅ |
| English | ✅ | ✅ |

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/justttleyla-bot/examiq.git
cd examiq

# Install Python dependencies
pip install -r requirements.txt

# Install Tesseract OCR (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install with French and Arabic language packs

# Create .env file
echo MISTRAL_API_KEY=your_key_here > .env

# Run the app
streamlit run app.py
```

---

## Project Structure
examiq/
├── app.py              # Streamlit web interface
├── extractor.py        # PDF reading + OCR + question extraction
├── analyzer.py         # TF-IDF topic extraction + difficulty classification
├── generator.py        # Mistral AI topic prediction + question generation
├── packages.txt        # Linux system packages for deployment
└── requirements.txt    # Python dependencies

---

## Deployment

Deployed on Streamlit Community Cloud. The `packages.txt` file installs Tesseract OCR on the Linux server:
tesseract-ocr
tesseract-ocr-fra
tesseract-ocr-ara
libgl1

Mistral API key stored securely in Streamlit Cloud Secrets.

---

## Author

**Leyla** — Data Science & Computer Science Student

[![GitHub](https://img.shields.io/badge/GitHub-justttleyla--bot-black?style=flat-square&logo=github)](https://github.com/justttleyla-bot)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=flat-square)](https://examiq.streamlit.app)
