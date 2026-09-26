# Ce que je dois apprendre et savoir expliquer

Le professeur a prévenu : **il faut comprendre chaque morceau du projet.** Ce fichier est mon guide de révision.
Conseil : le lire dans l'ordre, puis ouvrir le notebook et relancer chaque cellule en vérifiant que je comprends.

---

## 1. Le projet en 30 secondes (pour le prof ET pour un entretien de stage)

> « J'ai analysé 54 000 vols au départ d'Atlanta, le plus grand aéroport du monde, pendant l'été 2022, avec des données
> officielles du gouvernement américain. J'ai découvert que le retard grandit au fil de la journée : 12 % des vols
> du matin sont en retard contre 40 % le soir, parce que les retards se transmettent d'un vol à l'autre du même avion.
> Quand le vol précédent d'un avion est en retard, le suivant l'est une fois sur deux. J'ai construit un dashboard
> interactif en Python pour explorer ces résultats par compagnie, par heure et par jour. C'est le même problème que
> la ponctualité des bus que j'ai observée pendant mon stage chez ALSA. »

---

## 2. Les notions de statistique à maîtriser

### Types de variables
- **Numérique** : un nombre qu'on peut additionner ou moyenner (retard en minutes, distance).
- **Catégorielle** : un groupe, une étiquette (compagnie, destination). On compte, on compare des groupes.
- **Temporelle** : une date ou une heure (`FlightDate`).
- **Booléenne (vrai/faux)** : `Cancelled`, `Diverted`.

### Moyenne vs médiane — **question très probable**
- **Moyenne** = somme / nombre. Sensible aux valeurs extrêmes.
- **Médiane** = la valeur du milieu quand on trie. 50 % des vols sont en dessous, 50 % au-dessus.
- Chez nous : médiane = **0 min**, moyenne = **16 min**. Quelques vols avec 10-40 h de retard tirent la moyenne vers le haut.
- **C'est pour ça qu'on utilise le « % de vols en retard »** : il n'est pas déformé par les extrêmes, et c'est la définition officielle.

### Distribution asymétrique
Beaucoup de valeurs près de 0, et une « longue traîne » vers la droite (quelques très gros retards). Voir l'histogramme 10.2.

### Outliers et règle de l'IQR
- Q1 = 25e percentile (−3 min), Q3 = 75e percentile (16 min), **IQR = Q3 − Q1 = 19 min**.
- Outlier si > Q3 + 1,5 × IQR = **44,5 min** → ≈ 12 % des vols.
- **On les garde** : ce ne sont pas des erreurs, ce sont de vrais retards — le phénomène qu'on étudie.

### Corrélation
- Nombre entre −1 et 1. Proche de 1 : les deux variables montent ensemble. Proche de 0 : pas de lien **linéaire**.
- Retard départ / arrivée : **0,98** (très fort). Distance / retard : **0,01** (aucun lien).
- **Corrélation ≠ causalité** : deux choses qui varient ensemble n'ont pas forcément une cause à effet.
  Exemple : les glaces et les coups de soleil augmentent ensemble… à cause du soleil.

### Heatmap
Tableau coloré : plus la case est foncée, plus la valeur est grande. On l'utilise pour croiser **deux** variables
(jour × heure) avec une troisième en couleur (% de retard).

---

## 3. L'échantillonnage — **partie importante de la note**

**Population** = les 54 461 vols. **Échantillon** = une partie (≈ 5 000 vols).
**Représentatif** = l'échantillon ressemble à la population (mêmes proportions, même moyenne…).

| Méthode | Comment | Avantage | Inconvénient |
|---|---|---|---|
| **Aléatoire simple** | Tirer 5 000 vols au hasard | Simple, sans biais | Peut, par hasard, oublier un petit groupe |
| **Systématique** | Trier par date, prendre 1 vol sur 11 | Couvre toute la période régulièrement | Problème si les données ont un cycle de même pas |
| **Stratifié proportionnel** | Même **%** dans chaque groupe (compagnie) | Chaque groupe à sa vraie part (Delta 66 %) | Il faut connaître les groupes à l'avance |
| **Stratifié non proportionnel** | Même **nombre** de vols (625) dans chaque compagnie | Assez de vols pour étudier les petites compagnies | **Biaisé** pour décrire la population (Delta 12,5 %) → il faut **repondérer** |
| **Par grappes** | Tirer des jours entiers | Pratique pour collecter | **Instable** si les grappes sont différentes entre elles |
| **Stratifié temporel** | Même % dans chacun des 61 jours | Tous les jours présents | — |
| **Bootstrap** | Tirer 5 000 vols au hasard **avec remise** | Base du ré-échantillonnage (mesurer la variabilité) | Contient des doublons (un vol tiré plusieurs fois) |

