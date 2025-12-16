# app.py
# Flask app to extract text using EasyOCR and download as PDF
# This is the main file for my EasyOcr app

import os
from flask import Flask, render_template, request, send_file
import easyocr
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(path)

    results = reader.readtext(path)
    extracted_text = '\n'.join([text[1] for text in results])

    # Save text to PDF
    pdf_path = os.path.join(UPLOAD_FOLDER, 'output.pdf')
    c = canvas.Canvas(pdf_path)
    for i, line in enumerate(extracted_text.split('\n')):
        c.drawString(50, 800 - (15 * i), line)
    c.save()

    return render_template('index.html', text=extracted_text, pdf_url='/download')

@app.route('/download')
def download():
    return send_file(os.path.join(UPLOAD_FOLDER, 'output.pdf'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)