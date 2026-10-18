## 👉 [**🔴 LIVE DEMO — CLICK HERE TO TRY IT NOW**](https://muneeb-fayaz.github.io/weather-predictor/) 👈

https://muneeb-fayaz.github.io/weather-predictor/

---

# 🌦️ WEATHER PREDICTOR — STOP SCROLLING, YOUR FORECAST IS HERE! ⚡

### Type a city. Get tomorrow's weather. In under 10 seconds. No API key. No signup. No nonsense.

> **Will it be scorching? Will you need a jacket? Don't guess. PREDICT.** 🔥❄️

---

## 🚀 WHY YOU'LL LOVE IT

| 💥 Feature | 🎯 What you get |
|---|---|
| **Zero setup** | Pure Python. No `pip install`. Nothing. |
| **Live data** | Real temperatures from the free Open-Meteo API |
| **Smart prediction** | Linear trend + 7-day moving average, blended |
| **Beautiful UI** | Dark, clean, chart included |
| **Works offline** | No internet? It switches to demo data automatically |
| **Sanity check** | See our prediction side by side with the official forecast |

---

## ⚡ START IN 3 STEPS

```bash
# 1️⃣ Go to the folder
cd weather-predictor

# 2️⃣ Launch it
python server.py

# 3️⃣ Open your browser
http://localhost:8000
```

**That's it. You're a weather forecaster now.** 🎉

---

## 🔌 THE API (yes, there's an API!)

```
GET /api/predict?city=Jammu&days=3
```

**Try it:**
```bash
curl "http://localhost:8000/api/predict?city=Delhi&days=5"
```

**You get back:** the last 14 days of history, your predicted highs and lows, and the official forecast for comparison.

| Parameter | Meaning | Default |
|---|---|---|
| `city` | Any city in the world | `Jammu` |
| `days` | Days to predict (1–7) | `3` |

---

## 🐍 USE THE PREDICTOR FROM PYTHON

```bash
python predictor.py Srinagar
```

```python
import predictor
print(predictor.run("Mumbai", horizon=3))
```

---

## 📁 WHAT'S IN THE BOX

```
weather-predictor/
├── 🐍 predictor.py        ← the brain (fetch + predict)
├── 🌐 server.py           ← the API + web server
├── 🎨 static/index.html   ← the UI
├── 🔐 .env.example        ← credentials template
└── 📖 README.md           ← you are here
```

---

## 🧠 HOW THE PREDICTION WORKS

1. 📥 Fetch the last 30 days of highs and lows for your city
2. 📈 Fit a straight-line trend through them
3. 📊 Compute the 7-day moving average
4. 🎯 Blend: **40% trend + 60% moving average**

Simple. Fast. Honest. It's a demo model, not a replacement for a meteorological service. 😉

---

## 🔐 CREDENTIALS

This project **needs no API key** (Open-Meteo is free). If you add a keyed service later:

```bash
cp .env.example .env
# edit .env, then NEVER commit it
```

---

## 🛠️ MAKE IT YOURS

- Swap in a better model (Prophet, scikit-learn)
- Add rain, humidity, wind
- Deploy to Render, Railway or any VPS
- Change the port: `PORT=9000 python server.py`

---

## ⭐ LIKED IT? SHARE IT. BUILD ON IT. SHIP IT.

**Made with ☀️ and Python.**