**Comment je mesure la représentativité** (à savoir expliquer) :
- **Erreur absolue** = |valeur de l'échantillon − valeur de la population|. Ex. : 26,51 % − 26,25 % = 0,26 point.
- **Erreur relative** = erreur absolue / valeur de la population × 100. Ex. : 0,26 / 26,25 × 100 = 1 %.
  Elle permet de comparer des indicateurs d'unités différentes (minutes, %).
- **Score de représentativité** = 100 − moyenne des erreurs relatives sur 6 indicateurs. 100 = identique à la population.
- Le **retard médian** n'est pas dans le score : il vaut 0 dans la population, et on ne peut pas diviser par 0.
- Petit piège : le **% d'annulés** (1,9 %) a souvent la plus grosse erreur relative, car un petit écart sur un petit
  pourcentage donne une grande erreur relative.

**Classement (score moyen sur 100 tirages)** : systématique 96,7 · stratifié compagnie 96,1 · **stratifié par jour 96,0
(retenu)** · aléatoire 95,8 · bootstrap 95,7 · grappes 84,8 · non proportionnel 71,8.

**Mon résultat clé :** en répétant 100 fois chaque tirage, les grappes donnent de 18 % à 36 % de retard,
les autres méthodes restent à 26 % ± 1. **Pourquoi ?** Parce que les jours sont très différents (10 % à 63 % de retard) :
6 jours tirés au hasard peuvent tomber sur des jours d'orage.

