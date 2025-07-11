import React from "react";

export default function TimeFrameSelector({ timeframe, setTimeframe }) {
  const options = ["1m", "5m", "15m", "1h", "4h", "1d"];
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-400">Timeframe</label>
      <select className="w-full px-3 py-2 bg-gray-800 text-white rounded-lg border border-gray-700" value={timeframe} onChange={(e) => setTimeframe(e.target.value)}>
        {options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
      </select>
    </div>
  );
}
