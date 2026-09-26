# Journal du projet — étape par étape

Ce journal raconte **ce qui a été fait, dans quel ordre, et pourquoi**. Il sert à :
- savoir où en est le projet ;
- pouvoir expliquer chaque décision au professeur ;
- rédiger le rapport final.

Les phases suivent le cahier des charges (`docs/cahier_des_charges.md`, section 27).

---

## Tableau d'avancement

| Phase | Contenu | État |
|---|---|---|
| 1 | Recherche et choix du dataset | ✅ Fait (25/09) |
| 2 | Problématique et sous-questions | ✅ Fait (25/09) |
| 2 bis | PowerPoint du rendu de lundi | ✅ Fait (25/09) — à relire |
| 3 | Exploration et nettoyage | ✅ Fait (25/09) |
| 4 | Échantillonnage | ✅ Fait (25/09) |
| 5 | Analyse univariée | ✅ Fait (25/09) |
| 6 | Analyse bivariée | ✅ Fait (25/09) |
| 7 | Analyse multivariée | ✅ Fait (25/09) |
| 8 | Storytelling et insights | ✅ Fait (25/09) — à valider ensemble |
| 9 | Dashboard Streamlit | ✅ Fait (25/09) |
| 10 | Tests et design du dashboard | ✅ Fait (26/09) |
| 11 | Rapport PDF (6 pages) | ✅ Fait (26/09) — à relire |
| 12 | Présentation orale finale (10 min) | ✅ Fait (26/09) — à répéter |
| 13 | GitHub public + dashboard en ligne + README portfolio | 🟡 Dépôt git local prêt ; publication à faire avec vos comptes (`docs/MISE_EN_LIGNE.md`) |

---

## Phase 1 — Choix du dataset (25/09)

**Contrainte :** Kaggle, ≥ 30 000 lignes, ≥ 50 colonnes, numériques + catégorielles, domaine mobilité/transport
(lien avec le stage chez ALSA Agadir City).

**Candidats comparés :**

| Dataset | Lignes | Colonnes | Verdict |
|---|---|---|---|
| **Flight Status Prediction (vols USA 2018-2022)** | ~29 M (4 M en 2022) | 61 | ✅ **Retenu** |
| Uber & Lyft Boston | 693 071 | 57 | Seulement 22 jours ; ~30 colonnes météo redondantes ; très utilisé pour « prédire le prix » |
| Accidents en France 2005-2016 | ~840 000 accidents | ~55 après jointure de 4 tables | Codes à décoder, 4 tables à joindre |
| Accidents UK 2005-2017 | ~2 M | ~57 après jointure | Très lourd (1,3 Go), sujet proche du précédent |
| US Accidents | 7,7 M | **46** | ❌ < 50 colonnes |
| Chicago Traffic Crashes | ~900 000 | **48** | ❌ < 50 colonnes |
| Taxis NYC / vélos Divvy | millions | < 25 | ❌ trop peu de colonnes |

