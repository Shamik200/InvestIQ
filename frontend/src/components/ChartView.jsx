import React, { useEffect, useRef } from "react";
import {
  createChart,
  CandlestickSeries,
  createSeriesMarkers,
} from "lightweight-charts";

export default function ChartView({ symbol, timeframe }) {
  const containerRef = useRef(null);
  const chartRef = useRef(null);
  const seriesRef = useRef(null);
  const markersApiRef = useRef(null);
  const markers = useRef([]);

  useEffect(() => {
    const cleanedTimeframe = timeframe.replace(/[mhd]/g, "");
    const interval = `${symbol.toLowerCase()}@kline_${cleanedTimeframe}m`;
    const container = containerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      width: container.clientWidth,
      height: 600,
      layout: {
        background: { color: "#0f172a" },
        textColor: "#cbd5e1",
      },
      grid: {
        vertLines: { color: "#1e293b" },
        horzLines: { color: "#1e293b" },
      },
      priceScale: { borderColor: "#334155" },
      timeScale: { borderColor: "#334155", timeVisible: true },
    });

    chartRef.current = chart;
    const series = chart.addSeries(CandlestickSeries, {});
    seriesRef.current = series;
    const markersApi = createSeriesMarkers(series);
    markersApiRef.current = markersApi;

    // WebSocket live stream from Binance
    const socket = new WebSocket(
      `wss://stream.binance.com:9443/ws/${interval}`
    );

    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      const k = msg.k;
      const candle = {
        time: Math.floor(k.t / 1000),
        open: parseFloat(k.o),
        high: parseFloat(k.h),
        low: parseFloat(k.l),
        close: parseFloat(k.c),
      };

      series.update(candle);

      // Example dummy conditions for entry/exit (replace with real logic)
      if (parseFloat(k.c) > parseFloat(k.o) * 1.01) {
        markers.current.push({
          time: candle.time,
          position: "belowBar",
          color: "green",
          shape: "arrowUp",
          text: "BUY",
        });
      } else if (parseFloat(k.c) < parseFloat(k.o) * 0.99) {
        markers.current.push({
          time: candle.time,
          position: "aboveBar",
          color: "red",
          shape: "arrowDown",
          text: "SELL",
        });
      }

      markersApi.setMarkers(markers.current);
    };

    return () => {
      socket.close();
      chart.remove();
      chartRef.current = null;
      seriesRef.current = null;
      markersApiRef.current = null;
    };
  }, [symbol, timeframe]);

  return <div style={{ width: "100%", height: "600px" }} ref={containerRef} />;
}
