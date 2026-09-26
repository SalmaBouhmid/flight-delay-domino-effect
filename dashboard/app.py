"""Dashboard interactif : l'effet domino des retards à Atlanta (été 2022).

Lancer depuis la racine du projet :  streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Permet d'importer les modules du dossier src/
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from analysis import effet_domino, indicateurs_cles, taux_de_retard_par, tableau_croise_retard, vols_partis
from preprocessing import charger_vols_propres
from sampling import echantillon_stratifie_par_jour
from visualizations import BLEU, ENCRE_SECONDAIRE, GRIS, ORANGE, PLOTLY_LAYOUT

st.set_page_config(page_title="Effet domino des retards — Atlanta", page_icon="✈️", layout="wide")

ORDRE_JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MINIMUM_VOLS_DOMINO = 100  # en dessous, le pourcentage d'un groupe est trop fragile pour être affiché


@st.cache_data
def charger_donnees():
    """Charge le dataset nettoyé une seule fois (mis en cache par Streamlit)."""
    return charger_vols_propres()


def mise_en_forme(figure, hauteur=380):
    """Applique le style du projet à un graphique Plotly."""
    figure.update_layout(**PLOTLY_LAYOUT, height=hauteur, hoverlabel=dict(bgcolor="white"))
    if figure.layout.title.text is None:
        figure.update_layout(title_text="")  # évite l'affichage de « undefined » quand il n'y a pas de titre
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(gridcolor="#e1e0d9")
    return figure


def format_fr(nombre, decimales=1):
    """Écrit un nombre à la française : 26,3 au lieu de 26.3, espace pour les milliers."""
    return f"{nombre:,.{decimales}f}".replace(",", " ").replace(".", ",")


vols = charger_donnees()

# --------------------------------------------------------------------------- Filtres
st.sidebar.header("🔎 Filtres")
st.sidebar.caption("Tous les graphiques et indicateurs se mettent à jour selon ces filtres.")

date_min, date_max = vols["FlightDate"].min().date(), vols["FlightDate"].max().date()
periode = st.sidebar.date_input("Période", value=(date_min, date_max), min_value=date_min, max_value=date_max,
                                format="DD/MM/YYYY")

toutes_compagnies = vols["compagnie"].value_counts().index.tolist()
compagnies = st.sidebar.multiselect("Compagnies", toutes_compagnies, default=toutes_compagnies)

heures = st.sidebar.slider("Heure de départ prévue", min_value=5, max_value=23, value=(5, 23), format="%d h")

jours = st.sidebar.multiselect("Jours de la semaine", ORDRE_JOURS, default=ORDRE_JOURS)

st.sidebar.divider()
st.sidebar.caption(
    "**Définition** : un vol est « en retard » s'il part plus de 15 minutes après l'heure prévue "
    "(définition officielle du Bureau of Transportation Statistics)."
)

# La date peut n'avoir qu'une borne pendant que l'utilisateur choisit la seconde
debut, fin = (periode[0], periode[-1]) if isinstance(periode, tuple) and periode else (date_min, date_max)

filtre = (
    vols["FlightDate"].dt.date.between(debut, fin)
    & vols["compagnie"].isin(compagnies)
    & vols["heure_depart_prevue"].between(*heures)
    & vols["jour_semaine"].isin(jours)
)
selection = vols[filtre]

# --------------------------------------------------------------------------- En-tête
st.title("✈️ L'effet domino des retards")
st.markdown(
    "#### Quand et pourquoi les vols au départ d'Atlanta prennent-ils du retard pendant l'été 2022 ?\n"
    "54 461 vols au départ de l'aéroport le plus fréquenté du monde (juin–juillet 2022). "
    "Source : Bureau of Transportation Statistics, via Kaggle."
)

if len(vols_partis(selection)) < 50:
    st.warning("Moins de 50 vols correspondent à ces filtres : élargissez la sélection pour obtenir des résultats fiables.")
    st.stop()

# --------------------------------------------------------------------------- KPI
kpi = indicateurs_cles(selection)
kpi_global = indicateurs_cles(vols)
domino = effet_domino(selection)

colonnes_kpi = st.columns(5)
colonnes_kpi[0].metric("Vols sélectionnés", format_fr(kpi["nb_vols"], 0))
filtres_actifs = len(selection) < len(vols)
colonnes_kpi[1].metric(
    "En retard (> 15 min)", f"{format_fr(kpi['pct_retard'])} %",
    delta=f"{format_fr(kpi['pct_retard'] - kpi_global['pct_retard'])} pts vs ensemble" if filtres_actifs else None,
    delta_color="inverse", help="Part des vols partis avec plus de 15 min de retard. L'écart est calculé par rapport "
                                "à l'ensemble des 54 461 vols (rouge = pire que la moyenne).",
)
colonnes_kpi[2].metric("Durée moyenne d'un retard", f"{format_fr(kpi['retard_moyen_des_vols_en_retard'], 0)} min",
                       help="Retard moyen au départ, calculé seulement sur les vols partis en retard.")
colonnes_kpi[3].metric("Vols annulés", f"{format_fr(kpi['pct_annules'])} %")
AIDE_DOMINO = ("Combien de fois plus de risque d'être en retard quand le vol précédent "
               "du même avion (le même jour) était déjà en retard.")
domino_fiable = len(domino) == 2 and domino["nb_vols"].min() >= MINIMUM_VOLS_DOMINO
if domino_fiable:
    multiplicateur = domino.loc["Vol précédent en retard", "pct_retard"] / domino.loc["Vol précédent à l'heure", "pct_retard"]
    colonnes_kpi[4].metric("Effet domino", f"× {format_fr(multiplicateur)}", help=AIDE_DOMINO)
else:
    colonnes_kpi[4].metric("Effet domino", "—", help=AIDE_DOMINO + f" Non calculé : moins de {MINIMUM_VOLS_DOMINO} vols "
                                                   "dans un des deux groupes avec ces filtres.")

st.divider()

# --------------------------------------------------------------------------- Onglets
onglet_vue, onglet_domino, onglet_comparer, onglet_destinations, onglet_insights = st.tabs(
    ["📈 Vue générale", "🔗 Effet domino", "⚖️ Comparer des compagnies", "🗺️ Destinations", "💡 Insights"]
)

with onglet_vue:
    st.subheader("Le retard s'accumule au fil de la journée")
    colonne_gauche, colonne_droite = st.columns(2)

    par_heure = taux_de_retard_par(selection, "heure_depart_prevue").reset_index()
    figure = px.line(par_heure, x="heure_depart_prevue", y="pct_retard", markers=True,
                     custom_data=["nb_vols", "retard_median_min"],
                     labels={"heure_depart_prevue": "Heure de départ prévue", "pct_retard": "% de vols en retard"})
    figure.update_traces(line_color=ORANGE, line_width=3,
                         hovertemplate="%{x} h : <b>%{y:.1f} %</b> en retard<br>%{customdata[0]} vols<br>"
                                       "retard médian : %{customdata[1]} min<extra></extra>")
    figure.update_yaxes(ticksuffix=" %", rangemode="tozero")
    colonne_gauche.plotly_chart(mise_en_forme(figure), width="stretch")
    colonne_gauche.caption("Le matin, les avions partent à l'heure ; le soir, les retards accumulés se reportent sur les derniers vols.")

    par_jour_semaine = taux_de_retard_par(selection, "jour_semaine").reindex([j for j in ORDRE_JOURS if j in jours]).reset_index()
    figure = px.bar(par_jour_semaine, x="jour_semaine", y="pct_retard", text_auto=".0f",
                    labels={"jour_semaine": "", "pct_retard": "% de vols en retard"})
    figure.update_traces(marker_color=BLEU, textposition="outside", texttemplate="%{y:.0f} %",
                         hovertemplate="%{x} : <b>%{y:.1f} %</b> en retard<extra></extra>")
    figure.update_yaxes(ticksuffix=" %", range=[0, par_jour_semaine["pct_retard"].max() * 1.2])  # place pour les étiquettes
    colonne_droite.plotly_chart(mise_en_forme(figure), width="stretch")
    colonne_droite.caption("L'écart entre jours de la semaine est plus faible que l'écart entre heures.")

    st.subheader("Jour après jour : certains jours font exploser les retards")
    par_date = taux_de_retard_par(selection, "FlightDate").reset_index()
    figure = px.line(par_date, x="FlightDate", y="pct_retard", custom_data=["nb_vols"],
                     labels={"FlightDate": "", "pct_retard": "% de vols en retard"})
    figure.update_traces(line_color=BLEU, hovertemplate="%{x|%d/%m} : <b>%{y:.1f} %</b> en retard (%{customdata[0]} vols)<extra></extra>")
    figure.add_hline(y=kpi["pct_retard"], line_color=GRIS, annotation_text="moyenne de la sélection",
                     annotation_font_color=ENCRE_SECONDAIRE)
    figure.update_yaxes(ticksuffix=" %", rangemode="tozero")
    figure.update_xaxes(tickformat="%d/%m")
    st.plotly_chart(mise_en_forme(figure, 320), width="stretch")

    st.subheader("Carte des heures à risque")
    jours_choisis = [j for j in ORDRE_JOURS if j in jours]
    carte = tableau_croise_retard(selection, "jour_semaine", "heure_depart_prevue").reindex(jours_choisis)
    effectifs = vols_partis(selection).groupby(["jour_semaine", "heure_depart_prevue"]).size().unstack().reindex(jours_choisis)
    carte = carte.where(effectifs >= 30)  # cases avec moins de 30 vols masquées (pourcentage peu fiable)
    figure = px.imshow(carte, color_continuous_scale="Oranges", aspect="auto", text_auto=".0f",
                       labels=dict(x="Heure de départ prévue", y="", color="% en retard"))
    figure.update_traces(hovertemplate="%{y} à %{x} h : <b>%{z:.1f} %</b> en retard<extra></extra>")
    st.plotly_chart(mise_en_forme(figure, 340), width="stretch")
    st.caption("Plus la case est foncée, plus les vols de ce créneau partent souvent en retard. "
               "Cases vides : moins de 30 vols, pourcentage non affiché.")

with onglet_domino:
    st.subheader("Un retard se transmet au vol suivant du même avion")
    st.markdown(
        "Un même avion (repéré par son immatriculation) part souvent plusieurs fois par jour d'Atlanta. "
        "Pour chaque départ, on regarde si **son départ précédent, le même jour**, était déjà en retard."
    )
    if not domino_fiable:
        st.warning(f"Avec ces filtres, un des deux groupes compte moins de {MINIMUM_VOLS_DOMINO} vols : "
                   "les pourcentages ci-dessous sont peu fiables.")
    colonne_gauche, colonne_droite = st.columns([2, 3])

    figure = px.bar(domino.reset_index(), x="pct_retard", y="vol_precedent_en_retard", orientation="h",
                    custom_data=["nb_vols"], labels={"pct_retard": "% de vols en retard", "vol_precedent_en_retard": ""})
    figure.update_traces(marker_color=[BLEU, ORANGE][: len(domino)], texttemplate="%{x:.0f} %", textposition="outside",
                         hovertemplate="%{y} : <b>%{x:.1f} %</b> en retard<br>%{customdata[0]} vols<extra></extra>")
    figure.update_xaxes(ticksuffix=" %", range=[0, 70])
    colonne_gauche.plotly_chart(mise_en_forme(figure, 300), width="stretch")

    partis_avec_precedent = vols_partis(selection).dropna(subset=["vol_precedent_en_retard"])
    domino_heure = tableau_croise_retard(partis_avec_precedent, "heure_depart_prevue", "vol_precedent_en_retard")
    effectifs = partis_avec_precedent.groupby(["heure_depart_prevue", "vol_precedent_en_retard"]).size().unstack()
    domino_heure = domino_heure.where(effectifs >= 30)  # moins de 30 vols : pourcentage trop fragile, masqué

    figure = go.Figure()
    for valeur, nom, couleur in [(1.0, "Vol précédent en retard", ORANGE), (0.0, "Vol précédent à l'heure", BLEU)]:
        if valeur in domino_heure:
            figure.add_trace(go.Scatter(x=domino_heure.index, y=domino_heure[valeur], name=nom, mode="lines+markers",
                                        line=dict(color=couleur, width=3),
                                        hovertemplate="%{x} h : <b>%{y:.1f} %</b> en retard<extra>" + nom + "</extra>"))
    figure.update_layout(title="À chaque heure, l'écart persiste", legend=dict(orientation="h", y=-0.2))
    figure.update_xaxes(title="Heure de départ prévue")
    figure.update_yaxes(title="% de vols en retard", ticksuffix=" %", rangemode="tozero")
    colonne_droite.plotly_chart(mise_en_forme(figure, 360), width="stretch")

    st.info(
        "**Lecture prudente** : c'est une association, pas une preuve de cause à effet. Les deux vols d'un même avion "
        "partagent aussi la même journée (météo, affluence). Le BTS reconnaît toutefois officiellement cette cause de "
        "retard (« Aircraft Arriving Late »)."
    )

with onglet_comparer:
    st.subheader("Comparer deux compagnies")
    if len(compagnies) < 2:
        st.info("Sélectionnez au moins deux compagnies dans les filtres pour les comparer.")
        compagnie_a = compagnie_b = None
    else:
        colonne_a, colonne_b = st.columns(2)
        compagnie_a = colonne_a.selectbox("Compagnie A", compagnies, index=0)
        compagnie_b = colonne_b.selectbox("Compagnie B", compagnies, index=1)

    # La couleur suit la position (A = bleu, B = orange) : elle ne change pas quand on filtre
    couleurs_ab = {compagnie_a: BLEU, compagnie_b: ORANGE}
    duo = selection[selection["compagnie"].isin([compagnie_a, compagnie_b])]
    if compagnie_a is None:
        pass
    elif compagnie_a == compagnie_b:
        st.info("Choisissez deux compagnies différentes.")
    elif vols_partis(duo)["compagnie"].nunique() < 2:
        st.warning("Une des deux compagnies n'a aucun vol avec les filtres actuels.")
    else:
        resume = taux_de_retard_par(duo, "compagnie").loc[[compagnie_a, compagnie_b]]
        colonnes = st.columns(2)
        for colonne, compagnie in zip(colonnes, [compagnie_a, compagnie_b]):
            ligne = resume.loc[compagnie]
            colonne.metric(compagnie, f"{format_fr(ligne['pct_retard'])} % en retard",
                           help=f"{format_fr(ligne['nb_vols'], 0)} vols ; retard médian {format_fr(ligne['retard_median_min'], 0)} min")
            colonne.caption(f"{format_fr(ligne['nb_vols'], 0)} vols · retard médian {format_fr(ligne['retard_median_min'], 0)} min")

        par_heure_duo = tableau_croise_retard(duo, "heure_depart_prevue", "compagnie")
        effectifs = vols_partis(duo).groupby(["heure_depart_prevue", "compagnie"]).size().unstack()
        par_heure_duo = par_heure_duo.where(effectifs >= 20)
        figure = go.Figure()
        for compagnie in [compagnie_a, compagnie_b]:
            figure.add_trace(go.Scatter(x=par_heure_duo.index, y=par_heure_duo[compagnie], name=compagnie,
                                        mode="lines+markers", line=dict(color=couleurs_ab[compagnie], width=3),
                                        hovertemplate="%{x} h : <b>%{y:.1f} %</b><extra>" + compagnie + "</extra>"))
        figure.update_layout(title="% de vols en retard selon l'heure de départ", legend=dict(orientation="h", y=-0.2))
        figure.update_xaxes(title="Heure de départ prévue")
        figure.update_yaxes(title="% de vols en retard", ticksuffix=" %", rangemode="tozero")
        st.plotly_chart(mise_en_forme(figure), width="stretch")
        st.caption("Les heures avec moins de 20 vols pour une compagnie sont masquées (pourcentage peu fiable).")

    st.subheader("Toutes les compagnies sélectionnées")
    toutes = taux_de_retard_par(selection, "compagnie").sort_values("pct_retard").reset_index()
    toutes["etiquette"] = toutes["pct_retard"].map(lambda valeur: f"{format_fr(valeur)} %")
    figure = px.bar(toutes, x="pct_retard", y="compagnie", orientation="h", text="etiquette", custom_data=["nb_vols"],
                    labels={"pct_retard": "% de vols en retard", "compagnie": ""})
    figure.update_traces(marker_color=BLEU, textposition="outside",
                         hovertemplate="%{y} : <b>%{text}</b> en retard<br>%{customdata[0]} vols<extra></extra>")
    figure.update_xaxes(ticksuffix=" %", range=[0, toutes["pct_retard"].max() * 1.18])
    st.plotly_chart(mise_en_forme(figure, 60 + 40 * len(toutes)), width="stretch")

with onglet_destinations:
    st.subheader("Quelles destinations sont les plus touchées ?")
    minimum = st.slider("Nombre minimum de vols par destination", 50, 800, 300, step=50,
                        help="Les destinations avec peu de vols donnent des pourcentages peu fiables.")
    destinations = taux_de_retard_par(selection, "Dest")
    destinations["distance_miles"] = selection.groupby("Dest")["Distance"].first()
    destinations["ville"] = selection.groupby("Dest")["DestCityName"].first()
    destinations = destinations[destinations["nb_vols"] >= minimum].reset_index()
    # Étiquettes seulement sur les extrêmes (4 plus touchées, 3 plus ponctuelles) : sinon les noms se chevauchent
    extremes = set(destinations.nlargest(4, "pct_retard")["Dest"]) | set(destinations.nsmallest(3, "pct_retard")["Dest"])
    destinations["etiquette"] = destinations["Dest"].where(destinations["Dest"].isin(extremes), "")

    if destinations.empty:
        st.info("Aucune destination n'atteint ce nombre de vols avec les filtres actuels.")
    else:
        figure = px.scatter(destinations, x="distance_miles", y="pct_retard", size="nb_vols", text="etiquette",
                            custom_data=["ville", "nb_vols", "retard_median_min", "Dest"],
                            labels={"distance_miles": "Distance depuis Atlanta (miles)", "pct_retard": "% de vols en retard"})
        figure.update_traces(marker=dict(color=BLEU, opacity=0.55, line=dict(width=1, color="white")),
                             textposition="top center", textfont=dict(size=12, color=ENCRE_SECONDAIRE),
                             hovertemplate="<b>%{customdata[0]}</b> (%{customdata[3]})<br>%{y:.1f} % en retard<br>"
                                           "%{customdata[1]} vols · %{x} miles<br>retard médian %{customdata[2]} min<extra></extra>")
        figure.update_yaxes(ticksuffix=" %")
        st.plotly_chart(mise_en_forme(figure, 520), width="stretch")
        st.caption("Taille des bulles = nombre de vols. Seules les destinations extrêmes sont nommées : survolez une bulle "
                   "pour voir les autres. La distance n'explique pas le retard ; la Floride revient souvent parmi les plus touchées.")

    st.subheader("Le retard au départ se retrouve à l'arrivée")
    echantillon = echantillon_stratifie_par_jour(selection, taille=min(3000, len(selection)))
    echantillon = echantillon.dropna(subset=["DepDelay", "ArrDelay"])
    figure = px.scatter(echantillon, x="DepDelay", y="ArrDelay", opacity=0.35, custom_data=["compagnie", "Dest"],
                        labels={"DepDelay": "Retard au départ (min)", "ArrDelay": "Retard à l'arrivée (min)"})
    figure.update_traces(marker=dict(color=BLEU, size=5),
                         hovertemplate="%{customdata[0]} → %{customdata[1]}<br>départ %{x} min · arrivée %{y} min<extra></extra>")
    figure.add_trace(go.Scatter(x=[-30, 300], y=[-30, 300], mode="lines", line=dict(color=ORANGE, width=2),
                                name="arrivée = départ", hoverinfo="skip"))
    figure.update_xaxes(range=[-30, 300])
    figure.update_yaxes(range=[-60, 300])
    st.plotly_chart(mise_en_forme(figure, 450), width="stretch")
    st.caption("Échantillon stratifié par jour (3 000 vols au maximum) pour rester lisible. Zoom possible à la souris.")

with onglet_insights:
    st.subheader("Ce que disent les données")
    st.markdown(
        """
