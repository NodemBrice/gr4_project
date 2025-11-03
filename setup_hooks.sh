#!/bin/bash

echo "🚀 Installation du système d'analyse STRICT..."

# Python
echo "📦 Installation outils Python..."
pip install --upgrade pip
pip install google-generativeai python-dotenv requests
pip install pylint mypy pre-commit

# Node.js
echo "📦 Installation outils Node.js..."
npm install -g eslint htmlhint

# Pre-commit
echo "🔧 Configuration pre-commit..."
pre-commit install
pre-commit autoupdate

# Fichiers de config
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Configure ton .env avec tes clés !"
fi

# Test
echo "✅ Installation terminée !"
echo "🧪 Test de la configuration..."
pre-commit run --all-files || echo "⚠️ Des erreurs ont été détectées"

echo ""
echo "📝 Prochaines étapes :"
echo "1. Configure .env avec GEMINI_API_KEY"
echo "2. Configure les secrets GitHub"
echo "3. Teste avec: git commit -m 'test'"
