"""Méthodes d'échantillonnage et comparaison avec le dataset complet.

Population = les 54 461 vols au départ d'Atlanta (juin-juillet 2022).
On tire des échantillons d'environ 10 % (≈ 5 000 vols) avec 7 méthodes,
puis on mesure à quel point chaque échantillon ressemble à la population
(erreurs absolues et relatives, score de représentativité, classement).

Pourquoi échantillonner ? Pour les nuages de points (scatter plots) : 54 000 points
se superposent et deviennent illisibles. Un échantillon représentatif de 5 000 vols
donne la même image, en plus lisible et plus rapide à afficher dans le dashboard.
"""

import numpy as np
import pandas as pd

from analysis import vols_partis

TAILLE_ECHANTILLON = 5000
GRAINE = 42  # random_state : le même tirage à chaque exécution (reproductibilité)

# Seuil des retards extrêmes : Q3 + 1,5 × IQR du retard dans la population (16 + 1,5 × 19 = 44,5 min)
SEUIL_RETARD_EXTREME = 44.5


# --------------------------------------------------------------------------- Méthodes

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
    """Stratifié PROPORTIONNEL : le même pourcentage de vols est tiré dans chaque groupe (strate).

    Exemple avec les compagnies : Delta fait 66 % des vols, donc 66 % de l'échantillon sera Delta.
    """
    fraction = taille / len(vols)
    return vols.groupby(colonne_strate).sample(frac=fraction, random_state=graine)


def echantillon_stratifie_non_proportionnel(vols, colonne_strate="compagnie", taille=TAILLE_ECHANTILLON,
                                            graine=GRAINE):
    """Stratifié NON PROPORTIONNEL : le même NOMBRE de vols est tiré dans chaque groupe.

    Avec 8 compagnies et 5 000 vols : 625 vols par compagnie, qu'elle soit grande ou petite.
    Utile pour étudier les petites compagnies avec assez de vols, mais l'échantillon ne
    ressemble plus à la population (Delta passe de 66 % à 12,5 %) : pour estimer une valeur
    globale, il faudrait repondérer chaque vol (voir `pourcentage_retard_pondere`).
    Si un groupe a moins de vols que demandé, on prend tous ses vols.
    """
    nb_groupes = vols[colonne_strate].nunique()
    par_groupe = taille // nb_groupes
    return pd.concat(
        groupe.sample(n=min(len(groupe), par_groupe), random_state=graine)
        for _, groupe in vols.groupby(colonne_strate)
    )


