// components/SymbolSelector.js
import React from "react";

export default function SymbolSelector({ symbol, setSymbol }) {
  return (
    <div className="space-y-1">
      <label className="block text-sm font-medium text-gray-400">Symbol</label>
      <select
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        className="w-full px-3 py-2 bg-gray-800 text-white rounded-lg border border-gray-700"
      >
        <option>BTC/USDT</option>
        <option>ETH/USDT</option>
        <option>BNB/USDT</option>
        <option>SOL/USDT</option>
        <option>ADA/USDT</option>
      </select>
    </div>
  );
}
