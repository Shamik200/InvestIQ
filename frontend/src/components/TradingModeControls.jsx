import React, { useState } from "react";

export default function TradingModeControls({ isPaperTrading, setIsPaperTrading, setIsLiveTrading }) {
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");

  const handleLiveTradingStart = () => {
    if (!apiKey || !apiSecret) {
      alert("Please enter both API Key and Secret to start live trading.");
      return;
    }
    setIsPaperTrading(false);
    setIsLiveTrading(true);
    // You can pass these to backend here
  };

  const handlePaperTradingStart = () => {
    setIsPaperTrading(true);
    setIsLiveTrading(false);
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 space-y-4 shadow-lg">
      <h2 className="text-lg font-semibold text-white text-center">🚀 Select Trading Mode</h2>
      <div className="flex flex-col md:flex-row justify-center items-center gap-4">
        <button
          onClick={handlePaperTradingStart}
          className={`px-6 py-2 rounded-lg font-medium text-sm ${
            isPaperTrading ? "bg-green-500 text-white" : "bg-gray-700 hover:bg-gray-600"
          }`}
        >
          🧪 Paper Trading
        </button>

        <div className="flex flex-col gap-2">
          <input
            type="text"
            placeholder="Binance API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="bg-gray-900 border border-gray-700 px-4 py-2 rounded-md text-white text-sm"
          />
          <input
            type="password"
            placeholder="Binance API Secret"
            value={apiSecret}
            onChange={(e) => setApiSecret(e.target.value)}
            className="bg-gray-900 border border-gray-700 px-4 py-2 rounded-md text-white text-sm"
          />
          <button
            onClick={handleLiveTradingStart}
            className="bg-red-600 text-white px-6 py-2 rounded-lg font-medium text-sm hover:bg-red-700"
          >
            ⚡ Start Live Trading
          </button>
        </div>
      </div>
    </div>
  );
}
