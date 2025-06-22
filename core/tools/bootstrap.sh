#!/bin/bash

# Set the Python version you want to use
PYTHON_VERSION="3.11.9"

echo "🔍 Checking pyenv..."
if ! command -v pyenv &>/dev/null; then
  echo "❌ pyenv is not installed. Please install it first (brew install pyenv)."
  exit 1
fi

# Install Python version if missing
if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
  echo "⬇️ Installing Python $PYTHON_VERSION..."
  pyenv install "$PYTHON_VERSION"
fi

# Set it for this folder
echo "📌 Setting local Python version to $PYTHON_VERSION..."
pyenv local "$PYTHON_VERSION"

# Use pyenv's shimmed python
eval "$(pyenv init -)"
PYENV_PYTHON="$(pyenv which python)"

# Create .venv if not exists
if [ -d ".venv" ]; then
  echo "🧹 Removing existing .venv..."
  rm -rf .venv
else
  echo "No existing .venv found — starting fresh."
fi

# Create new virtual environment
echo "🐍 Creating virtual environment..."
"$PYENV_PYTHON" -m venv .venv

# Activate and install packages
echo "📦 Installing packages..."
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

# Optional: install project requirements
if [ -f "requirements.txt" ]; then
  echo "📄 Installing requirements.txt packages..."
  pip install -r requirements.txt
fi

echo "✅ Environment ready. To activate later: source .venv/bin/activate"