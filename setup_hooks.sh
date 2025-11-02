#!/bin/bash

echo "🚀 Installation du hook IA Gemini..."

# Installation des dépendances Python
pip install google-generativeai python-dotenv requests pylint

# Installation des linters JS/HTML
npm install -g eslint htmlhint

# Installation de pre-commit
pip install pre-commit

# Configuration du hook
pre-commit install

# Copie du .env.example si .env n'existe pas
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Configure ton fichier .env avec tes clés API !"
fi

echo "✅ Installation terminée !"
echo "📝 N'oublie pas de configurer .env avec tes clés"