**Repondération** : dans le non proportionnel, chaque vol reçoit un poids = (vols de sa compagnie dans la population) /
(vols de sa compagnie dans l'échantillon). Sur 100 tirages : 25,8 % sans poids (biais), 26,1 % avec poids (population 26,2 %).

**`random_state = 42`** : fixe le hasard pour obtenir le même tirage à chaque exécution (**reproductibilité**).

**Choix du périmètre ≠ échantillonnage** : garder Atlanta en juin-juillet, c'est choisir mon sujet.
L'échantillonnage vient après, sur ces 54 461 vols.

---

## 4. Le code, fichier par fichier

Tout est en Python avec **pandas** (tableaux), **matplotlib/seaborn** (graphiques fixes), **plotly** (graphiques interactifs)
et **streamlit** (dashboard).

### `src/data_loading.py` — charger les données
- `pd.read_parquet(fichier, filters=[...])` : lit le gros fichier en ne gardant que les lignes voulues (Atlanta, juin-juillet).
- `.to_csv(...)` : enregistre en CSV.
- `pd.read_csv(..., parse_dates=["FlightDate"])` : relit le CSV en transformant la colonne en vraie date.

### `src/preprocessing.py` — nettoyer
- `vols[col].nunique()` : nombre de valeurs différentes. Si = 1 → colonne constante → supprimée avec `.drop(columns=...)`.
- `.drop_duplicates()` : supprime les doublons (il n'y en a pas).
- `vols["CRSDepTime"] // 100` : division entière. 1435 // 100 = 14 → l'heure.
- `.map({1: "Lundi", ...})` : remplace chaque valeur grâce à un dictionnaire.
- **Effet domino** (la partie la plus technique, à bien comprendre) :
  1. `sort_values(["Tail_Number", "FlightDate", "CRSDepTime"])` : on range les vols **par avion, puis par jour, puis par heure** ;
  2. `groupby(["Tail_Number", "FlightDate"])` : on fait des paquets « un avion, un jour » ;
  3. `cumcount() + 1` : numérote les vols dans chaque paquet (1er, 2e, 3e…) → `rang_rotation` ;
  4. `["DepDel15"].shift(1)` : pour chaque vol, prend la valeur **du vol juste avant dans le même paquet** → `vol_precedent_en_retard`.
     Le premier vol de la journée n'a pas de vol précédent → valeur vide (NaN).

### `src/sampling.py` — échantillonner
- `vols.sample(n=5000, random_state=42)` : tirage aléatoire simple.
- `vols.groupby("compagnie").sample(frac=0.09)` : tirage stratifié proportionnel (9 % dans chaque compagnie).
- `groupe.sample(n=625)` pour chaque compagnie : stratifié non proportionnel (même nombre partout).
- `vols.sample(n=5000, replace=True)` : bootstrap (`replace=True` = avec remise, doublons possibles).
- `.iloc[positions]` : sélectionne des lignes par leur position (systématique).
- `vols[vols["FlightDate"].isin(jours_tires)]` : garde les vols des jours tirés (grappes).

### `src/analysis.py` — calculer
- `groupby(colonne).agg(...)` : pour chaque groupe, calcule nombre de vols, % en retard, médiane.
- `DepDel15.mean() * 100` : comme `DepDel15` vaut 0 ou 1, **sa moyenne est la proportion de vols en retard**. Astuce clé !
- `pivot_table(index=..., columns=..., values=..., aggfunc="mean")` : tableau croisé (utilisé pour les heatmaps).

### `src/visualizations.py` — le style des graphiques
- Les couleurs du projet et une fonction `appliquer_style()` qui enlève le superflu (data-ink ratio).

### `dashboard/app.py` — le dashboard
- `st.sidebar.multiselect(...)`, `st.sidebar.slider(...)` : les filtres.
- `st.metric(...)` : les KPI.
- `st.tabs([...])` : les onglets.
- `@st.cache_data` : ne charge le fichier qu'une fois (plus rapide).
- `st.plotly_chart(...)` : affiche un graphique interactif.

---

## 5. Principes de visualisation appliqués (à citer à l'oral)

| Principe | Où je l'ai appliqué |
|---|---|
| **Data-ink ratio** | Pas de cadre, grille légère, pas de 3D, pas de décoration |
| **Attributs pré-attentifs** | La couleur orange attire l'œil sur ce qui compte (retard, pire compagnie) ; le reste en bleu/gris |
| **Couleurs cohérentes** | Bleu = vols, orange = retard, partout (notebook, slides, dashboard). Palette testée pour les daltoniens |
| **Titres explicites** | Le titre dit la conclusion : « Le retard s'accumule au fil de la journée », pas « Graphique 3 » |
| **Unités** | Minutes, %, miles indiqués sur les axes |
| **Bon graphique pour le bon type** | Ligne pour le temps, barres pour comparer des catégories, nuage de points pour 2 nombres, heatmap pour 2 catégories + 1 valeur |
| **Pas de camembert** | 8 compagnies → barres horizontales triées, plus faciles à comparer |
| **Barres horizontales** | Les noms longs (compagnies) restent lisibles |
| **Lisibilité des nuages de points** | Échantillon de 5 000 points + transparence |

---

## 6. Questions probables du professeur — et mes réponses

**Pourquoi ce dataset ?**
Données officielles et réelles, riches (61 colonnes), dans le transport (mon domaine de stage), et qui permettent un angle
original grâce à l'immatriculation des avions : l'effet domino.

**Pourquoi Atlanta en juin-juillet ?**
Aéroport le plus fréquenté du monde, période de pic des retards, et au moins 30 000 lignes (juillet seul = 27 533).
Un seul aéroport permet de suivre le même avion dans la journée.

**Pourquoi cette problématique ?**
Parce que la ponctualité est l'indicateur n°1 d'un transporteur, et que comprendre *quand* et *comment* le retard apparaît
permet d'agir (protéger les premiers vols du matin).

**Comment avez-vous traité les valeurs manquantes ?**
Je les ai analysées : elles correspondent toutes aux vols annulés ou déviés (un vol annulé n'a pas d'heure de départ).
Je ne les ai pas remplies, car inventer un retard pour un vol annulé n'aurait pas de sens.

**Pourquoi avez-vous supprimé ces colonnes ?**
Seulement 10 colonnes, toutes **constantes** (ex. ville de départ = Atlanta pour toutes les lignes) : elles n'apportent aucune information.

**Pourquoi garder les outliers ?**
Ce sont de vrais vols très en retard, pas des erreurs de saisie. Les supprimer effacerait une partie du phénomène.
J'utilise des indicateurs robustes (médiane, % en retard) pour qu'ils ne déforment pas l'analyse.

**Pourquoi ce type d'échantillonnage ? Votre échantillon est-il représentatif ?**
J'ai comparé 7 méthodes à la population avec l'erreur absolue, l'erreur relative et un score de représentativité,
sur un tirage puis sur 100 tirages. J'ai retenu le stratifié par jour : score moyen 96,0 (groupe de tête), % de retard
26,5 % contre 26,2 % dans la population, part de Delta 67 % contre 66 %, les 61 jours présents.
Les grappes sont instables (18-36 %) car les jours sont très différents ; le non proportionnel est biaisé par construction.

**Pourquoi le systématique est premier et vous ne l'avez pas choisi ?**
L'écart est très faible (96,7 contre 96,0). J'ai préféré le stratifié par jour car il **garantit** que chacun des 61 jours
est représenté, et il a l'écart-type le plus faible du % de retard (0,52 point). Les deux choix sont défendables.

**Pourquoi le bootstrap a des doublons ?**
Parce qu'il tire **avec remise** : un vol tiré peut être tiré à nouveau. Sur 5 000 tirages parmi 54 461 vols, environ
230 vols sortent deux fois. C'est normal et voulu.

**Comment avez-vous testé le code ?**
43 tests automatiques avec `pytest` (dossier `tests/`) : taille des échantillons, proportions stratifiées conservées,
doublons du bootstrap, grappes complètes, pourcentages entre 0 et 100, fichier brut jamais modifié, démarrage du dashboard,
filtres qui changent réellement les résultats. Commande : `python -m pytest`.

**Pourquoi un scatter plot ici ?**
Pour montrer la relation entre deux variables numériques (retard au départ et à l'arrivée). J'utilise l'échantillon
pour que les points ne se superposent pas en une tache.

**Que montre la corrélation ?**
0,98 entre retard au départ et à l'arrivée : le retard se conserve. 0,01 avec la distance : aucun lien.
Mais une corrélation ne prouve pas une cause.

**Pourquoi ces couleurs ?**
Palette limitée : bleu pour les vols en général, orange pour mettre en avant le retard. Toujours les mêmes, pour que
le lecteur les apprenne une fois. Palette vérifiée pour les personnes daltoniennes.

**Pourquoi Streamlit ?**
Imposé par le cahier des charges, et adapté : tout en Python, filtres simples à créer, déploiement gratuit en ligne.

**Quelle est votre principale découverte ?**
L'effet domino : si le vol précédent du même avion était en retard, le suivant l'est 2 fois plus souvent (50 % contre 24 %),
et c'est vrai à chaque heure de la journée.

**Peut-on parler de causalité ?**
Non, pas à partir de ces données seules. Les deux vols d'un même avion partagent la même journée (météo, affluence).
L'effet domino est très plausible et reconnu officiellement par le BTS (cause « Aircraft Arriving Late »), mais mes données
montrent une association, pas une preuve.

**Quelles sont les limites ?**
Un seul aéroport, deux mois d'été ; pas de météo ; je ne vois pas les vols retour vers Atlanta entre deux départs ;
Delta fait 66 % des vols ; associations et non causalité.

**Que changeriez-vous avec plus de données ?**
Ajouter la météo heure par heure, les causes officielles de retard (dans les fichiers bruts), une année complète pour
comparer les saisons, et les vols arrivant à Atlanta pour suivre la chaîne complète de chaque avion.

---

## 7. Les chiffres à connaître par cœur

| Chiffre | Signification |
|---|---|
| **54 461** vols, **61** colonnes | Taille du dataset |
| **26 %** | Vols en retard (> 15 min) |
| **0 min / 16 min** | Retard médian / moyen |
| **12 % → 40 %** | Retard le matin → le soir |
| **24 % → 50 %** | Retard si le vol précédent était à l'heure → en retard (**effet domino**) |
| **0,98** | Corrélation retard départ / arrivée |
| **37 % / 18 %** | Southwest / Endeavor |
| **10 % → 63 %** | Jour le plus calme → le pire (21 juillet) |
| **66 %** | Part de Delta dans les vols |
| **7** méthodes · **96,0** | Méthodes d'échantillonnage · score de l'échantillon retenu (stratifié par jour) |
| **43** | Tests automatiques qui passent |
