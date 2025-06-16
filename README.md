# Crypto Trailing Stop Backtester

This project is a Streamlit web app for backtesting a simple crypto trading strategy:
- Buy any crypto that spikes more than X% in an hour
- Use a trailing stop of Y%

## 📈 Run Locally

1. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

2. Start the app:
    ```bash
    streamlit run crypto_trailing_stop_dashboard.py
    ```

## 🐳 Run with Docker

1. Build:
    ```bash
    docker build -t crypto-backtester .
    ```

2. Run:
    ```bash
    docker run -p 8501:8501 crypto-backtester
    ```

Then visit `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

- Push this repo to GitHub
- Go to https://streamlit.io/cloud
- Connect GitHub and deploy your app

Enjoy backtesting!