# Recruitment Platform

Plateforme de recrutement développée avec **Django** : les recruteurs publient des offres d'emploi, les candidats postulent avec CV et lettre de motivation, et une messagerie intégrée permet l'échange entre les deux parties.

## Fonctionnalités

**Comptes**
- Deux types de profils distincts : **Candidat** et **Recruteur** (un utilisateur ne peut pas être les deux à la fois)
- Inscription / connexion séparées par rôle
- Profil candidat : compétences, expérience, formation, photo de profil
- Profil recruteur : nom et description de l'entreprise, logo

**Offres d'emploi**
- Publication d'offres par les recruteurs (type de contrat, localisation, salaire, date limite)
- Liste des offres actives, avec exclusion automatique des offres déjà postulées pour un candidat connecté

**Candidatures**
- Candidature à une offre avec upload de CV et lettre de motivation
- Suivi de statut : en attente, examinée, entretien, acceptée, rejetée
- Un candidat ne peut postuler qu'une fois par offre

**Messagerie**
- Messages entre candidat et recruteur, liés ou non à une candidature
- Fils de discussion (réponses), statut lu/non lu

**Tableau de bord**
- App dédiée (`apps/dashboard`), actuellement au stade initial

## Stack technique

- **Django 5.2**
- **SQLite** (base de développement)
- **django-crispy-forms** + **crispy-bootstrap5** — mise en forme des formulaires
- **django-debug-toolbar** — débogage en développement
- Internationalisation activée (`locale/fr`)

## Prérequis

- Python 3.13
- pip

## Installation

```bash
git clone https://github.com/AlahyaneYassine/recruitment_platform.git
cd recruitment_platform
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
pip install django-debug-toolbar  # dépendance utilisée mais absente de requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Puis ouvrir `http://127.0.0.1:8000`.

## Structure du projet

```
recruitment_platform/
├── cand/                  # Configuration du projet Django (settings, urls, wsgi/asgi)
├── apps/
│   ├── accounts/          # Utilisateurs, profils candidat/recruteur
│   ├── jobs/               # Offres d'emploi
│   ├── applications/       # Candidatures (CV, lettre de motivation, statut)
│   ├── messaging/          # Messagerie candidat ↔ recruteur
│   └── dashboard/          # Tableau de bord (en cours de développement)
├── templates/              # Templates globaux
├── media/                  # Fichiers uploadés (CV, photos...) — non versionné
└── requirements.txt
```

## Pistes d'amélioration

- `SECRET_KEY` et les identifiants email sont actuellement en dur dans `settings.py` — à externaliser via des variables d'environnement (`django-environ` ou `python-decouple`) avant tout déploiement, et à régénérer.
- `django-debug-toolbar` est utilisé dans `settings.py` mais absent de `requirements.txt`.
- `DEBUG = True` et `ALLOWED_HOSTS = []` : à adapter avant toute mise en production.
- Le dossier `media/` (fichiers uploadés par les utilisateurs) et `db.sqlite3` ne doivent jamais être versionnés — voir `.gitignore`.
- L'app `dashboard` n'a pas encore de logique implémentée.

## Auteur

**Yassine Alahyane**
Cybersecurity Engineering Student
