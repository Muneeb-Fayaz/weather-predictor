"""Weather predictor core: fetch history from Open-Meteo (no API key) and forecast
the next days with a simple linear-regression + seasonal-smoothing model.
Falls back to synthetic demo data if the network is unavailable."""
import json
import math
import random
import urllib.parse
import urllib.request
from datetime import date, timedelta

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_URL = "https://api.open-meteo.com/v1/forecast"


def _get(url, params, timeout=8):
    full = f"{url}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(full, timeout=timeout) as r:
        return json.loads(r.read().decode())


def geocode(city):
    data = _get(GEO_URL, {"name": city, "count": 1})
    if not data.get("results"):
        raise ValueError(f"City not found: {city}")
    r = data["results"][0]
    return r["name"], r.get("country", ""), r["latitude"], r["longitude"]


def fetch_history(lat, lon, days=30):
    data = _get(ARCHIVE_URL, {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "past_days": days, "forecast_days": 4, "timezone": "auto",
    })
    d = data["daily"]
    rows = list(zip(d["time"], d["temperature_2m_max"], d["temperature_2m_min"]))
    return rows  # last 4 rows are Open-Meteo's own forecast (for comparison)


def synthetic_history(days=30):
    random.seed(18)
    today = date.today()
    rows = []
    for i in range(days + 4):
        dt = today - timedelta(days=days - i)
        base = 26 + 4 * math.sin(i / 6)
        rows.append((dt.isoformat(), round(base + 5 + random.uniform(-1.5, 1.5), 1),
                     round(base - 5 + random.uniform(-1.5, 1.5), 1)))
    return rows


def linreg(ys):
    n = len(ys)
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs) or 1
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den
    return slope, my - slope * mx


def predict(history, horizon=3):
    """Blend linear trend with a 7-day moving average (damped trend)."""
    maxs = [r[1] for r in history]
    mins = [r[2] for r in history]
    out = []
    last = date.fromisoformat(history[-1][0])
    for label, series in (("max", maxs), ("min", mins)):
        slope, icpt = linreg(series)
        ma = sum(series[-7:]) / 7
        preds = []
        for h in range(1, horizon + 1):
            trend = slope * (len(series) - 1 + h) + icpt
            preds.append(round(0.4 * trend + 0.6 * ma, 1))
        out.append(preds)
    return [
        {"date": (last + timedelta(days=h + 1)).isoformat(), "max": out[0][h], "min": out[1][h]}
        for h in range(horizon)
    ]


def run(city, horizon=3):
    try:
        name, country, lat, lon = geocode(city)
        rows = fetch_history(lat, lon)
        source = "live"
    except Exception:
        name, country, source = city.title(), "", "demo"
        rows = synthetic_history()
    today = date.today().isoformat()
    past = [r for r in rows if r[0] < today]
    official = [r for r in rows if r[0] >= today]
    return {
        "city": name, "country": country, "source": source,
        "history": [{"date": r[0], "max": r[1], "min": r[2]} for r in past[-14:]],
        "prediction": predict(past, horizon),
        "official_forecast": [{"date": r[0], "max": r[1], "min": r[2]} for r in official],
    }


if __name__ == "__main__":
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else "Jammu"), indent=2))
