import React from "react";

export default function ModelSelector({ model, setModel }) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-400">Model Type</label>
      <select className="w-full px-3 py-2 bg-gray-800 text-white rounded-lg border border-gray-700" value={model} onChange={(e) => setModel(e.target.value)}>
        <option value="ml">ML (XGBoost, LGBM, RF)</option>
        <option value="rl">RL (Coming Soon)</option>
      </select>
    </div>
  );
}