**Pourquoi les vols ?**
- données **officielles** (BTS) et réelles ;
- la colonne `Tail_Number` (immatriculation de l'avion) permet un **angle original : l'effet domino des retards** ;
- 58 notebooks sur Kaggle + statistiques officielles du BTS → on peut **comparer nos résultats** ;
- lien direct avec le transport de voyageurs (ponctualité = indicateur n°1 d'un exploitant, comme chez ALSA).

**Décision sur la taille :** 4 millions de lignes, c'est trop lourd et inutile. On a délimité un **périmètre** :
les départs d'Atlanta en juin-juillet 2022 = **54 461 vols**. (Juillet seul = 27 533, sous le minimum de 30 000.)

**Fichiers créés :** `src/data_loading.py` → `data/raw/vols_atlanta_ete_2022.csv`.

---

## Phase 2 — Problématique (25/09)

> **Quand et pourquoi les vols au départ d'Atlanta prennent-ils du retard pendant l'été 2022 ?**

1. Quelle est l'ampleur des retards ?
2. Comment le retard évolue-t-il au fil de la journée et de la semaine ?
3. Quelles compagnies et quelles destinations sont les plus touchées ?
4. Le retard au départ se rattrape-t-il en vol ?
5. Un retard se transmet-il d'un vol à l'autre du même avion (effet domino) ?

**Phrase mémorable :** *« Un retard de vol ne naît pas au hasard : il grandit au fil de la journée.
Nous l'avons mesuré sur 54 000 vols au départ du premier aéroport du monde. »*

**Définition clé :** « en retard » = départ **plus de 15 min** après l'heure prévue (définition officielle BTS).

---

## Phase 3 — Exploration et nettoyage (25/09)

**Exploration** (notebook, sections 5-6) : types, statistiques, cardinalité, valeurs manquantes, doublons, outliers, incohérences.

**Constats :**
- 0 doublon ;
- valeurs manquantes **toutes expliquées** : vols annulés (1 009) et déviés (123) n'ont pas d'heure/retard ;
- retard très asymétrique : médiane 0 min, moyenne 16 min, maximum 2 493 min (41 h) ;
- ≈ 12 % d'outliers selon l'IQR, mais ce sont de **vrais** retards ;
- 10 colonnes constantes (toujours « Atlanta »).

**Décisions de nettoyage** (`src/preprocessing.py`) :

| Décision | Raison |
|---|---|
| Supprimer les 10 colonnes constantes | Aucune information (une seule valeur) |
| Garder les valeurs manquantes | Elles ont un sens (vol annulé = pas de retard mesurable) |
| Garder les vols annulés | L'annulation fait partie du phénomène |
| Garder les outliers | Ce sont de vrais vols, pas des erreurs |
| Regrouper les compagnies < 1 000 vols en « Autres » | Trop peu de vols pour un pourcentage fiable |
| Ajouter 8 colonnes (heure, jour, statut, effet domino…) | Répondre aux sous-questions, graphiques lisibles |

Résultat : `data/processed/vols_atlanta_ete_2022_propre.csv` (54 461 × 59). Le fichier brut n'est jamais modifié.

---

## Phase 4 — Échantillonnage (25/09)

**Pourquoi ?** Les nuages de points avec 54 000 points sont illisibles et lents dans le dashboard → on a besoin
d'un échantillon **représentatif** de ~5 000 vols (10 %).

**5 méthodes testées** (`src/sampling.py`) : aléatoire simple, systématique, stratifié par compagnie,
par grappes (jours entiers), stratifié temporel (par jour). Toutes avec `random_state` fixé.

**Résultats :**
- un seul tirage : les 5 méthodes donnent ≈ 26 % de retard (population : 26,2 %) ;
- **100 tirages par méthode** : 4 méthodes restent stables (écart-type ≈ 0,5 point), mais **les grappes varient de 18 % à 36 %**
  → les retards dépendent fortement du jour, 6 jours ne représentent pas l'été.

**Choix :** échantillon **stratifié par jour** (4 994 vols) pour les nuages de points. Tous les pourcentages
restent calculés sur les 54 461 vols.

---

## Phases 5-7 — Analyses (25/09)

Toutes dans `notebooks/analysis.ipynb`, figures enregistrées dans `reports/figures/`.

| Niveau | Graphiques | Question |
|---|---|---|
| Univariée | statut, distribution du retard, vols par heure, compagnies | Que se passe-t-il ? |
| Bivariée | retard × heure, × compagnie, × jour, statut × jour de semaine, départ × arrivée, effet domino, distance, corrélations | Quand ? Chez qui ? Quels facteurs ? |
| Multivariée | heatmap jour × heure, domino × heure, compagnie × heure, bulles destinations (Plotly) | Quels profils ? |

**Identité visuelle :** bleu = les vols en général, orange = le retard / ce qu'on met en avant, gris = le reste.
Palette vérifiée pour les daltoniens. Titres = la conclusion du graphique (pas « Graphique 1 »).

---

## Phase 8 — Insights (25/09)

1. **Le retard est fréquent** : 26 % des vols partent avec plus de 15 min de retard ; 8 % avec plus d'1 h.
2. **Il grandit au fil de la journée** : ≈ 12 % à 6 h → ≈ 40 % à 20 h, tous les jours de la semaine.
3. **Effet domino** : si le vol précédent du même avion était en retard → 50 % de retard, contre 24 % sinon, à chaque heure.
4. **Le retard se joue au départ** : corrélation départ/arrivée 0,98 ; seulement 20 % des vols partis en retard arrivent à l'heure ; la distance ne joue aucun rôle.
5. **Compagnies** : Southwest (37 %) et Frontier (35 %) contre Endeavor (18 %) ; Southwest s'effondre surtout le soir.
6. **Jours exceptionnels** : de 10 % à 63 % de vols en retard selon le jour.

⚠️ **À valider ensemble** avant le rapport final.

---

## Phase 2 bis — PowerPoint du rendu de lundi (25/09)

`presentation/rendu_etape_1.pptx` : 9 slides.

| # | Slide | Contenu |
|---|---|---|
| 1 | Titre | L'effet domino des retards |
| 2 | Pourquoi étudier les retards ? | 26 % de vols en retard, lien avec le stage ALSA |
| 3 | Recherche du dataset | Tableau des 7 candidats comparés |
| 4 | Le dataset retenu | 4 M → 54 461 vols × 61 colonnes, justification du périmètre |
| 5 | Problématique | Question + 5 sous-questions |
| 6 | Qualité des données | Doublons, manquants, outliers, colonnes constantes |
| 7 | Observation 1 | Le retard s'accumule au fil de la journée (graphique) |
| 8 | Observation 2 | Effet domino 24 % → 50 % + compagnies (graphique) |
| 9 | Suite du projet | Planning des 2 semaines |

**Le texte à dire est dans les notes de chaque slide** (PowerPoint → Affichage → Page de notes).
Les graphiques sont des graphiques PowerPoint natifs (modifiables).

---

## Phase 9 — Dashboard (25/09, première version)

`dashboard/app.py` — lancer avec `streamlit run dashboard/app.py`.

- **Filtres** (barre latérale) : période, compagnies, heures de départ, jours de la semaine.
- **5 KPI** : vols sélectionnés, % en retard (avec écart à l'ensemble), retard moyen des vols en retard, % annulés, effet domino (× combien).
- **5 onglets** : Vue générale (heure, jour, jour par jour, carte jour × heure) · Effet domino · Comparer deux compagnies · Destinations (bulles + nuage départ/arrivée) · Insights et limites.
- **Garde-fous** : les pourcentages calculés sur trop peu de vols sont masqués (ex. effet domino si < 100 vols dans un groupe) pour ne pas afficher de résultat trompeur.

**Tests réalisés** (outil `AppTest` de Streamlit, qui simule les clics) : 15 combinaisons de filtres
(une compagnie, aucune compagnie, une seule date, un seul jour, heures du matin, du soir, comparaison d'une compagnie avec elle-même…) :
**aucune erreur**.

---

## Phase 10 — Tests et design du dashboard (26/09)

- Captures de chaque onglet prises automatiquement (Chrome piloté par script) → `reports/captures/`.
- Corrections après relecture des captures : étiquettes coupées (graphique des jours), décimales à l'anglaise
  (37.1 → 37,1), noms de destinations qui se chevauchaient (seules les destinations extrêmes sont nommées,
  les autres au survol), libellés des indicateurs trop longs, écart « 0,0 pts » affiché sans filtre.
- Thème aux couleurs du projet (`.streamlit/config.toml`).

## Phase 11 — Rapport (26/09)

`reports/rapport.pdf` (6 pages, A4), généré depuis `reports/rapport.html` (modifiable, puis réimprimer en PDF depuis Chrome :
Ctrl+P → « Enregistrer au format PDF », marges par défaut, graphiques d'arrière-plan cochés).
Plan du cahier des charges : introduction · dataset et méthodologie · analyse · dashboard · insights · limites · conclusion.

## Phase 12 — Présentation orale finale (26/09)

`presentation/presentation_finale.pptx` : 12 slides qui suivent le minutage de la section 24 (indiqué en bas à gauche de chaque slide).
**Le texte complet à dire est dans les notes** ; la slide 9 contient le scénario de démonstration du dashboard.

| Minutes | Slides |
|---|---|
| 0:00 – 1:00 | 1 Titre · 2 Le problème |
| 1:00 – 2:00 | 3 Dataset |
| 2:00 – 4:00 | 4 Méthodologie · 5 Échantillonnage |
| 4:00 – 6:00 | 6 Heure · 7 Effet domino · 8 Profils |
| 6:00 – 8:30 | 9 Démonstration du dashboard |
| 8:30 – 9:30 | 10 Insights |
| 9:30 – 10:00 | 11 Conclusion et limites · 12 Questions |

## Phase 13 — Mise en ligne (26/09, préparée)

- Dépôt git local avec un historique propre (un commit par étape).
- `dashboard/requirements.txt` léger pour Streamlit Community Cloud.
- Guide pas à pas : `docs/MISE_EN_LIGNE.md` (créer le dépôt GitHub, `git push`, déployer sur share.streamlit.io).

---

## Compléments après comparaison avec un autre cahier des charges (26/09)

Comparaison avec le cahier des charges d'un·e camarade du module ; ajouts retenus selon trois niveaux de priorité
(on reste au niveau Bac+2, sans complexité inutile) :

| Ajout | Où |
|---|---|
| 2 méthodes d'échantillonnage de plus : **stratifié non proportionnel** et **bootstrap** (7 au total) | `src/sampling.py`, notebook section 8 |
| Analyse de chaque échantillon : doublons, manquants, retards extrêmes, jours couverts | `indicateurs()`, notebook 9.1 |
| **Erreurs absolue et relative**, **score de représentativité**, **classement** sur 100 tirages | notebook 9.2-9.3, rapport, slide 5 |
| Repondération du stratifié non proportionnel (25,8 % → 26,1 %, population 26,2 %) | notebook 9.4 |
| **43 tests automatiques** (`pytest`) | `tests/` |
| Onglets **Échantillonnage** (méthode, taille, graine au choix, comparaison en direct, classement) et **Qualité des données** | dashboard |

Non retenus (volontairement) : tests de Kolmogorov-Smirnov et du khi-deux, intervalles de confiance (plus avancés, à
expliquer à l'oral) ; réorganisation complète du projet en pages multiples (beaucoup de risque avant le rendu, peu de gain).

---

## Ce qui reste à faire

- [ ] Relire le notebook, le rapport et les deux présentations ; poser toutes les questions
- [ ] Répéter l'oral (10 min chrono) avec la démo du dashboard
- [ ] Publier sur GitHub et Streamlit Cloud (`docs/MISE_EN_LIGNE.md`), puis ajouter le lien au README
- [ ] Ajouter le projet sur LinkedIn et dans le CV
