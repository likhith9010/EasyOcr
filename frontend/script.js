// Configuration - UPDATE THIS AFTER DEPLOYING BACKEND
const API_URL = 'YOUR_GCP_CLOUD_RUN_URL'; // e.g., 'https://easyocr-api-xxxxx-uc.a.run.app'

// Elements
const imageInput = document.getElementById('imageInput');
const uploadArea = document.getElementById('uploadArea');
const preview = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const extractBtn = document.getElementById('extractBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const extractedText = document.getElementById('extractedText');
const copyBtn = document.getElementById('copyBtn');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');

let selectedFile = null;
let pdfData = null;

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File input change
imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Handle file selection
function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        preview.style.display = 'block';
        extractBtn.style.display = 'block';
        result.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Extract text
extractBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    if (API_URL === 'YOUR_GCP_CLOUD_RUN_URL') {
        alert('Please update the API_URL in script.js with your GCP Cloud Run URL');
        return;
    }
    
    // Show loading
    loading.style.display = 'block';
    extractBtn.style.display = 'none';
    result.style.display = 'none';
    
    try {
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        const response = await fetch(`${API_URL}/api/extract-pdf`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to process image');
        }
        
        const data = await response.json();
        
        if (data.success) {
            extractedText.value = data.text;
            pdfData = data.pdf;
            result.style.display = 'block';
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        loading.style.display = 'none';
        extractBtn.style.display = 'block';
    }
});

// Copy text
copyBtn.addEventListener('click', () => {
    extractedText.select();
    document.execCommand('copy');
    
    const originalText = copyBtn.textContent;
    copyBtn.textContent = '✓ Copied!';
    setTimeout(() => {
        copyBtn.textContent = originalText;
    }, 2000);
});

// Download PDF
downloadPdfBtn.addEventListener('click', () => {
    if (!pdfData) {
        alert('No PDF data available');
        return;
    }
    
    const binary = atob(pdfData);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    
    const blob = new Blob([bytes], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'extracted-text.pdf';
    a.click();
    URL.revokeObjectURL(url);
});
