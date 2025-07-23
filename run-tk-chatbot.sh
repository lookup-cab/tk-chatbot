#!/bin/bash

# Start the Ollama process
ollama run gemma3:12b &

# Wait for the Ollama process to start
sleep 0  # Adjust this sleep time if needed, based on Ollama's startup time

# Activate the Python virtual environment
source "tk-chatbot-venv/bin/activate"

# Run the main Python script

python3 client.py

# Optional: Clean up the virtual environment after the script finishes
ollama stop gemma3:12b
deactivate
exit
