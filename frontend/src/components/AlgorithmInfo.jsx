import React from 'react';

export default function AlgorithmInfo() {
  return (
    <div className="bg-white p-6 mt-8 rounded shadow-md max-w-2xl mx-auto text-left">
      <h2 className="text-xl font-bold mb-4">Supported Algorithms</h2>
      <p className="mb-2"><strong>Huffman Coding:</strong> A lossless algorithm that encodes frequently occurring symbols with shorter codes based on their frequency.</p>
      <p className="mb-2"><strong>Run-Length Encoding (RLE):</strong> A simple compression method that replaces sequences of repeated characters with a single character and count.</p>
      <p><strong>LZ77:</strong> Uses sliding window compression by replacing repeated sequences with references to earlier occurrences.</p>
    </div>
  );
}
