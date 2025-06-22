# Stage 1 - builder
FROM python:3.10-slim-buster as builder

WORKDIR /install

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install_packages -r requirements.txt

# Stage 2 - runner
FROM python:3.10-slim-buster

WORKDIR /app

# Copy entire app directory and installed packages
COPY --from=builder /install_packages /usr/local
COPY . .

ENV PORT=8080

EXPOSE 8080

HEALTHCHECK CMD curl -f http://localhost:8080 || exit 1

CMD ["streamlit", "run", "home.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]