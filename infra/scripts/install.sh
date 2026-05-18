#!/bin/bash
set -e

echo "J.A.R.V.I.S. Installation Script"
echo "================================="

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required. Please install Python 3.12 or higher."
    exit 1
fi

if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your settings."
fi

echo ""
echo "Installation complete."
echo "Run 'python main.py' to start J.A.R.V.I.S."