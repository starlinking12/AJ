#!/bin/bash
set -e

echo "Setting up Ollama for J.A.R.V.I.S."
echo "=================================="

if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed. Installing now..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

echo "Starting Ollama server..."
ollama serve &
sleep 3

echo "Pulling recommended models..."
ollama pull llama3.2:3b
ollama pull llama3.2:8b
ollama pull mistral:7b

echo ""
echo "Ollama setup complete."
echo "Available models:"
ollama list