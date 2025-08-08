#!/bin/bash

echo "Setting up your Ticket Analysis system..."

python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from .env.example. Please update it with your API key and dataset path."
else
    echo "No .env.example found or .env already exists."
fi

echo "Setup complete!"
echo "Now run the app with: streamlit run app.py"

streamlit run app.py