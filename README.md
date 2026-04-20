# aug25cds_variabilite
Projet Data Science d'analyse et de prédiction de la variabilité de la production solaire à partir de données ouvertes de la région PACA.

## Ajout des données locales

### Environnement python du projet

1. Après avoir cloné le repo du projet, aller dans 'data' et créer un répertoire 'local_data' :

```js
aug25cds_variabilite
|-f README.md
|-f requirements.txt
|-d notebooks
|-d reports
|-d src
|-d data
   |-d local_data
```

2. Dans ce répertoire, on va créer l'environnement du projet. Par exemple 'variabilite_env' :

```js
python3.10 -m venv variabilite_env
```

3. Activer l'environnement :

```js
source variabilite_env/bin/activate
```

4. Revenir à la racine du projet :
```js
cd ../..
```

5. Installer les biliothèques requises par le projet :

```js
pip install -r requirements.txt
```

6. Lier l'environnement python activé à Jupyter notebook :

```js
python3 -m ipykernel install --user --name=variabilite_env
```

### Données à télécharger préalablement


