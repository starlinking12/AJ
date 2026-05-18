#!/bin/bash
set -e

echo "Downloading J.A.R.V.I.S. models..."
echo "=================================="

MODEL_DIR="voice_pipeline/stt/models"
mkdir -p "$MODEL_DIR"

echo "STT models will be downloaded automatically by faster-whisper on first use."
echo "Run the system once to trigger model downloads."

TTS_DIR="voice_pipeline/tts/models"
mkdir -p "$TTS_DIR"

echo ""
echo "For Piper TTS voice models, download from:"
echo "https://huggingface.co/rhasspy/piper-voices"
echo "Place the .onnx and .json files in: $TTS_DIR"

echo ""
echo "Model download guide complete."