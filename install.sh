#!/bin/bash

set -e

# чтобы apt не задавал интерактивные вопросы
export DEBIAN_FRONTEND=noninteractive

# ссылка на репозиторий ()
REPO_URL="https://github.com/nkrylosov/uptime-monitor.git"

# папка проекта
PROJECT_DIR="uptime-monitor"

echo "📦 Установка системных зависимостей..."

# ставим python, pip, venv и git
sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv git

echo "📁 Подготовка проекта..."

# если папка уже есть — обновляем
if [ -d "$PROJECT_DIR" ]; then
    echo "🔄 Репозиторий уже есть, обновляем..."
    cd $PROJECT_DIR
    git pull
else
    echo "⬇️ Скачиваем репозиторий..."
    git clone $REPO_URL
    cd $PROJECT_DIR
fi

echo "🐍 Настройка виртуального окружения..."

# пересоздаём окружение, чтобы не было старого мусора
rm -rf venv

python3 -m venv venv
source venv/bin/activate

echo "📦 Установка Python-зависимостей..."

pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Запуск мониторинга..."

python main.py
