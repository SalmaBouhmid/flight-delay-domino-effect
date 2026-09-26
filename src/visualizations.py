"""Style visuel commun et fonctions de graphiques réutilisables.

Identité visuelle du projet (la même partout : notebook, présentation, dashboard) :
- BLEU   = couleur principale (les vols en général) ;
- ORANGE = couleur de mise en avant (le retard, ce qu'on veut montrer) ;
- GRIS   = le reste, en arrière-plan.
Une seule couleur par graphique sauf si une deuxième est nécessaire pour comparer.
Palette vérifiée pour les daltoniens (outil de validation de palette, 25/09/2026).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DOSSIER_FIGURES = Path(__file__).resolve().parent.parent / "reports" / "figures"

BLEU = "#2a78d6"
ORANGE = "#eb6834"
VERT_EAU = "#1baf7a"  # 3e couleur, seulement si 3 groupes à comparer
GRIS = "#c3c2b7"
ENCRE = "#0b0b0b"
ENCRE_SECONDAIRE = "#52514e"
GRILLE = "#e1e0d9"
FOND = "#fcfcfb"


def appliquer_style():
    """Applique le style du projet à tous les graphiques Matplotlib/Seaborn.

    Principe du data-ink ratio : on enlève tout ce qui n'aide pas à lire (cadre, grille verticale...).
    """
    plt.rcParams.update({
        "figure.figsize": (9, 4.5),
        "figure.dpi": 110,
        "figure.facecolor": FOND,
        "axes.facecolor": FOND,
        "axes.edgecolor": GRIS,
        "axes.labelcolor": ENCRE_SECONDAIRE,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 12,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,  # la grille passe derrière les barres
        "grid.color": GRILLE,
        "grid.linewidth": 0.8,
        "xtick.color": ENCRE_SECONDAIRE,
        "ytick.color": ENCRE_SECONDAIRE,
        "font.family": "sans-serif",
        "font.size": 10,
        "legend.frameon": False,
    })


def enregistrer_figure(nom):
    """Enregistre le graphique en cours dans reports/figures/<nom>.png (pour le rapport et la présentation)."""
    DOSSIER_FIGURES.mkdir(parents=True, exist_ok=True)
    plt.savefig(DOSSIER_FIGURES / f"{nom}.png", dpi=150, bbox_inches="tight")


def format_pourcentage(axe, axe_xy="y"):
    """Affiche les graduations de l'axe en pourcentage (ex. : 25 %)."""
    formateur = mticker.FuncFormatter(lambda valeur, _: f"{valeur:.0f} %")
    (axe.yaxis if axe_xy == "y" else axe.xaxis).set_major_formatter(formateur)


def barres_horizontales(valeurs, titre, legende_axe, a_mettre_en_avant=(), format_etiquette="{:.1f} %", axe=None):
    """Barres horizontales triées, avec la valeur écrite au bout de chaque barre.

    valeurs           : Series pandas (index = catégories, valeurs = nombres)
    a_mettre_en_avant : catégories colorées en orange ; les autres sont en bleu
    """
    if axe is None:
        _, axe = plt.subplots(figsize=(9, 0.45 * len(valeurs) + 1))
    valeurs = valeurs.sort_values()
    couleurs = [ORANGE if categorie in a_mettre_en_avant else BLEU for categorie in valeurs.index]
    barres = axe.barh(valeurs.index.astype(str), valeurs.values, color=couleurs, height=0.65)
    axe.bar_label(barres, labels=[format_etiquette.format(v).replace(".", ",") for v in valeurs.values],
                  padding=4, color=ENCRE_SECONDAIRE, fontsize=9)
    axe.set_title(titre)
    axe.set_xlabel(legende_axe)
    axe.grid(axis="y", visible=False)
    axe.grid(axis="x", visible=True)
    axe.set_xlim(0, valeurs.max() * 1.15)
    return axe


def ligne_temporelle(valeurs, titre, legende_x, legende_y, couleur=BLEU, axe=None, etiquette=None):
    """Courbe d'un indicateur dans le temps (par heure, par jour...)."""
    if axe is None:
        _, axe = plt.subplots()
    axe.plot(valeurs.index, valeurs.values, color=couleur, linewidth=2, marker="o", markersize=4, label=etiquette)
    axe.set_title(titre)
    axe.set_xlabel(legende_x)
    axe.set_ylabel(legende_y)
    return axe


# Thème Plotly équivalent, pour les graphiques interactifs (notebook et dashboard)
PLOTLY_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="sans-serif", size=13, color=ENCRE_SECONDAIRE),
    title_font=dict(size=16, color=ENCRE),
    paper_bgcolor=FOND,
    plot_bgcolor=FOND,
    colorway=[BLEU, ORANGE, VERT_EAU],
    margin=dict(l=10, r=10, t=60, b=10),
)
