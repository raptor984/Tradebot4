FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "crypto_trailing_stop_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]