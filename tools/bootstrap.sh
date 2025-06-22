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

# Set local Python version
echo "📌 Setting local Python version to $PYTHON_VERSION..."
pyenv local "$PYTHON_VERSION"

# Init pyenv shims
eval "$(pyenv init -)"
PYENV_PYTHON="$(pyenv which python)"

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
  echo "🐍 Creating virtual environment..."
  "$PYENV_PYTHON" -m venv .venv
else
  echo "✅ .venv already exists"
fi

# Activate and install packages
echo "📦 Installing packages..."
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "⚠️ No requirements.txt found!"
fi

# Create .env file if missing
if [ ! -f .env ]; then
  echo "🧪 Generating .env file from example..."
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "✅ .env file created from .env.example"
  else
    echo "⚠️ .env.example not found, creating default .env"
    cat <<EOF > .env
OPENAI_API_KEY=
GOOGLE_API_KEY=
GCP_PROJECT_ID=
GEMINI_API_KEY=
HUGGINGFACE_TOKEN=
EOF
    echo "✅ .env file created with placeholder values"
  fi
else
  echo "✅ .env already exists"
fi

echo "✅ Environment ready."
echo "➡️ To activate manually: source .venv/bin/activate"

# Optional: auto-run dev server
echo "🚀 Run 'make run' now? (y/n): \c"
read run_now
if [ "$run_now" = "y" ]; then
  make run
fi