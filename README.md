# OCR Text Extraction Pipeline

This project is a Python-based tool that extracts text from a variety of document formats — including:

- PDF files (both text-based and scanned/image-based)
- Word documents (.docx)
- Images (.png, .jpg, .tiff, etc.)

It automatically determines the appropriate method for text extraction — using standard parsing when possible and falling back to OCR (Tesseract) for image-based content.

---

## 🔧 How It Works

- Uses `pdfminer.six` to extract text from searchable PDFs
- Falls back to OCR (via `pdf2image` + `pytesseract`) for scanned/image-only PDFs
- Extracts text from `.docx` Word documents using `python-docx`
- OCRs image files directly using `pytesseract`
- Supports both **single files** and **batch processing** of folders

---

##  Quick Start

### 1. Install Dependencies

In your Codespace or terminal:

```bash
pip install -r requirements.txt