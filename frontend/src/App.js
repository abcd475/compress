import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import CompressionStats from './components/CompressionStats';
import AlgorithmInfo from './components/AlgorithmInfo';

function App() {
  const [result, setResult] = useState(null);
  const [stats, setStats] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-center">
      <h1 className="text-4xl font-bold mb-6 text-blue-700">Data Compression & Decompression Portal</h1>
      <FileUploader setResult={setResult} setStats={setStats} />
      {stats && <CompressionStats stats={stats} />}
      {result && (
        <div className="mt-4">
          <a
            href={URL.createObjectURL(result)}
            download
            className="text-blue-500 underline"
          >
            Download Processed File
          </a>
        </div>
      )}
      <AlgorithmInfo />
    </div>
  );
}

export default App;
