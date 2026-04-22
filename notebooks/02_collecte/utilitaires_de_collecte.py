# Création d'une fonction pour normaliser le nom des colonnes
def clean_name(name):
    resultat = name.lower()
    resultat = resultat.replace('(', '')
    resultat = resultat.replace(')', '')
    resultat = resultat.replace('%', '')
    resultat = resultat.replace('.', '')
    resultat = resultat.strip()
    resultat = resultat.replace(' ', '_')
    resultat = resultat.replace('é', 'e')
    resultat = resultat.replace('è', 'e')
    return resultat

# Normalisation du nom des colonnes (minuscules, pas d'espace, pas de caractères spéciaux autre que '_')
def normalize_columns_name(df) :
    # Récupération du nom des colunnes
    nom_cols = df.columns

    # Initialisation d'un dictionnaire
    # les clés seront les noms initiaux
    # les valeurs les noms normalisés
    dico = {}

    # Remplir le dictionnaire
    for nom in nom_cols:
        dico[nom] = clean_name(nom)

    # Normaliser le nom des colonnes
    return df.rename(columns=dico)

def update_database(df_new, df_old):
    # Liste des variables d'éCO2mix retenues dans l'ancien dataset
    variables_retenues = [
        'Date', 'Heures', 'Consommation',
        'Solaire', 'TCO Solaire (%)', 'TCH Solaire (%)']

    # Vérification de la présence de ces variables dans le nouveau dataset
    toutes_presentes = True
    for var in variables_retenues :
        if var not in df_new.columns :
            toutes_presentes = False

    if toutes_presentes :
        print("Les variables précédemment retenues sont toutes présentes dans le nouveau dataset.")
    else :
        return 'Variable(s) manquante(s) dans le nouveau dataset.'

    # Les variables étant toutes présentes, on peut procéder à leur extraction
    df = df_new[variables_retenues].copy()

    # On supprime les lignes où la variable TCH Solaire est manquante
    df = df.dropna(subset=['TCH Solaire (%)'])

    if df.isna().sum().sum() != 0 :
        return 'Impossible de gérer les valeurs manquantes.'




