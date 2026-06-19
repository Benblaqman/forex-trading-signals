# Forex Trading Signal App (EUR/USD)

**Advanced AI-powered trading signals for EUR/USD with high-confidence recommendations, risk management, and M-Pesa payments.**

## 🎯 Overview

A subscription-based SaaS platform that generates buy/sell signals for EUR/USD traders using:
- **Multi-indicator consensus** (RSI, MACD, Bollinger Bands, ADX, Stochastic, Ichimoku)
- **Machine Learning** (LSTM/Random Forest models)
- **Risk management** (Stop-loss, take-profit, position sizing)
- **Real-time alerts** (Web dashboard + mobile app)
- **M-Pesa payments** (Kenya-first monetization)

## 📊 Key Features

### Signal Engine
- ✅ Real-time EUR/USD price analysis
- ✅ Multi-timeframe analysis (1m, 5m, 15m, 1h, 4h, 1d)
- ✅ Confidence scoring (0-100%)
- ✅ Risk outputs (SL, TP, position size)
- ✅ Signal rationale (why BUY/SELL)

### Subscription Tiers
| **Tier** | **Price** | **Features** |
|---|---|---|
| **Free** | KES 0 | Basic signals, 1h/4h only |
| **Pro** | KES 500/mo | All timeframes + confidence + risk mgmt + backtesting |
| **Elite** | KES 1,500/mo | ML-enhanced signals + news sentiment + historical data |

### Platforms
- 🌐 **Web Dashboard** - Real-time charts, signal feed, performance tracking
- 📱 **Mobile App (Flutter)** - Push notifications, on-the-go trading
- 🔔 **Alerts** - SMS, email, in-app notifications

## 🏗️ Architecture

```
forex-trading-signals/
├── backend/
│   ├── data-fetcher/          # EUR/USD price ingestion
│   ├── signal-engine/         # Multi-indicator consensus
│   ├── ml-models/             # LSTM/Random Forest
│   ├── backtesting/           # Historical signal evaluation
│   ├── payment-processor/      # M-Pesa (Daraja API)
│   └── api-server/            # FastAPI/Express
├── frontend/
│   ├── web-dashboard/         # React/Vue + TradingView Charts
│   └── mobile-app/            # Flutter
├── devops/
│   ├── docker/
│   ├── ci-cd/                 # GitHub Actions
│   └── monitoring/            # Prometheus/Grafana
└── docs/
    ├── API_SPEC.md
    ├── DEPLOYMENT.md
    └── TRADING_RULES.md
```

## 🚀 MVP Timeline (4-6 weeks)

### Week 1-2: Backend Foundation
- Data fetcher (Alpha Vantage/Finnhub)
- Time-series database setup
- Signal engine core (RSI, MACD, Bollinger Bands)

### Week 2-3: Signal Intelligence
- Complete all 7 indicators
- Consensus voting system
- Confidence scoring
- Risk management calculations

### Week 3-4: ML & Backtesting
- LSTM model prototype
- Backtesting framework
- Performance evaluation (win rate, ROI)

### Week 4-5: Frontend & Payments
- Web dashboard with charts
- M-Pesa integration
- Subscription management

### Week 5-6: Mobile & DevOps
- Flutter mobile app
- CI/CD pipeline (GitHub Actions)
- Cloud deployment (DigitalOcean/AWS)
- Monitoring setup

## 🛠️ Tech Stack

- **Backend**: Python 3.10+ (FastAPI) or Node.js (Express)
- **Database**: PostgreSQL + TimescaleDB (time-series) or InfluxDB
- **ML**: TensorFlow/Keras (LSTM), scikit-learn (Random Forest)
- **Technical Analysis**: TA-Lib, pandas-ta
- **Charting**: TradingView Lightweight Charts, Chart.js
- **Mobile**: Flutter
- **Payments**: Daraja API (M-Pesa)
- **DevOps**: Docker, GitHub Actions, AWS/DigitalOcean

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Benblaqman/forex-trading-signals.git
cd forex-trading-signals

# Install dependencies (backend)
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (Alpha Vantage, Daraja, etc.)

# Run data fetcher
python -m backend.data_fetcher.main

# Run signal engine
python -m backend.signal_engine.main

# Run API server
python -m backend.api_server.main
```

## 📋 API Endpoints

### Get Latest Signal
```
GET /api/v1/signal?pair=EUR/USD&timeframe=1h
```

**Response:**
```json
{
  "signal": "BUY",
  "confidence": 87,
  "stoploss": 1.0850,
  "takeprofit": 1.1050,
  "rationale": "RSI oversold + MACD bullish crossover + Ichimoku support",
  "timestamp": "2024-06-19T14:30:00Z"
}
```

### Get Signal History
```
GET /api/v1/signals?pair=EUR/USD&limit=50
```

### Get Backtesting Report
```
GET /api/v1/backtest?start_date=2023-01-01&end_date=2024-06-19
```

**Response:**
```json
{
  "total_signals": 245,
  "winning_trades": 178,
  "win_rate": 0.727,
  "avg_profit_per_trade": 0.0043,
  "max_drawdown": 0.051,
  "sharpe_ratio": 1.45
}
```

## 💳 Payment Flow

1. User selects **Pro** tier → KES 500/month
2. Click **Pay with M-Pesa**
3. **Daraja API** sends STK Push to phone
4. User enters M-Pesa PIN
5. **Webhook callback** confirms payment
6. **Subscription activated** → Access all Pro signals

## ⚠️ Risk Disclaimer

**IMPORTANT**: Trading signals are for educational purposes only. They are not financial advice. Forex trading involves substantial risk of loss. Past performance does not guarantee future results. Always trade responsibly and consult a financial advisor before making investment decisions.

## 📊 Backtesting & Performance

We maintain a **public accuracy dashboard** showing:
- Win rate (last 7/30 days)
- Average profit per signal
- Maximum consecutive wins/losses
- Sharpe ratio and risk metrics

See [PERFORMANCE.md](./docs/PERFORMANCE.md) for historical data.

## 🔒 Security

- API authentication: JWT tokens
- M-Pesa webhook verification: HMAC-SHA256
- Database encryption: TLS/SSL
- No storage of payment card details (PCI-DSS compliant)

## 📞 Support

- **Email**: support@forexsignals.co.ke
- **WhatsApp**: +254 XXX XXX XXX
- **Telegram**: @ForexSignalsBot

## 📝 License

MIT License - See [LICENSE](./LICENSE)

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

---

**Status**: Pre-MVP Development  
**Next Milestone**: First beta signals (Week 2)  
**Target Launch**: 6 weeks from start
