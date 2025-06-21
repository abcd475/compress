import React from 'react';

export default function CompressionStats({ stats }) {
  return (
    <div className="bg-gray-50 p-4 mt-4 rounded shadow text-left max-w-xl mx-auto">
      <h2 className="text-xl font-semibold mb-2">Compression Statistics</h2>
      <ul className="list-disc pl-5 space-y-1">
        {stats.compressionRatio && <li>Compression Ratio: {stats.compressionRatio}</li>}
        {stats.originalSize && <li>Original Size: {stats.originalSize} bytes</li>}
        {stats.compressedSize && <li>Compressed Size: {stats.compressedSize} bytes</li>}
        {stats.decompressedSize && <li>Decompressed Size: {stats.decompressedSize} bytes</li>}
        {stats.timeTaken && <li>Time Taken: {stats.timeTaken} seconds</li>}
      </ul>
    </div>
  );
}
