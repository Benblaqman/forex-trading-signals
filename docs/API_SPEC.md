# API Specification

## Base URL
```
https://api.forexsignals.co.ke/api/v1
```

## Authentication
All authenticated endpoints require a JWT bearer token:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. Get Latest Signal

**Endpoint:** `GET /signal`

**Query Parameters:**
- `pair` (string, required): Currency pair (e.g., "EUR/USD")
- `timeframe` (string, optional): Timeframe (1m, 5m, 15m, 1h, 4h, 1d) - default: 1h

**Response:**
```json
{
  "signal": "BUY",
  "confidence": 87.5,
  "stoploss": 1.0850,
  "takeprofit": 1.1050,
  "rationale": "BUY signal: RSI + MACD + BB aligned. RSI at 28.5, strong trend (ADX: 32.2)",
  "timestamp": "2024-06-19T14:30:00Z",
  "indicator_votes": {
    "RSI": "BUY",
    "MACD": "BUY",
    "BB": "BUY",
    "ADX": "BUY",
    "Stochastic": "SELL"
  }
}
```

**Example Request:**
```bash
curl -X GET "https://api.forexsignals.co.ke/api/v1/signal?pair=EUR/USD&timeframe=1h" \
  -H "Authorization: Bearer your_token_here"
```

---

### 2. Get Signal History

**Endpoint:** `GET /signals`

**Query Parameters:**
- `pair` (string, required): Currency pair
- `limit` (integer, optional): Number of signals to return (default: 50, max: 500)
- `offset` (integer, optional): Pagination offset (default: 0)
- `start_date` (string, optional): ISO 8601 format (e.g., "2024-06-01T00:00:00Z")
- `end_date` (string, optional): ISO 8601 format

**Response:**
```json
{
  "data": [
    {
      "signal": "BUY",
      "confidence": 85.0,
      "stoploss": 1.0855,
      "takeprofit": 1.1055,
      "timestamp": "2024-06-19T14:00:00Z"
    },
    {
      "signal": "SELL",
      "confidence": 92.0,
      "stoploss": 1.1045,
      "takeprofit": 1.0745,
      "timestamp": "2024-06-19T13:00:00Z"
    }
  ],
  "total": 245,
  "limit": 50,
  "offset": 0
}
```

---

### 3. Get Backtesting Report

**Endpoint:** `GET /backtest`

**Query Parameters:**
- `start_date` (string, required): ISO 8601 format
- `end_date` (string, required): ISO 8601 format
- `pair` (string, optional): Currency pair (default: EUR/USD)
- `timeframe` (string, optional): Timeframe (default: 1h)

**Response:**
```json
{
  "period": "2024-01-01 to 2024-06-19",
  "total_signals": 245,
  "winning_trades": 178,
  "losing_trades": 67,
  "win_rate": 0.727,
  "avg_profit_per_trade": 0.0043,
  "total_profit": 1.0535,
  "max_consecutive_wins": 12,
  "max_consecutive_losses": 4,
  "max_drawdown": 0.051,
  "sharpe_ratio": 1.45,
  "sortino_ratio": 1.89,
  "roi_percent": 105.35
}
```

---

### 4. User Registration

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "phone": "+254712345678"
}
```

**Response:**
```json
{
  "user_id": "uuid-12345",
  "email": "user@example.com",
  "full_name": "John Doe",
  "subscription_tier": "free",
  "created_at": "2024-06-19T12:00:00Z"
}
```

---

### 5. User Login

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

---

### 6. Get User Profile

**Endpoint:** `GET /user/profile`

**Response:**
```json
{
  "user_id": "uuid-12345",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+254712345678",
  "subscription_tier": "pro",
  "subscription_expires_at": "2024-07-19T12:00:00Z",
  "created_at": "2024-06-19T12:00:00Z"
}
```

---

### 7. Initiate M-Pesa Payment

**Endpoint:** `POST /payments/mpesa/initiate`

**Request Body:**
```json
{
  "phone_number": "+254712345678",
  "tier": "pro",
  "amount": 500
}
```

**Response:**
```json
{
  "payment_request_id": "uuid-67890",
  "status": "pending",
  "amount": 500,
  "currency": "KES",
  "message": "STK push sent. Enter M-Pesa PIN on your phone.",
  "created_at": "2024-06-19T14:30:00Z"
}
```

---

### 8. Get Payment Status

**Endpoint:** `GET /payments/{payment_request_id}`

**Response:**
```json
{
  "payment_request_id": "uuid-67890",
  "status": "completed",
  "amount": 500,
  "tier_activated": "pro",
  "subscription_expires_at": "2024-07-19T14:30:00Z",
  "transaction_id": "MPESA_TRANS_12345"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "details": "pair parameter is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "details": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "details": "Your subscription does not include this feature"
}
```

### 429 Rate Limit
```json
{
  "error": "Too Many Requests",
  "details": "Rate limit exceeded. Try again in 60 seconds."
}
```

### 500 Server Error
```json
{
  "error": "Internal Server Error",
  "details": "An unexpected error occurred. Please try again later."
}
```

---

## Rate Limiting

- **Free tier**: 10 requests/minute
- **Pro tier**: 100 requests/minute
- **Elite tier**: 500 requests/minute

---

## Webhook Events

### Payment Completed Webhook

**Event:** `payment.completed`

**Payload:**
```json
{
  "event": "payment.completed",
  "payment_request_id": "uuid-67890",
  "user_id": "uuid-12345",
  "amount": 500,
  "tier": "pro",
  "subscription_expires_at": "2024-07-19T14:30:00Z",
  "timestamp": "2024-06-19T14:35:00Z"
}
```

**Webhook URL:** Set in your dashboard settings
