"""Chargement des données : extraction du périmètre d'étude.

Le fichier Kaggle complet (Combined_Flights_2022.parquet) contient 4 millions de vols
de janvier à juillet 2022. On ne garde que les vols au départ d'Atlanta (ATL)
en juin et juillet 2022 : c'est notre dataset d'étude.
"""

from pathlib import Path

import pandas as pd

# Dossier racine du projet : les chemins marchent quel que soit le dossier d'où on lance le code
RACINE = Path(__file__).resolve().parent.parent
FICHIER_KAGGLE = RACINE / "data/raw/Combined_Flights_2022.parquet"
FICHIER_ATLANTA = RACINE / "data/raw/vols_atlanta_ete_2022.csv"


def extraire_vols_atlanta():
    """Lit le gros fichier Kaggle, garde les départs d'Atlanta en juin-juillet, et les enregistre en CSV."""
    vols = pd.read_parquet(
        FICHIER_KAGGLE,
        filters=[("Origin", "==", "ATL"), ("Month", "in", [6, 7])],
    )
    # index=False : on n'enregistre pas l'index technique hérité du fichier Kaggle
    vols.to_csv(FICHIER_ATLANTA, index=False)
    return vols


def charger_vols_atlanta():
    """Charge le dataset d'étude (54 461 vols au départ d'Atlanta, juin-juillet 2022)."""
    return pd.read_csv(FICHIER_ATLANTA, parse_dates=["FlightDate"])


if __name__ == "__main__":
    vols = extraire_vols_atlanta()
    print(f"{len(vols)} lignes, {vols.shape[1]} colonnes enregistrées dans {FICHIER_ATLANTA}")
