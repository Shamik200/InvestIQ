import React, { useEffect, useState } from "react";
import axios from "axios";

export default function TradeLogTable() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get("http://localhost:8000/trades")
        .then(res => setLogs(res.data))
        .catch(err => console.error("Trade fetch error:", err));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-900 p-4 rounded-lg shadow-lg mt-6 text-white" style={{ height: '400px' }}>
      <h2 className="text-xl font-bold text-green-400 mb-4">📈 Trade Log</h2>
      {logs.length === 0 ? (
        <p className="text-gray-400">No trades yet...</p>
      ) : (
        <div className="overflow-y-auto border border-gray-700 rounded" style={{ height: '320px' }}>
          <table className="w-full text-sm text-left">
            <thead className="text-gray-400 border-b border-gray-700 sticky top-0 bg-gray-900 z-10">
              <tr>
                <th className="py-2 px-3">Time</th>
                <th className="py-2 px-3">Symbol</th>
                <th className="py-2 px-3">Entry</th>
                <th className="py-2 px-3">Exit</th>
                <th className="py-2 px-3">PnL</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((trade, idx) => (
                <tr key={idx} className="border-b border-gray-800 hover:bg-gray-800">
                  <td className="py-2 px-3">{new Date(trade.timestamp).toLocaleString()}</td>
                  <td className="py-2 px-3 text-yellow-300">{trade.symbol}</td>
                  <td className="py-2 px-3 text-green-400">${trade.entry.toFixed(2)}</td>
                  <td className="py-2 px-3 text-red-400">${trade.exit.toFixed(2)}</td>
                  <td className={`py-2 px-3 ${trade.pnl >= 0 ? "text-green-300" : "text-red-300"}`}>
                    {trade.pnl.toFixed(2)}
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