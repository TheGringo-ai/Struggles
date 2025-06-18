# Stage 1 - builder
FROM python:3.10-slim-buster as builder

WORKDIR /install

COPY ../requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install_packages -r requirements.txt

# Stage 2 - runner
FROM python:3.10-slim-buster

WORKDIR /app

COPY --from=builder /install_packages /usr/local
COPY app/ /app/

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/_stcore/health || exit 1

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0