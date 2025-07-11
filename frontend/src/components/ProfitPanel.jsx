import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ProfitPanel() {
  const [profit, setProfit] = useState(0);

  useEffect(() => {
    const fetchProfit = async () => {
      try {
        const res = await axios.get("http://localhost:8000/total_profit");
        setProfit(res.data.total_profit);
      } catch (err) {
        console.error("Profit fetch error", err);
      }
    };

    fetchProfit();
    const interval = setInterval(fetchProfit, 5000); // update every 5s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-800 rounded-lg p-4 flex flex-col justify-center items-center">
      <h2 className="text-lg font-semibold mb-2 text-center">📈 Net Profit</h2>
      <span className={`text-2xl font-bold ${profit >= 0 ? "text-green-400" : "text-red-400"}`}>
        ${profit}
      </span>
    </div>
  );
}
