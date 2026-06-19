"""Multi-indicator consensus signal engine."""

import pandas as pd
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

from .indicators import TechnicalIndicators


class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"


@dataclass
class Signal:
    """Signal output structure."""
    signal_type: SignalType
    confidence: float  # 0-100
    stoploss: float
    takeprofit: float
    rationale: str
    timestamp: str
    indicator_votes: Dict[str, str]  # Which indicators voted for what


class ConsensusEngine:
    """Generate signals based on multi-indicator consensus voting."""

    def __init__(
        self,
        rsi_oversold_threshold: float = 30,
        rsi_overbought_threshold: float = 70,
        confidence_threshold: float = 60,
    ):
        self.rsi_oversold = rsi_oversold_threshold
        self.rsi_overbought = rsi_overbought_threshold
        self.confidence_threshold = confidence_threshold

    def generate_signal(
        self,
        ohlcv_data: pd.DataFrame,
        pair: str = "EUR/USD",
        timeframe: str = "1h",
    ) -> Signal:
        """
        Generate a signal based on multi-indicator consensus.
        
        Args:
            ohlcv_data: DataFrame with columns [open, high, low, close, volume]
            pair: Currency pair (e.g., 'EUR/USD')
            timeframe: Timeframe (e.g., '1h', '4h')
            
        Returns:
            Signal object
        """
        indicator_votes = {}
        buy_votes = 0
        sell_votes = 0
        total_indicators = 0

        # === RSI Signal ===
        rsi = TechnicalIndicators.calculate_rsi(ohlcv_data["close"])
        latest_rsi = rsi.iloc[-1]
        
        if latest_rsi < self.rsi_oversold:
            indicator_votes["RSI"] = "BUY"
            buy_votes += 1
        elif latest_rsi > self.rsi_overbought:
            indicator_votes["RSI"] = "SELL"
            sell_votes += 1
        else:
            indicator_votes["RSI"] = "NEUTRAL"
        total_indicators += 1

        # === MACD Signal ===
        macd, signal_line, histogram = TechnicalIndicators.calculate_macd(ohlcv_data["close"])
        latest_macd = macd.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        latest_histogram = histogram.iloc[-1]
        
        if latest_macd > latest_signal and latest_histogram > 0:
            indicator_votes["MACD"] = "BUY"
            buy_votes += 1
        elif latest_macd < latest_signal and latest_histogram < 0:
            indicator_votes["MACD"] = "SELL"
            sell_votes += 1
        else:
            indicator_votes["MACD"] = "NEUTRAL"
        total_indicators += 1

        # === Bollinger Bands Signal ===
        upper, middle, lower = TechnicalIndicators.calculate_bollinger_bands(ohlcv_data["close"])
        latest_close = ohlcv_data["close"].iloc[-1]
        latest_upper = upper.iloc[-1]
        latest_lower = lower.iloc[-1]
        
        if latest_close < latest_lower:
            indicator_votes["BB"] = "BUY"
            buy_votes += 1
        elif latest_close > latest_upper:
            indicator_votes["BB"] = "SELL"
            sell_votes += 1
        else:
            indicator_votes["BB"] = "NEUTRAL"
        total_indicators += 1

        # === ADX Signal (Trend Strength) ===
        adx = TechnicalIndicators.calculate_adx(
            ohlcv_data["high"],
            ohlcv_data["low"],
            ohlcv_data["close"]
        )
        latest_adx = adx.iloc[-1]
        
        if latest_adx > 25:  # Strong trend
            if buy_votes > sell_votes:
                indicator_votes["ADX"] = "BUY"
                buy_votes += 1
            else:
                indicator_votes["ADX"] = "SELL"
                sell_votes += 1
        else:
            indicator_votes["ADX"] = "NEUTRAL"
        total_indicators += 1

        # === Stochastic Oscillator Signal ===
        k, d = TechnicalIndicators.calculate_stochastic(
            ohlcv_data["high"],
            ohlcv_data["low"],
            ohlcv_data["close"]
        )
        latest_k = k.iloc[-1]
        
        if latest_k < 20:
            indicator_votes["Stochastic"] = "BUY"
            buy_votes += 1
        elif latest_k > 80:
            indicator_votes["Stochastic"] = "SELL"
            sell_votes += 1
        else:
            indicator_votes["Stochastic"] = "NEUTRAL"
        total_indicators += 1

        # === Calculate Confidence ===
        if buy_votes + sell_votes == 0:
            confidence = 0
            signal_type = SignalType.NEUTRAL
        else:
            max_votes = max(buy_votes, sell_votes)
            confidence = (max_votes / total_indicators) * 100
            signal_type = SignalType.BUY if buy_votes > sell_votes else SignalType.SELL

        # === Risk Management: Calculate SL and TP ===
        atr = TechnicalIndicators.calculate_atr(
            ohlcv_data["high"],
            ohlcv_data["low"],
            ohlcv_data["close"]
        )
        latest_atr = atr.iloc[-1]
        
        if signal_type == SignalType.BUY:
            stoploss = latest_close - (latest_atr * 1.5)  # 1.5 ATR below entry
            takeprofit = latest_close + (latest_atr * 3.0)  # 1:2 risk-reward
        else:
            stoploss = latest_close + (latest_atr * 1.5)  # 1.5 ATR above entry
            takeprofit = latest_close - (latest_atr * 3.0)  # 1:2 risk-reward

        # === Build Rationale ===
        rationale = self._build_rationale(indicator_votes, latest_rsi, latest_adx)

        return Signal(
            signal_type=signal_type,
            confidence=round(confidence, 1),
            stoploss=round(stoploss, 5),
            takeprofit=round(takeprofit, 5),
            rationale=rationale,
            timestamp=pd.Timestamp.now().isoformat(),
            indicator_votes=indicator_votes,
        )

    def _build_rationale(self, votes: Dict, rsi: float, adx: float) -> str:
        """Build a human-readable rationale for the signal."""
        buy_indicators = [k for k, v in votes.items() if v == "BUY"]
        sell_indicators = [k for k, v in votes.items() if v == "SELL"]
        
        if buy_indicators:
            indicators_str = " + ".join(buy_indicators)
            trend = "strong" if adx > 25 else "weak"
            return f"BUY signal: {indicators_str} aligned. RSI at {rsi:.1f}, {trend} trend (ADX: {adx:.1f})"
        elif sell_indicators:
            indicators_str = " + ".join(sell_indicators)
            trend = "strong" if adx > 25 else "weak"
            return f"SELL signal: {indicators_str} aligned. RSI at {rsi:.1f}, {trend} trend (ADX: {adx:.1f})"
        else:
            return "No clear signal: Mixed indicator readings."
