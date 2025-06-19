# Application de Gestion de Boulangerie

Une application web Django pour gérer une boulangerie, permettant de suivre les ventes, les utilisateurs et les rôles.

## Fonctionnalités

- Gestion des utilisateurs et des rôles
- Suivi des achats en FCFA
- Tableau de bord avec statistiques
- Interface en français
- Design responsive avec Bootstrap 5

## Installation

1. Cloner le projet
```bash
git clone [URL_DU_REPO]
cd Boulangerie-APP
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer la base de données
```bash
python manage.py migrate
```

5. Créer un super utilisateur
```bash
python manage.py createsuperuser
```

6. Lancer le serveur
```bash
python manage.py runserver
```

## Technologies utilisées

- Django
- Bootstrap 5
- SQLite (développement) / PostgreSQL (production)
- Crispy Forms
- WhiteNoise (fichiers statiques)

## Déploiement

L'application est configurée pour être déployée sur Render.com. 