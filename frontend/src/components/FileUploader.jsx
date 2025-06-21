import React, { useState } from 'react';
import axios from 'axios';

export default function FileUploader({ setResult, setStats }) {
  const [file, setFile] = useState(null);
  const [algorithm, setAlgorithm] = useState('huffman');
  const [action, setAction] = useState('compress');

  const handleSubmit = async () => {
    if (!file) return alert('Please select a file');

    const formData = new FormData();
    formData.append('file', file);

    const endpoint = action === 'compress' ? '/compress' : '/decompress';

    try {
      const response = await axios.post(`http://127.0.0.1:5000${endpoint}`, formData, {
        responseType: 'blob'
      });

      const headers = response.headers;
      const stats = {
        compressionRatio: headers['x-compression-ratio'],
        originalSize: headers['x-original-size'],
        compressedSize: headers['x-compressed-size'],
        decompressedSize: headers['x-decompressed-size'],
        timeTaken: headers['x-time-taken']
      };
      setStats(stats);

      // Extract filename from Content-Disposition header
      const contentDisposition = headers['content-disposition'];
      let filename = 'downloaded_file';
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="(.+)"/);
        if (match && match[1]) {
          filename = match[1];
        }
      }

      // Trigger download
      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();

      setResult(response.data);
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Something went wrong'));
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow-md max-w-xl mx-auto">
      <input type="file" onChange={e => setFile(e.target.files[0])} className="mb-4" />
      <div className="mb-4">
        <label className="mr-2">Algorithm:</label>
        <select onChange={e => setAlgorithm(e.target.value)} value={algorithm} className="border p-1">
          <option value="huffman">Huffman Coding</option>
          <option value="rle" disabled>RLE (Coming Soon)</option>
          <option value="lz77" disabled>LZ77 (Coming Soon)</option>
        </select>
      </div>
      <div className="mb-4">
        <button
          onClick={() => {
            setAction('compress');
            handleSubmit();
          }}
          className="bg-blue-500 text-white px-4 py-2 mr-2 rounded"
        >
          Compress
        </button>
        <button
          onClick={() => {
            setAction('decompress');
            handleSubmit();
          }}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Decompress
        </button>
      </div>
    </div>
  );
}
