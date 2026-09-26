"""Nettoyage et préparation des données.

Principe : on ne modifie jamais le fichier brut. On crée une copie nettoyée,
et chaque décision est expliquée (voir docs/JOURNAL.md, étape « Nettoyage »).
"""

import pandas as pd

from data_loading import RACINE, charger_vols_atlanta

FICHIER_PROPRE = RACINE / "data/processed/vols_atlanta_ete_2022_propre.csv"

# Compagnies qui opèrent moins de 1 000 vols sur la période : trop peu de vols
# pour comparer leur taux de retard de façon fiable. On les regroupe dans « Autres ».
SEUIL_VOLS_COMPAGNIE = 1000

NOMS_JOURS = {1: "Lundi", 2: "Mardi", 3: "Mercredi", 4: "Jeudi",
              5: "Vendredi", 6: "Samedi", 7: "Dimanche"}
NOMS_MOIS = {6: "Juin", 7: "Juillet"}

# Noms courts, plus lisibles dans les graphiques
NOMS_COURTS_COMPAGNIES = {
    "Delta Air Lines Inc.": "Delta",
    "Southwest Airlines Co.": "Southwest",
    "Endeavor Air Inc.": "Endeavor (Delta Connection)",
    "Spirit Air Lines": "Spirit",
    "Frontier Airlines Inc.": "Frontier",
    "American Airlines Inc.": "American",
    "Republic Airlines": "Republic",
}


def colonnes_constantes(vols):
    """Renvoie la liste des colonnes qui ont une seule valeur sur tout le dataset.

    Exemple : Origin vaut toujours « ATL » puisqu'on n'a gardé que les départs d'Atlanta.
    Ces colonnes n'apportent aucune information pour l'analyse.
    """
    return [col for col in vols.columns if vols[col].nunique(dropna=False) == 1]


def ajouter_statut(vols):
    """Ajoute la colonne « statut » : Annulé, Dévié, En retard (> 15 min) ou À l'heure.

    Le seuil de 15 minutes est la définition officielle du retard aux États-Unis (BTS).
    """
    statut = pd.Series("À l'heure", index=vols.index)
    statut[vols["DepDel15"] == 1] = "En retard"
    statut[vols["Diverted"]] = "Dévié"
    statut[vols["Cancelled"]] = "Annulé"
    vols["statut"] = statut
    return vols


def ajouter_effet_domino(vols):
    """Ajoute deux colonnes pour mesurer l'effet domino des retards d'un même avion.

    Un même avion (identifié par Tail_Number) part souvent plusieurs fois par jour d'Atlanta :
    il part vers une ville, revient, puis repart.
    - « rang_rotation » : 1er, 2e, 3e... départ de la journée de cet avion depuis Atlanta ;
    - « vol_precedent_en_retard » : 1 si le départ précédent du même avion, le même jour,
      était en retard (> 15 min), 0 sinon, vide si c'est son premier départ de la journée.
    Les vols sans immatriculation d'avion (75 vols, tous annulés) restent vides.
    """
    vols = vols.sort_values(["Tail_Number", "FlightDate", "CRSDepTime"])
    vols_du_meme_avion_le_meme_jour = vols.groupby(["Tail_Number", "FlightDate"])
    vols["rang_rotation"] = vols_du_meme_avion_le_meme_jour.cumcount() + 1
    # shift(1) = valeur de la ligne précédente dans le même groupe (le vol d'avant)
    vols["vol_precedent_en_retard"] = vols_du_meme_avion_le_meme_jour["DepDel15"].shift(1)
    vols.loc[vols["Tail_Number"].isna(), "rang_rotation"] = pd.NA
    return vols.sort_index()


def nettoyer_vols(vols_bruts):
    """Crée la version nettoyée du dataset à partir des données brutes.

    Étapes :
    1. suppression des colonnes constantes (aucune information) ;
    2. vérification des doublons ;
    3. création de colonnes lisibles (heure, jour, mois, compagnie, statut...) ;
    4. création d'indicateurs utiles à la problématique (minutes rattrapées en vol, effet domino).

    Les vols annulés sont GARDÉS : l'annulation fait partie du phénomène étudié.
    Leurs valeurs manquantes (heure de départ, retard...) sont normales : un vol annulé n'a pas décollé.
    Les très gros retards sont GARDÉS : ce sont de vrais vols, pas des erreurs de saisie.
    """
    vols = vols_bruts.copy()

    # 1. Colonnes constantes
    vols = vols.drop(columns=colonnes_constantes(vols))

    # 2. Doublons (il n'y en a aucun, mais on le vérifie à chaque exécution)
    vols = vols.drop_duplicates()

    # 3. Colonnes lisibles
    vols["heure_depart_prevue"] = vols["CRSDepTime"] // 100  # 1435 -> 14 h
    vols["jour_semaine"] = vols["DayOfWeek"].map(NOMS_JOURS)
    vols["mois"] = vols["Month"].map(NOMS_MOIS)
    vols["compagnie"] = vols["Airline"].map(NOMS_COURTS_COMPAGNIES)
    nb_vols_par_compagnie = vols["Airline"].value_counts()
    petites_compagnies = nb_vols_par_compagnie[nb_vols_par_compagnie < SEUIL_VOLS_COMPAGNIE].index
    vols.loc[vols["Airline"].isin(petites_compagnies), "compagnie"] = "Autres"
    vols = ajouter_statut(vols)

    # 4. Indicateurs
    # Minutes rattrapées en vol : positif = l'avion a réduit son retard entre départ et arrivée
    vols["minutes_rattrapees"] = vols["DepDelay"] - vols["ArrDelay"]
    vols = ajouter_effet_domino(vols)

    return vols


def charger_vols_propres():
    """Charge le dataset nettoyé (à utiliser dans le notebook et le dashboard)."""
    return pd.read_csv(FICHIER_PROPRE, parse_dates=["FlightDate"])


if __name__ == "__main__":
    vols_bruts = charger_vols_atlanta()
    vols = nettoyer_vols(vols_bruts)
    vols.to_csv(FICHIER_PROPRE, index=False)
    print(f"Brut : {vols_bruts.shape} -> Nettoyé : {vols.shape}")
    print("Colonnes constantes supprimées :", colonnes_constantes(vols_bruts))
