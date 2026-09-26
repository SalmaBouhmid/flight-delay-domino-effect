"""Méthodes d'échantillonnage et comparaison avec le dataset complet.

Population = les 54 461 vols au départ d'Atlanta (juin-juillet 2022).
On tire des échantillons d'environ 10 % (≈ 5 000 vols) avec 5 méthodes,
puis on vérifie si chaque échantillon ressemble à la population.

Pourquoi échantillonner ? Pour les nuages de points (scatter plots) : 54 000 points
se superposent et deviennent illisibles. Un échantillon représentatif de 5 000 vols
donne la même image, en plus lisible et plus rapide à afficher dans le dashboard.
"""

import numpy as np
import pandas as pd

from analysis import vols_partis

TAILLE_ECHANTILLON = 5000
GRAINE = 42  # random_state : le même tirage à chaque exécution (reproductibilité)


def echantillon_aleatoire_simple(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Tire `taille` vols au hasard : chaque vol a la même chance d'être choisi."""
    return vols.sample(n=taille, random_state=graine)


def echantillon_systematique(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Trie les vols par date et heure, puis garde 1 vol tous les k vols (k = pas).

    Ici k = 54 461 / 5 000 ≈ 10,9 : on arrondit chaque position à l'entier inférieur,
    ce qui répartit les 5 000 vols sur toute la période (du 1er juin au 31 juillet).
    Le point de départ est tiré au hasard dans le premier intervalle.
    """
    vols_tries = vols.sort_values(["FlightDate", "CRSDepTime"])
    pas = len(vols_tries) / taille
    depart = np.random.default_rng(graine).uniform(0, pas)
    positions = (depart + np.arange(taille) * pas).astype(int)
    return vols_tries.iloc[positions]


def echantillon_stratifie(vols, colonne_strate="compagnie", taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Tire le même pourcentage de vols dans chaque groupe (strate) de `colonne_strate`.

    Exemple avec les compagnies : Delta fait 66 % des vols, donc 66 % de l'échantillon sera Delta.
    Garantit que les petites compagnies sont bien présentes.
    """
    fraction = taille / len(vols)
    return vols.groupby(colonne_strate).sample(frac=fraction, random_state=graine)


def echantillon_par_grappes(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Tire des journées entières au hasard (une grappe = tous les vols d'un jour).

    On tire autant de jours que nécessaire pour atteindre environ `taille` vols.
    Pratique dans la réalité (on collecte quelques jours complets), mais risqué :
    si on tombe sur des jours d'orage, l'échantillon ne ressemble plus à la population.
    """
    jours = vols["FlightDate"].drop_duplicates()
    vols_par_jour = len(vols) / len(jours)
    nb_jours = round(taille / vols_par_jour)
    jours_tires = jours.sample(n=nb_jours, random_state=graine)
    return vols[vols["FlightDate"].isin(jours_tires)]


def echantillon_stratifie_par_jour(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Méthode temporelle : stratifié par date, pour que chacun des 61 jours soit représenté."""
    return echantillon_stratifie(vols, colonne_strate="FlightDate", taille=taille, graine=graine)


METHODES = {
    "Aléatoire simple": echantillon_aleatoire_simple,
    "Systématique": echantillon_systematique,
    "Stratifié (compagnie)": echantillon_stratifie,
    "Par grappes (jours)": echantillon_par_grappes,
    "Stratifié temporel (jour)": echantillon_stratifie_par_jour,
}


def indicateurs(vols):
    """Calcule les indicateurs clés utilisés pour comparer un échantillon à la population.

    Les indicateurs de retard sont calculés sur les vols partis (sans les annulés), comme partout dans le projet.
    """
    partis = vols_partis(vols)
    return {
        "Nombre de vols": len(vols),
        "% en retard (>15 min)": partis["DepDel15"].mean() * 100,
        "Retard moyen (min)": partis["DepDelay"].mean(),
        "Retard médian (min)": partis["DepDelay"].median(),
        "Écart-type du retard (min)": partis["DepDelay"].std(),
        "% annulés": vols["Cancelled"].mean() * 100,
        "% Delta": (vols["compagnie"] == "Delta").mean() * 100,
        "Nombre de jours couverts": vols["FlightDate"].nunique(),
    }


def comparer_echantillons(vols):
    """Tableau comparatif : une ligne par méthode + la population complète en première ligne."""
    lignes = {"Population complète": indicateurs(vols)}
    for nom, methode in METHODES.items():
        lignes[nom] = indicateurs(methode(vols))
    return pd.DataFrame(lignes).T.round(1)


def stabilite_des_methodes(vols, nb_tirages=100):
    """Répète chaque tirage `nb_tirages` fois (graines 0 à 99) et mesure le % de vols en retard obtenu.

    Un seul tirage peut être « chanceux ». En répétant, on voit quelle méthode donne
    des résultats stables (proches de la vraie valeur) et laquelle varie beaucoup.
    """
    resultats = []
    for nom, methode in METHODES.items():
        for graine in range(nb_tirages):
            echantillon = methode(vols, graine=graine)
            resultats.append({"méthode": nom, "% en retard": vols_partis(echantillon)["DepDel15"].mean() * 100})
    return pd.DataFrame(resultats)
