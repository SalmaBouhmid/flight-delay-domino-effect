"""Tests du chargement et du nettoyage des données."""

import hashlib

import pandas as pd

from data_loading import FICHIER_ATLANTA
from preprocessing import colonnes_constantes


def test_dataset_brut_respecte_la_consigne(vols_bruts):
    """Au moins 30 000 lignes et 50 colonnes (cahier des charges, section 2)."""
    assert vols_bruts.shape == (54461, 61)


def test_nettoyage_ne_modifie_pas_le_fichier_brut(vols_bruts):
    """Le fichier brut sur le disque est identique avant et après le nettoyage."""
    empreinte_avant = hashlib.md5(FICHIER_ATLANTA.read_bytes()).hexdigest()
    from preprocessing import nettoyer_vols
    nettoyer_vols(vols_bruts)
    assert hashlib.md5(FICHIER_ATLANTA.read_bytes()).hexdigest() == empreinte_avant


def test_nettoyage_garde_toutes_les_lignes(vols_bruts, vols_nettoyes_a_la_volee):
    """Aucun vol n'est supprimé : les annulés et les retards extrêmes sont gardés volontairement."""
    assert len(vols_nettoyes_a_la_volee) == len(vols_bruts)
    assert vols_nettoyes_a_la_volee["Cancelled"].sum() == vols_bruts["Cancelled"].sum()


def test_pas_de_doublons(vols):
    assert vols.duplicated().sum() == 0


def test_colonnes_constantes_supprimees(vols_bruts, vols):
    constantes = colonnes_constantes(vols_bruts)
    assert len(constantes) == 10
    assert not set(constantes) & set(vols.columns)


def test_types_coherents(vols):
    assert pd.api.types.is_datetime64_any_dtype(vols["FlightDate"])
    assert vols["heure_depart_prevue"].between(0, 23).all()
    assert set(vols["statut"]) == {"À l'heure", "En retard", "Annulé", "Dévié"}
    assert vols["compagnie"].notna().all()


def test_valeurs_manquantes_seulement_pour_les_vols_annules(vols):
    """Un vol parti a toujours un retard au départ ; un vol annulé n'en a pas forcément."""
    partis = vols[~vols["Cancelled"]]
    assert partis["DepDelay"].notna().all()


def test_effet_domino_coherent(vols):
    """Le 1er départ de la journée d'un avion n'a pas de vol précédent ; les suivants en ont un (0 ou 1)."""
    premiers = vols[vols["rang_rotation"] == 1]
    assert premiers["vol_precedent_en_retard"].isna().all()
    suivants = vols[vols["rang_rotation"] > 1]["vol_precedent_en_retard"].dropna()
    assert set(suivants.unique()) <= {0.0, 1.0}


def test_nettoyage_reproductible(vols, vols_nettoyes_a_la_volee):
    """Le fichier nettoyé enregistré correspond au nettoyage recalculé."""
    assert list(vols.columns) == list(vols_nettoyes_a_la_volee.columns)
    assert vols["DepDel15"].sum() == vols_nettoyes_a_la_volee["DepDel15"].sum()