def echantillon_par_grappes(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Tire des journées entières au hasard (une grappe = tous les vols d'un jour).

    On tire autant de jours que nécessaire pour atteindre environ `taille` vols.
    Pratique dans la réalité (on collecte quelques jours complets), mais risqué :
    si on tombe sur des jours d'orage, l'échantillon ne ressemble plus à la population.
    """
    jours = vols["FlightDate"].drop_duplicates()
    vols_par_jour = len(vols) / len(jours)
    nb_jours = max(1, round(taille / vols_par_jour))
    jours_tires = jours.sample(n=nb_jours, random_state=graine)
    return vols[vols["FlightDate"].isin(jours_tires)]


def echantillon_stratifie_par_jour(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Méthode temporelle : stratifié proportionnel par date, pour que chacun des 61 jours soit représenté."""
    return echantillon_stratifie(vols, colonne_strate="FlightDate", taille=taille, graine=graine)


def echantillon_bootstrap(vols, taille=TAILLE_ECHANTILLON, graine=GRAINE):
    """Bootstrap : tirage au hasard AVEC REMISE, un même vol peut donc être tiré plusieurs fois.

    C'est la base des méthodes de ré-échantillonnage (estimer la variabilité d'un indicateur
    en répétant le tirage). L'échantillon contient donc des lignes en double, c'est normal.
    """
    return vols.sample(n=taille, replace=True, random_state=graine)


METHODES = {
    "Aléatoire simple": echantillon_aleatoire_simple,
    "Systématique": echantillon_systematique,
    "Stratifié (compagnie)": echantillon_stratifie,
    "Stratifié non proportionnel": echantillon_stratifie_non_proportionnel,
    "Par grappes (jours)": echantillon_par_grappes,
    "Stratifié temporel (jour)": echantillon_stratifie_par_jour,
    "Bootstrap (avec remise)": echantillon_bootstrap,
}


# --------------------------------------------------------------------------- Analyse d'un échantillon

def indicateurs_du_score(vols):
    """Les 6 indicateurs utilisés pour le score de représentativité (calcul rapide)."""
    partis = vols_partis(vols)
    return {
        "% en retard (>15 min)": partis["DepDel15"].mean() * 100,
        "Retard moyen (min)": partis["DepDelay"].mean(),
        "Écart-type du retard (min)": partis["DepDelay"].std(),
        "% retards extrêmes (>44,5 min)": (partis["DepDelay"] > SEUIL_RETARD_EXTREME).mean() * 100,
        "% annulés": vols["Cancelled"].mean() * 100,
        "% Delta": (vols["compagnie"] == "Delta").mean() * 100,
    }


def indicateurs(vols):
    """Analyse complète d'un échantillon (ou de la population) : taille, qualité et indicateurs de retard.

    Les indicateurs de retard sont calculés sur les vols partis (sans les annulés), comme partout dans le projet.
    """
    partis = vols_partis(vols)
    return {
        "Nombre de vols": len(vols),
        "Lignes en double": int(vols.duplicated().sum()),
        "% retard manquant": vols["DepDelay"].isna().mean() * 100,
        "Retard médian (min)": partis["DepDelay"].median(),
        **indicateurs_du_score(vols),
        "Nombre de jours couverts": vols["FlightDate"].nunique(),
    }


def comparer_echantillons(vols):
    """Tableau comparatif : une ligne par méthode + la population complète en première ligne."""
    lignes = {"Population complète": indicateurs(vols)}
    for nom, methode in METHODES.items():
        lignes[nom] = indicateurs(methode(vols))
    return pd.DataFrame(lignes).T.round(1)


# --------------------------------------------------------------------------- Représentativité

# Le score utilise les 6 indicateurs de `indicateurs_du_score`. Le retard MÉDIAN n'y est pas :
# il vaut 0 dans la population, donc l'erreur relative (division par 0) n'aurait pas de sens.


def erreurs_par_rapport_a_la_population(population, echantillon, valeurs_population=None):
    """Pour chaque indicateur du score : valeur population, valeur échantillon, erreur absolue et relative.

    Erreur absolue  = |échantillon − population|              (dans l'unité de l'indicateur)
    Erreur relative = erreur absolue / |population| × 100      (en %, comparable entre indicateurs)
    `valeurs_population` : indicateurs de la population déjà calculés (évite de les recalculer à chaque tirage).
    """
    if valeurs_population is None:
        valeurs_population = indicateurs_du_score(population)
    valeurs_echantillon = indicateurs_du_score(echantillon)
    lignes = []
    for nom in valeurs_echantillon:
        pop, ech = valeurs_population[nom], valeurs_echantillon[nom]
        erreur_absolue = abs(ech - pop)
        lignes.append({
            "indicateur": nom,
            "population": pop,
            "échantillon": ech,
            "erreur absolue": erreur_absolue,
            "erreur relative (%)": erreur_absolue / abs(pop) * 100,
        })
    return pd.DataFrame(lignes).set_index("indicateur")


def score_representativite(population, echantillon, valeurs_population=None):
    """Score de 0 à 100 : 100 − moyenne des erreurs relatives (en %). 100 = identique à la population.

    Exemple : si l'échantillon se trompe en moyenne de 3 % sur les 6 indicateurs, le score vaut 97.
    """
    erreurs = erreurs_par_rapport_a_la_population(population, echantillon, valeurs_population)
    return max(0.0, 100 - erreurs["erreur relative (%)"].mean())


def pourcentage_retard_pondere(echantillon, population, colonne_strate="compagnie"):
    """% de vols en retard d'un échantillon stratifié, REPONDÉRÉ pour retrouver la population.

    Chaque vol reçoit un poids = (vols du groupe dans la population) / (vols du groupe dans l'échantillon).
    Ainsi un vol Delta « compte » plus qu'un vol d'une petite compagnie surreprésentée.
    """
    partis = vols_partis(echantillon)
    poids = population[colonne_strate].value_counts() / echantillon[colonne_strate].value_counts()
    poids_des_vols = partis[colonne_strate].map(poids)
    return (partis["DepDel15"] * poids_des_vols).sum() / poids_des_vols.sum() * 100


# --------------------------------------------------------------------------- Répétition des tirages

def stabilite_des_methodes(vols, nb_tirages=100):
    """Répète chaque tirage `nb_tirages` fois (graines 0 à 99) : % de retard et score de chaque tirage.

    Un seul tirage peut être « chanceux ». En répétant, on voit quelle méthode donne
    des résultats stables (proches de la vraie valeur) et laquelle varie beaucoup.
    """
    valeurs_population = indicateurs_du_score(vols)  # calculées une seule fois
    resultats = []
    for nom, methode in METHODES.items():
        for graine in range(nb_tirages):
            echantillon = methode(vols, graine=graine)
            resultats.append({
                "méthode": nom,
                "% en retard": vols_partis(echantillon)["DepDel15"].mean() * 100,
                "score": score_representativite(vols, echantillon, valeurs_population),
            })
    return pd.DataFrame(resultats)


def classement_des_methodes(stabilite):
    """Classe les méthodes selon leur score moyen sur tous les tirages (le plus représentatif en premier)."""
    classement = stabilite.groupby("méthode").agg(
        score_moyen=("score", "mean"),
        score_minimum=("score", "min"),
        ecart_type_pct_retard=("% en retard", "std"),
    ).sort_values("score_moyen", ascending=False).round(2)
    classement.insert(0, "rang", range(1, len(classement) + 1))
    return classement
