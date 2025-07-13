import React, { useEffect, useState } from "react";
import axios from "axios";

export default function SignalViewer() {
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    const fetchSignals = () => {
      axios
        .get("https://investiq-frfe.onrender.com/signals")
        .then((res) => setSignals(res.data.reverse()))
        .catch((err) => console.error("Failed to load signals", err));
    };

    fetchSignals();
    const interval = setInterval(fetchSignals, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
  <div className="flex flex-col" style={{ height: '218px' }}> {/* 250px - 32px padding */}
    <h2 className="text-xl font-semibold mb-2 text-white flex-shrink-0">📈 Recent Signals</h2>

    {signals.length === 0 ? (
      <p className="text-gray-400">No signals yet.</p>
    ) : (
      <div className="flex-1 overflow-y-auto min-h-0">
        <table className="w-full text-sm text-left text-gray-300">
          <thead className="sticky top-0 bg-gray-900 text-gray-200 z-10">
            <tr>
              <th className="px-4 py-2 border-b border-gray-700">Type</th>
              <th className="px-4 py-2 border-b border-gray-700">Confidence</th>
              <th className="px-4 py-2 border-b border-gray-700">Time</th>
            </tr>
          </thead>
          <tbody>
            {signals.map((s, i) => (
              <tr
                key={i}
                className="hover:bg-gray-800 border-b border-gray-700 transition-colors"
              >
                <td className="px-4 py-2">
                  {s.signal === "BUY" ? "🟢 BUY" : "🔴 SELL"}
                </td>
                <td className="px-4 py-2">
                  {parseFloat(s.confidence * 100).toFixed(2)}%
                </td>
                <td className="px-4 py-2">
                  {new Date(s.timestamp).toLocaleTimeString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )}
  </div>
);
}
