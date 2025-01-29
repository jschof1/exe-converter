import os
from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# Use a writable directory
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.exe'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        try:
            result = subprocess.run(
                ['wine', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=1000  # Set a timeout for the process
            )
            return jsonify({
                "output": result.stdout,
                "error": result.stderr
            })
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Execution timed out"}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
