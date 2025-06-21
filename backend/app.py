from flask import Flask, request, jsonify, send_file, make_response
from compress_utilities import HuffFile, CompressionError
import os
import time
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app, expose_headers=[
    'X-Compression-Ratio',
    'X-Original-Size',
    'X-Compressed-Size',
    'X-Decompressed-Size',
    'X-Time-Taken',
    'Content-Disposition'
])

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if filename.endswith('.huff'):
        return jsonify({'error': 'This file is already compressed.'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    huff = HuffFile()

    try:
        start = time.time()
        compressed_dir = huff.compress_file(filepath)
        end = time.time()
        compressed_filename = filename + '.huff'
        compressed_path = os.path.join(compressed_dir, compressed_filename)
        original_size = os.path.getsize(filepath)
        compressed_size = os.path.getsize(compressed_path)
    except CompressionError as e:
        return jsonify({'error': str(e)}), 500

    response = make_response(send_file(compressed_path, as_attachment=True,
                                       download_name=compressed_filename,
                                       mimetype='application/octet-stream'))
    response.headers['Content-Disposition'] = f'attachment; filename="{compressed_filename}"'
    response.headers['X-Compression-Ratio'] = str(round(original_size / compressed_size, 2))
    response.headers['X-Original-Size'] = str(original_size)
    response.headers['X-Compressed-Size'] = str(compressed_size)
    response.headers['X-Time-Taken'] = str(round(end - start, 2))

    return response

@app.route('/decompress', methods=['POST'])
def decompress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if not filename.endswith('.huff'):
        return jsonify({'error': 'This file is not a .huff compressed file.'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    huff = HuffFile()

    try:
        start = time.time()
        decompressed_path = huff.decompress_file(filepath)
        end = time.time()
        decompressed_filename = os.path.basename(decompressed_path)
        size = os.path.getsize(decompressed_path)
    except CompressionError as e:
        return jsonify({'error': str(e)}), 500

    response = make_response(send_file(decompressed_path, as_attachment=True,
                                       download_name=decompressed_filename,
                                       mimetype='application/octet-stream'))
    response.headers['Content-Disposition'] = f'attachment; filename="{decompressed_filename}"'
    response.headers['X-Decompressed-Size'] = str(size)
    response.headers['X-Time-Taken'] = str(round(end - start, 2))

    return response

if __name__ == '__main__':
    app.run(debug=True)
