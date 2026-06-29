#!/bin/bash
# Script pour initialiser la base de données avec le schéma de départ

echo "Initialisation de la base de données (schéma de départ)..."
uv run init-db

echo "Base de données prête!"
echo "Pour lancer le serveur: uv run gro321-server"
