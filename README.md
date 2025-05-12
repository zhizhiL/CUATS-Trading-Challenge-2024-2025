# CUATS-challenge-2024

### 📈 Dynamically-Weighted Momentum Asset Allocation Strategy

This repository contains the implementation of a dynamically-weighted momentum-based asset allocation strategy developed for the CUATS 2025 Coding Challenge by Team KPZ Trading.


🚀 Strategy Overview

The strategy identifies and allocates capital to top-performing assets using Rate of Change (ROC) as a momentum signal. It dynamically adjusts portfolio weights based on relative strength and market regime:

    Long/Short Allocation: Up to 80% long and 20% short, adjusted based on SPY's relative momentum.

    Monthly Rebalancing to reflect the most recent momentum trends.

    Stop-Loss Protection for short positions to manage upside risk.

    Asset Universe: A diversified mix of ETFs, tech stocks, consumer staples, utilities, and commodities.

📊 Performance Highlights (Jan 2020 – Present)

Based on backtests (see CUATS_Challenge_KPZtrading.pdf):

    Sharpe Ratio: 1.12

    CAGR: 42.76%

    Max Drawdown: 34.8%

    Alpha: 0.216

🧠 Core Features

    Top momentum assets selected based on short-term ROC (3-day period).

    Portfolio weights are proportional to normalized momentum scores.

    Short positions taken on lowest momentum assets when market conditions warrant.

    Built with QuantConnect Lean Engine.

📁 Files

    MomentumAssetAllocationStrategy.py: Core algorithm implementation.

    CUATS_Challenge_KPZtrading.pdf: Slides detailing strategy design, parameter tuning, and results.

📌 Requirements

    QuantConnect environment or Lean CLI to run the backtest

    Python 3.x