1. **Le retard est fréquent** — 26 % des vols partent avec plus de 15 minutes de retard ; 8 % avec plus d'une heure.
2. **Il grandit au fil de la journée** — environ 12 % des vols sont en retard à 6 h, contre 40 % à 20 h, et ce tous les jours de la semaine.
3. **L'effet domino est mesurable** — quand le vol précédent du même avion était en retard, le suivant l'est une fois sur deux (50 % contre 24 %), à chaque heure de la journée.
4. **Le retard se joue au départ** — il se retrouve presque entièrement à l'arrivée (corrélation 0,98) ; la distance du vol ne joue aucun rôle.
5. **Les compagnies ne se valent pas** — Southwest (37 %) et Frontier (35 %) contre Endeavor (18 %) ; Southwest s'effondre surtout le soir.
6. **Certains jours font exploser les retards** — de 10 % à 63 % de vols en retard selon le jour.

**Piste d'action** : protéger les premières rotations de la journée (marges au sol, avions de réserve), car chaque retard
évité le matin en évite d'autres l'après-midi.
        """
    )
    st.subheader("Limites")
    st.markdown(
        """
- Un seul aéroport (Atlanta) et deux mois d'été : pas de généralisation automatique.
- Pas de données météo ni de causes détaillées de retard dans ce fichier.
- Les vols retour vers Atlanta, entre deux départs du même avion, ne sont pas observés.
- Delta représente 66 % des vols ; les petites compagnies sont regroupées dans « Autres ».
- Toutes les relations sont des associations, pas des preuves de causalité.
        """
    )
    st.caption("Données : Bureau of Transportation Statistics (BTS) via Kaggle « Flight Status Prediction ». "
               "Projet de visualisation des données — code source et méthode dans le dépôt du projet.")
