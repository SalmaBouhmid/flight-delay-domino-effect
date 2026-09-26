"""Tests des calculs d'analyse et du démarrage du dashboard."""

from pathlib import Path

import pytest

from analysis import effet_domino, indicateurs_cles, resume_qualite, tableau_croise_retard, taux_de_retard_par

APP = Path(__file__).resolve().parent.parent / "dashboard" / "app.py"


def test_pourcentages_entre_0_et_100(vols):
    for colonne in ["heure_depart_prevue", "compagnie", "jour_semaine", "Dest"]:
        tableau = taux_de_retard_par(vols, colonne)
        assert not tableau.empty
        assert tableau["pct_retard"].between(0, 100).all()


def test_proportions_totalisent_100(vols):
    assert vols["statut"].value_counts(normalize=True).sum() == pytest.approx(1)
    assert vols["compagnie"].value_counts(normalize=True).sum() == pytest.approx(1)


def test_indicateurs_cles_non_vides(vols):
    kpi = indicateurs_cles(vols)
    assert kpi["nb_vols"] == 54461
    assert 0 < kpi["pct_retard"] < 100
    assert kpi["retard_moyen_des_vols_en_retard"] > 15  # un vol « en retard » a plus de 15 min de retard


def test_effet_domino_resultat_principal(vols):
    """Le résultat central du projet : 50 % contre 24 %."""
    domino = effet_domino(vols)["pct_retard"]
    assert domino["Vol précédent à l'heure"] == pytest.approx(24.1, abs=0.1)
    assert domino["Vol précédent en retard"] == pytest.approx(50.0, abs=0.1)


def test_tableau_croise_non_vide(vols):
    carte = tableau_croise_retard(vols, "jour_semaine", "heure_depart_prevue")
    assert carte.shape[0] == 7
    assert carte.stack().between(0, 100).all()


def test_resume_qualite(vols_bruts):
    resume = resume_qualite(vols_bruts)
    assert resume["Nombre de lignes"] == 54461
    assert resume["Lignes en double"] == 0


def test_dashboard_demarre_sans_erreur():
    """Le dashboard s'exécute entièrement (tous les onglets) sans exception."""
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(APP), default_timeout=300)
    app.run()
    assert not app.exception
    assert len(app.metric) >= 5


def test_filtre_modifie_les_resultats():
    """Changer un filtre change réellement les indicateurs."""
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(APP), default_timeout=300)
    app.run()
    avant = app.metric[1].value
    app.sidebar.slider[0].set_value((18, 23))
    app.run()
    assert not app.exception
    assert app.metric[1].value != avant
