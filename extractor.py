import fitz  # PyMuPDF
import re
import pytesseract
from PIL import Image
import io

# Point to Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Stop words for French, English, and common Arabic
STOP_WORDS = {
    # French
    'les', 'des', 'est', 'une', 'que', 'qui', 'dans', 'pour', 'sur',
    'avec', 'par', 'pas', 'plus', 'tout', 'mais', 'ont', 'son', 'ses',
    'cette', 'ces', 'aux', 'leur', 'leurs', 'comme', 'aussi', 'bien',
    'peut', 'dont', 'ainsi', 'selon', 'entre', 'très', 'fait', 'être',
    'avoir', 'faire', 'dit', 'lors', 'alors', 'donc', 'car', 'soit',
    # English
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
    'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
    'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two',
    'way', 'who', 'use', 'your', 'from', 'they', 'will', 'with',
    'this', 'that', 'have', 'been', 'were', 'said', 'each', 'which',
    'their', 'what', 'about', 'would', 'there', 'when', 'make',
    'like', 'into', 'than', 'time', 'could', 'other', 'some',
    # Numbers and single chars
    'un', 'le', 'la', 'et', 'en', 'du', 'de', 'au',
}

def is_scanned_pdf(doc):
    """Check if PDF is scanned (image-based) or text-based."""
    text_count = 0
    for page in doc:
        text = page.get_text().strip()
        if len(text) > 50:
            text_count += 1
    return text_count < len(doc) * 0.3  # less than 30% pages have text

def ocr_page(page):
    """Convert a PDF page to image and run OCR."""
    mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR quality
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    
    # Try French + English + Arabic
    try:
        text = pytesseract.image_to_string(img, lang='fra+eng+ara')
    except:
        try:
            text = pytesseract.image_to_string(img, lang='fra+eng')
        except:
            text = pytesseract.image_to_string(img)
    
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF — handles both text-based and scanned PDFs."""
    doc = fitz.open(pdf_path)
    full_text = ""
    
    scanned = is_scanned_pdf(doc)
    
    for page in doc:
        if scanned:
            text = ocr_page(page)
        else:
            text = page.get_text()
            # If page has very little text, try OCR on it
            if len(text.strip()) < 50:
                text = ocr_page(page)
        full_text += text + "\n"
    
    doc.close()
    return full_text

def detect_exam_sections(text):
    """Detect if PDF contains multiple exams and split them."""
    # Patterns that indicate a new exam starts
    exam_markers = [
        r'(?:Examen|Exam|Contrôle|Test|Devoir)\s+(?:N°|No|#)?\s*\d+',
        r'(?:Session|Année|Year)\s+\d{4}',
        r'\d{4}[-/]\d{4}',  # Academic year like 2023-2024
        r'(?:Semestre|Semester)\s+[12]',
        r'(?:Janvier|Février|Mars|Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre)\s+\d{4}',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
    ]
    
    sections = []
    current_section = ""
    lines = text.split('\n')
    
    for line in lines:
        is_marker = False
        for pattern in exam_markers:
            if re.search(pattern, line, re.IGNORECASE):
                if current_section.strip():
                    sections.append(current_section.strip())
                current_section = line + '\n'
                is_marker = True
                break
        
        if not is_marker:
            current_section += line + '\n'
    
    if current_section.strip():
        sections.append(current_section.strip())
    
    # If no markers found, treat entire text as one exam
    return sections if len(sections) > 1 else [text]

def extract_questions(text):
    """Extract individual questions from exam text."""
    patterns = [
        r'(?:Question|Q)[\s\.\)]+\d+',
        r'\d+[\.\)]\s+[A-Z]',
        r'(?:Exercise|Exercice)\s+\d+',
        r'(?:Partie|Part)\s+[IVX\d]+',
    ]
    
    questions = []
    lines = text.split('\n')
    current_question = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        is_new_question = False
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                is_new_question = True
                break
        
        if is_new_question:
            if current_question.strip():
                questions.append(current_question.strip())
            current_question = line
        else:
            current_question += " " + line
    
    if current_question.strip():
        questions.append(current_question.strip())
    
    questions = [q for q in questions if len(q) > 30]
    return questions

def clean_text(text):
    """Clean extracted text for analysis."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\?\!\:\;\-\(\)]', ' ', text)
    return text.strip()

def filter_topics(topics):
    """Remove stop words and noise from extracted topics."""
    filtered = []
    for topic in topics:
        words = topic.lower().split()
        # Skip if all words are stop words or too short
        meaningful_words = [w for w in words if w not in STOP_WORDS and len(w) > 3]
        if meaningful_words:
            filtered.append(topic)
    return filtered