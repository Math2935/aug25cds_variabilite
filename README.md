# aug25cds_variabilite
Projet Data Science d'analyse et de prédiction de la variabilité de la production solaire à partir de données ouvertes de la région PACA.

## Ajout des données locales

### Environnement python du projet

Après avoir cloné le repo du projet, aller dans 'data' et créer un répertoire 'local_data' :

aug25cds_variabilite
|-f README.md
|-f requirements.txt
|-d notebooks
|-d reports
|-d src
|-d data
   |-d local_data

Dans ce répertoire, on va créer l'environnement du projet. Par exemple 'variabilite_env' :
    python3.10 -m venv variabilite_env

Activer l'environnement :
    source variabilite_env/bin/activate

Revenir à la racine du projet :
    cd ../..

Installer les biliothèques requises par le projet :
    pip install -r requirements.txt

Lier l'environnement python activé à Jupyter notebook :
    python3 -m ipykernel install --user --name=variabilite_env

### Données à télécharger préalablement


