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
