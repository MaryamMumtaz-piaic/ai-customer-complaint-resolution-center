import os
import fitz # PyMuPDF
import docx
import pandas as pd
import csv

def process_file(file_path: str, file_type: str) -> str:
    \"\"\"Extract text from various file formats.\"\"\"
    if not os.path.exists(file_path):
        return ""
    
    text = ""
    file_type = file_type.lower()
    
    try:
        if file_type == 'pdf':
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
        elif file_type == 'docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_type in ['txt', 'md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file_type == 'csv':
            try:
                df = pd.read_csv(file_path)
                text = df.to_string(index=False)
            except:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        text += " ".join(row) + "\n"
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        
    return text.strip()
