import os
import sys
from pathlib import Path
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from docx import Document

TEXT_THRESHOLD = 30
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]

def extract_from_pdf(file_path):
    print(f"[INFO] PDF: {file_path}")
    text = extract_text(file_path).strip()
    if len(text) >= TEXT_THRESHOLD:
        return text
    else:
        return ocr_from_pdf(file_path)

def ocr_from_pdf(file_path):
    text = ""
    try:
        pages = convert_from_path(file_path, dpi=300)
        for i, page in enumerate(pages):
            print(f"[INFO] OCRing PDF page {i + 1}")
            text += pytesseract.image_to_string(page) + "\n"
    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
    return text.strip()

def extract_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"[ERROR] DOCX failed: {e}")
        return ""

def extract_from_image(file_path):
    try:
        return pytesseract.image_to_string(Image.open(file_path))
    except Exception as e:
        print(f"[ERROR] Image OCR failed: {e}")
        return ""

def extract_text_from_file(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_from_pdf(file_path)
    elif ext == ".docx":
        return extract_from_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return extract_from_image(file_path)
    else:
        print(f"[WARN] Unsupported file type: {ext}")
        return ""

def save_output(text, input_file):
    output_name = Path(input_file).stem + "_extracted.txt"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✅] Saved to: {output_name}")

def process_input(input_path):
    path = Path(input_path)
    if path.is_file():
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            text = extract_text_from_file(str(path))
            save_output(text, str(path))
        else:
            print(f"[WARN] Unsupported file: {path.name}")
    elif path.is_dir():
        files = list(path.glob("*"))
        for file in files:
            if file.suffix.lower() in SUPPORTED_EXTENSIONS:
                text = extract_text_from_file(str(file))
                save_output(text, str(file))
    else:
        print(f"[ERROR] Invalid path: {input_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_text.py <file_or_folder>")
        sys.exit(1)

    input_path = sys.argv[1]
    process_input(input_path)