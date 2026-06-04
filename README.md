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

### Application Streamlit

1. Depuis la racine du projet, après avoir installé les dépendances requises décrites plus haut :
```
streamlit run src/app.py
```


### Données à télécharger préalablement

Pour pouvoir faire tourner les notebooks, il faut préalablement télécharger certains fichiers (trop volumineux pour être re-publiés sur Github).

Dans le dossier local_data que nous avons créé au point 1 de la mise en place de l'environnement python du projet, créer 3 nouveaux répertoires : 'input', 'temp' et 'output'.

```js
aug25cds_variabilite
|-f README.md
|-f requirements.txt
|-d notebooks
|-d reports
|-d src
|-d data
   |-d local_data
      |-d variabilite_env
      |-d input
      |-d temp
      |-d output
```

Comme leur nom le suggère :
 - le répertoire 'temp' contiendra les fichiers temporaires créés par les notebooks ;
 - le répertoire 'output' contiendra les résultats finaux des notebooks.
 
Dans le répertoire 'input', on placera :

1. les archives au format zip d'éCO2Mix telles qu'on peut les trouver sur le site de RTE (pour notre projet nous avons pris les données régionnales de la région PACA de 2013 à 2024 ainsi que l'archive de 2025 consolidée ('En-cours-Consolide')).

2. On placera également les 3 fichiers 'communes_PACA_INSEE.csv', 'registre_pv_paca_raw.csv' et 'region_paca.geojson' tels qu'on les retrouve sur le drive du projet.

3. Enfin on place également un fichier 'cams_access' qui est un fichier texte dont la première ligne correspond à la clé d'accès à l'API CAMS.

Contenu attendu du répertoire input :

```js
input :
   cams_access
   communes_PACA_INSEE.csv
   eCO2mix_RTE_PACA_Annuel-Definitif_2013.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2014.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2015.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2016.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2017.zip 
   eCO2mix_RTE_PACA_Annuel-Definitif_2018.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2019.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2020.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2021.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2022.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2023.zip
   eCO2mix_RTE_PACA_Annuel-Definitif_2024.zip
   eCO2mix_RTE_PACA_En-cours-Consolide.zip
   eCO2mix_RTE_PACA_En-cours-TR.zip (utile si on veut faire tourner sur l'année 2026 en cours)
   region_paca.geojson
   registre_pv_paca_raw.csv
```
