import React, { useState } from "react";
import axios from "axios";

export default function PaperTradingControls({ isPaperTrading, setIsPaperTrading }) {
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const startTrading = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/start_paper_trading", {
        symbol: "BTC/USDT",  // You can dynamically fetch from parent if needed
        timeframe: "1m",
        model_type: "ml",
        binance_api_key: apiKey,
        binance_api_secret: apiSecret,
      });
      setIsPaperTrading(true);
      setStatus(res.data.status);
    } catch (e) {
      setStatus("Failed to start");
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg space-y-4">
      <h3 className="text-lg font-semibold text-green-300">🔐 Paper Trading Config</h3>
      <input
        type="text"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="Binance API Key"
        className="w-full px-4 py-2 rounded bg-gray-900 text-white border border-gray-600"
      />
      <input
        type="password"
        value={apiSecret}
        onChange={(e) => setApiSecret(e.target.value)}
        placeholder="Binance API Secret"
        className="w-full px-4 py-2 rounded bg-gray-900 text-white border border-gray-600"
      />
      <button
        onClick={startTrading}
        disabled={loading}
        className="bg-green-500 hover:bg-green-600 text-black font-bold py-2 px-4 rounded w-full"
      >
        {loading ? "Starting..." : "🚀 Start Paper Trading"}
      </button>
      {status && <p className="text-sm text-gray-300">{status}</p>}
    </div>
  );
}
