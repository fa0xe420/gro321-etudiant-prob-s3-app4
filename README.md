# GRO321 - Système de Gestion de Maintenance Assistée par Ordinateur (GMAO)

## Description

Application de gestion de maintenance pour robots de service utilisant Python et
SQLite. Le projet fournit la gestion des robots et de leurs clients, ainsi qu'un
début de fonctionnalité pour les bons de travail à compléter.

## Installation

```bash
uv sync
```

## Initialisation de la base de données

```bash
uv run init-db
```

## Serveur web

```bash
uv run gro321-server
```

Le serveur écoute ensuite sur http://127.0.0.1:18000.
Vous pouvez changer le port dans la fonction main de web/app.py.

## Structure

```
gro321/
├── src/gro321/
│   ├── models/         # Classes des entités (Client, Robot, BonTravail)
│   ├── database/       # Accès aux données et schémas
│   └── web/            # Application web
├── scripts/            # Scripts d'initialisation
└── data/               # Fichiers de données (généré)
```

## Exigences

- Python 3.12+
- SQLite3 (inclus dans Python)
- Bibliothèque standard uniquement

## Pistes pour la problématique

Commencez par analyser la structure gérant l'inventaire (entités Client et Robot).
Cette partie est entièrement fonctionnelle et peut servir de modèle pour les bons de travail.

Vous n'avez rien à modifier dans le dossier web/, l'application se charge d'appeler les bonnes
fonctions dans les modules crud_*.py du dossier database.
De cette façon, on isole la manipulation des données de l'interface utilisateur.

La majorité du travail devrait se retrouver dans bon_travail.py et crud_bons.py, en plus des
ajustements que vous aurez à apporter au modèle et données initiales dans les deux fichiers
donnees_depart.sql et schema_depart.sql.

Le script init_db permet d'initialiser l'ensemble des données depuis les fichiers SQL.
Il est donc préférable de travailler dans ceux-ci plutôt que de tenter des manipulations
manuelles au schéma. 
Si vous pensez avoir trop modifié le modèle avec des manipulations manuelles, n'hésitez-pas à supprimer le fichier data/gro321.db, le script pourra le recréer sans difficultés.
