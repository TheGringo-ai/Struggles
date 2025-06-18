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
All components are up to date.
➜  Struggles git:(main) ✗ gcloud beta run services logs tail agent-core-ui --region=us-central1
streaming logs from chatterfix-ui


EXPOSE 8080

HEALTHCHECK CMD curl -f http://localhost:8080 || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]