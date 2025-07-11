import React, { useEffect, useState } from "react";
import axios from "axios";
import ModelSelector from "./components/ModelSelector";
import TimeFrameSelector from "./components/TimeFrameSelector";
import SignalViewer from "./components/SignalViewer";
import TradingViewChart from "./components/TradingViewChart";
import TradingConfigForm from "./components/TradingConfigForm";
import SymbolSelector from "./components/SymbolSelector";
import ProfitPanel from "./components/ProfitPanel";
import TradeLogTable from "./components/TradeLogTable";
import LightweightChart from "./components/ChartView";

export default function App() {
  const [model, setModel] = useState("ml");
  const [symbol, setSymbol] = useState("BTC/USDT");
  const [timeframe, setTimeframe] = useState("1m");
  const [signalData, setSignalData] = useState({ signal: null, confidence: 0 });
  const [chartData, setChartData] = useState([]);
  const [isPaperTrading, setIsPaperTrading] = useState(false);
  const [isLiveTrading, setIsLiveTrading] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(false);

const togglePaperTrading = async () => {
  if (!isPaperTrading) {
    await axios.post("http://localhost:8000/start", {
      symbol: "BTC/USDT",
      timeframe: "1m"
    });
  } else {
    await axios.post("http://localhost:8000/stop");
  }

  setIsPaperTrading(!isPaperTrading);
};


  // const fetchPrediction = async () => {
  //   try {
  //     const res = await axios.post("http://localhost:8000/predict", {
  //       model_type: model,
  //       symbol,
  //       timeframe,
  //     });
  //     setSignalData(res.data);
  //   } catch (e) {
  //     console.error("Prediction Error", e);
  //   }
  // };

  const fetchChart = async () => {
    try {
      const res = await axios.get("http://localhost:8000/chart", {
        params: { symbol, timeframe },
      });
      setChartData(res.data);
    } catch (e) {
      console.error("Chart Error", e);
    }
  };

  const trainModel = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/train_model", {
        symbol,
        timeframe
      });
      // alert("Model training started: " + response.data.message);
    } catch (error) {
      console.error("Model training failed:", error);
      alert("Model training failed. Check backend logs.");
    }
    setLoading(false);
  };


  // useEffect(() => {
  //   fetchPrediction();
  //   fetchChart();
  //   const interval = setInterval(() => {
  //     fetchPrediction();
  //     fetchChart();
  //   }, 30000);
  //   return () => clearInterval(interval);
  // }, [model, timeframe, symbol]);

  useEffect(() => {
    fetchChart();
  }, []);

  const startLiveTrading = () => {
    if (!apiKey || !apiSecret) {
      alert("Please enter both API Key and Secret to start live trading.");
      return;
    }
    setIsLiveTrading(true);
    setIsPaperTrading(false);
  };

  const startPaperTrading = () => {
  setIsLiveTrading(false);
  setIsPaperTrading(true);

  axios.post("http://localhost:8000/start_paper_trading", {
    symbol: symbol,
    timeframe: timeframe
    // model_type: model
  })
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error("Error starting paper trading:", error);
  });
};

  return (
    <div className="min-h-screen bg-gradient-to-br from-black to-gray-900 text-white px-6 py-10">
      <div className="max-w-7xl mx-auto space-y-10">
        <header className="text-center">
          <h1 className="text-5xl font-extrabold text-green-400 mb-2">💹 AI Trading Dashboard</h1>
          <p className="text-sm text-gray-400">Live predictions • Strategy selector • Paper & Live trading</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ModelSelector model={model} setModel={setModel}  />
          <TimeFrameSelector timeframe={timeframe} setTimeframe={setTimeframe} />
          <SymbolSelector symbol={symbol} setSymbol={setSymbol}  />
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-gray-900 rounded-xl p-6 space-y-4 shadow-xl border border-green-400">
            <h2 className="text-lg font-semibold text-white text-center">🔴 Live Trading</h2>
            <input
              type="text"
              placeholder="Binance API Key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="bg-black border border-gray-700 px-4 py-2 w-full rounded-md text-white text-sm"
            />
            <input
              type="password"
              placeholder="Binance API Secret"
              value={apiSecret}
              onChange={(e) => setApiSecret(e.target.value)}
              className="bg-black border border-gray-700 px-4 py-2 w-full rounded-md text-white text-sm"
            />
            <button
              onClick={startLiveTrading}
              className="w-full bg-red-600 hover:bg-red-700 transition-colors text-white px-6 py-2 rounded-lg font-medium text-sm"
            >
              🔴 Start Live Trading
            </button>
          </div>

          <div className="bg-gray-900 rounded-xl p-6 space-y-4 shadow-xl border border-green-400 flex flex-col justify-center">
            <h2 className="text-lg font-semibold text-white text-center">⚙️ Train Model</h2>
            <button
              onClick={trainModel}
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-md flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading && (
                <svg
                  className="animate-spin h-4 w-4 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.372 0 0 5.372 0 12h4z"
                  ></path>
                </svg>
              )}
              {loading ? "Training..." : "Train Model"}
            </button>

            <h2 className="text-lg font-semibold text-white text-center">🧪 Paper Trading</h2>
            <button
              onClick={togglePaperTrading}
              className={`w-full px-6 py-3 rounded-lg font-semibold text-sm transition-colors duration-200 text-center shadow-md ${
                isPaperTrading ? "bg-red-500 text-white" : "bg-green-600 hover:bg-green-700"
              }`}
            >
              {isPaperTrading ? "🛑 Stop Paper Trading" : "🧪 Start Paper Trading"}
            </button>
          </div>
        </div>
        
        <div className="grid gap-6">
          <div className="w-full h-screen">
            {/* <LightweightChart symbol={symbol} timeframe={timeframe} /> */}
            <TradingViewChart symbol={symbol} timeframe={timeframe} />
          </div>

          <div className="w-full">
            <TradeLogTable />
          </div>
        </div>

        {/* <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-h-[100px] overflow-y-auto">
          <ProfitPanel />
          <SignalViewer signal={signalData.signal} confidence={signalData.confidence} showEmoji={true} />
        </div> */}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-900 rounded-xl p-4 max-h-[250px] shadow-lg overflow-hidden flex flex-col justify-center">
            <ProfitPanel />
          </div>

          <div className="bg-gray-900 rounded-xl p-4 max-h-[250px] shadow-lg overflow-hidden flex flex-col">
            <SignalViewer signal={signalData.signal} confidence={signalData.confidence} showEmoji={true}/>
          </div>
        </div>
      </div>
    </div>
  );
}
