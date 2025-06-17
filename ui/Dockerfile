FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]