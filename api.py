# Backend API for EasyOCR
# Lightweight API-only version for GCP Cloud Run

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import easyocr
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Allow all origins for Vercel frontend

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "EasyOCR API"})

@app.route('/api/extract', methods=['POST'])
def extract_text():
    """Extract text from uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image_file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        # Extract text using EasyOCR
        results = reader.readtext(tmp_path)
        extracted_text = '\n'.join([text[1] for text in results])
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return jsonify({
            "success": True,
            "text": extracted_text,
            "word_count": len(extracted_text.split())
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/extract-pdf', methods=['POST'])
def extract_and_generate_pdf():
    """Extract text and return as PDF"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image_file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        # Extract text
        results = reader.readtext(tmp_path)
        extracted_text = '\n'.join([text[1] for text in results])
        
        # Generate PDF
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        # Write text to PDF
        y = 750
        for line in extracted_text.split('\n'):
            if y < 50:  # New page if needed
                c.showPage()
                y = 750
            c.drawString(50, y, line[:80])  # Limit line length
            y -= 20
        
        c.save()
        pdf_buffer.seek(0)
        
        # Clean up
        os.unlink(tmp_path)
        
        # Return PDF as base64 for easy handling
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            "success": True,
            "text": extracted_text,
            "pdf": pdf_base64
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
