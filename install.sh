#!/bin/bash

echo "📦 Cloning repo..."

#Качаем
REPO_URL="https://github.com/Shadowdays387/uptime-monitor.git"

if [ -d "uptime-monitor" ]; then
    echo "📁 Repo already exists, pulling latest changes..."
    cd uptime-monitor
    git pull
else
    git clone $REPO_URL
    cd uptime-monitor
fi

echo "🐍 Setting up environment..."

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Starting monitor..."

python main.py
