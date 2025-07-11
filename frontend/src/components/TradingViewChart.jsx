import React, { useEffect } from "react";

export default function TradingViewChart({ symbol , timeframe }) {
  useEffect(() => {
    const existingScript = document.getElementById("tv-script");
    if (existingScript) existingScript.remove();

    const script = document.createElement("script");
    script.id = "tv-script";
    script.src = "https://s3.tradingview.com/tv.js";
    script.async = true;
    script.onload = () => {
      if (window.TradingView) {
        new window.TradingView.widget({
          autosize: true,
          symbol: symbol.replace("/", ""),
          interval: timeframe.replace("m","").replace("h","").replace("d",""),
          timezone: "Asia/Kolkata",
          theme: "dark",
          style: "1",
          locale: "en",
          toolbar_bg: "#1e293b",
          enable_publishing: false,
          allow_symbol_change: false,
          container_id: "tradingview_chart_container",
        });
      }
    };
    document.body.appendChild(script);
  }, [symbol, timeframe]);

  return (
    <div className="bg-gray-900 rounded-xl p-4 shadow-lg">
      <div
        id="tradingview_chart_container"
        className="w-full h-screen"
      ></div>
    </div>
  );
}
