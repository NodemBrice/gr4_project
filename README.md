# GR4 Project: Système de Validation de Code Intelligent avec IA

## Description
Ce projet met en place un système automatisé pour valider le code poussé sur un dépôt Git. À chaque push :
- Le code est vérifié avec des outils comme mypy (typage strict), pylint (style/conventions), py_compile et pytest.
- Si des erreurs sont détectées, un rapport est généré.
- Le rapport est reformulé par une IA (OpenAI) en un message poli et personnalisé basé sur le profil du développeur (niveau : beginner, intermediate, advanced).
- Un email est envoyé au développeur avec les explications.
- Le push est bloqué si configuré via les protections de branches GitHub.

Le backend est en Flask pour gérer les profils (eleves) et notes (éventuellement pour logs de reviews). Le frontend est une simple page HTML/JS pour visualisation.

Objectif : Améliorer la qualité du code en équipe sans reviews manuelles.

## Prérequis
- Python 3.11+
- GitHub account pour Actions et Secrets
- Compte OpenAI pour l'API key
- Serveur SMTP (e.g., Gmail avec app password)

## Installation
1. Clone le repo :