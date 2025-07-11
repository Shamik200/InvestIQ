import React, { useState, useEffect } from "react";

export default function TradingConfigForm({ model, symbol, timeframe }) {
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");

  const startTrading = async () => {
    try {
      await axios.post("http://localhost:8000/start_trading", {
        model_type: model,
        symbol,
        timeframe,
        mode: "paper",
        api_key: apiKey,
        api_secret: apiSecret
      });
      alert("Trading Started");
    } catch (err) {
      alert("Start Failed");
    }
  };

  return (
    <div className="space-y-3 bg-gray-800 p-4 rounded-lg shadow-md text-white">
      <input
        type="text"
        placeholder="Binance API Key"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        className="w-full p-2 rounded bg-gray-900 border border-gray-700"
      />
      <input
        type="text"
        placeholder="Binance Secret Key"
        value={apiSecret}
        onChange={(e) => setApiSecret(e.target.value)}
        className="w-full p-2 rounded bg-gray-900 border border-gray-700"
      />
      <button
        onClick={startTrading}
        className="w-full p-2 bg-green-600 rounded hover:bg-green-700"
      >
        🚀 Start Trading
      </button>
    </div>
  );
}
