# CAHIER DES CHARGES — PROJET FINAL DE VISUALISATION DES DONNÉES

> Copie fidèle du cahier des charges fourni le 25/09/2026. Document de référence du projet :
> toute décision doit rester cohérente avec ce texte.

## 0. CONTEXTE PERSONNEL ET OBJECTIF CARRIÈRE — À LIRE EN PREMIER

Je suis étudiante en **2e année, fin de cycle**, et j'obtiens cette année le diplôme de **technicienne en ingénierie des données**. Je recherche un **stage pour avril**, puis un **emploi juste après**.

Ce projet n'est donc PAS seulement un projet scolaire noté. Il doit aussi servir de **pièce de portfolio** pour mes candidatures (stage puis emploi). Cet objectif ne doit jamais réduire la rigueur académique ni la qualité de l'analyse attendues par le professeur — il s'ajoute aux exigences ci-dessous, sans les remplacer.

Conséquences concrètes sur la façon de travailler le projet :

1. **Le code doit être lisible par un recruteur technique**, pas seulement fonctionnel pour un rendu de notes. Noms de variables clairs, fonctions bien séparées, pas de code mort, commentaires utiles (voir section 26, renforcée).
2. **Le dépôt doit être hébergé sur GitHub, en public**, avec un historique de commits propre (des messages clairs, pas "update" ou "fix" répétés).
3. **Le README doit fonctionner comme un mini-CV technique** : contexte, problématique, dataset, méthodologie, captures d'écran du dashboard, lien vers le dashboard déployé, technologies utilisées. Il doit être compréhensible par quelqu'un qui n'a que 2 minutes.
4. **Le dashboard Streamlit doit être déployé en ligne** (Streamlit Community Cloud, gratuit), pas seulement lancé en local. Un lien cliquable dans un CV ou un profil LinkedIn a beaucoup plus de valeur qu'une instruction "cloner le repo et lancer streamlit run".
5. **Le sujet et l'angle d'analyse doivent, si possible, rester défendables à l'oral en entretien de stage/embauche**, pas seulement devant le professeur. Éviter un sujet qui n'aurait de sens que dans un cadre scolaire.
6. **Le calendrier est contraint** : le projet doit être terminé, déployé et prêt à être montré (GitHub + dashboard en ligne) **avant la période de candidatures de stage**, donc idéalement finalisé en février-mars.

Cet objectif carrière NE change PAS le niveau académique attendu (voir section 19 : rester un projet de Bac+2, réalisable, sans complexité artificielle). Il change seulement le soin apporté à la présentation, au code, et à la mise en ligne.

### 0.1 Domaine choisi

Le domaine retenu pour ce projet est **mobilité / transport**. Ce choix est cohérent avec mon stage effectué chez ALSA Agadir City (entreprise de transport), ce qui donne une accroche naturelle en entretien de stage/embauche. Rechercher les datasets Kaggle candidats en priorité dans ce domaine (trajets, transport public, trafic urbain, mobilité partagée, retards de transport, etc.), avant d'envisager un domaine alternatif si aucun dataset satisfaisant n'est trouvé.

### 0.2 Calendrier réel du projet — À RESPECTER STRICTEMENT

- **Durée totale disponible : 3 semaines.**
- **Premier rendu d'étape : lundi prochain.** Pour ce premier rendu, il faut avoir :
  1. Un dataset choisi et justifié (Phase 1 terminée).
  2. Une problématique et des sous-questions définies (Phase 2 terminée).
  3. Idéalement, une exploration initiale des données commencée (début de Phase 3).
  4. **Une présentation PowerPoint (.pptx)** de ce premier état d'avancement, à rendre en même temps que ce point d'étape. Cette présentation est distincte de la présentation orale finale de 10 minutes (section 24) : c'est un livrable intermédiaire, plus court, qui montre le dataset choisi, la problématique, et les premières observations.
- Le reste du projet (nettoyage, échantillonnage, analyses univariée/bivariée/multivariée, storytelling, dashboard, rapport, mise en ligne) doit être réparti sur les 2 semaines restantes après ce premier rendu.

**Conséquence pour la méthode de travail (section 27) :** prioriser les Phases 1 et 2 dès le début, en laissant du temps pour préparer le support PowerPoint du premier rendu, avant d'enchaîner sur les phases suivantes.

---

## 1. CONTEXTE — IMPORTANT

Ce projet correspond au projet final du module de Visualisation des Données en Bac+2 / DUT Ingénierie des Données.

La qualité de ce projet est très importante car il compte pour la note finale du module.

Je ne veux donc PAS un projet scolaire banal qui se limite à :

- charger un CSV ;
- faire quelques histogrammes ;
- afficher une heatmap ;
- créer quelques KPI ;
- mettre le tout dans un dashboard.

Je veux construire un projet qui donne l'impression d'un vrai projet de Data Visualization / Data Analysis, avec :

- une problématique intéressante ;
- un dataset suffisamment riche ;
- une histoire à raconter avec les données ;
- des visualisations choisies pour répondre à des questions précises ;
- plusieurs niveaux d'analyse ;
- un dashboard interactif réellement utile ;
- une identité visuelle cohérente ;
- des conclusions basées sur les données ;
- une présentation orale convaincante.

### OBJECTIF PRINCIPAL

Le projet doit être intéressant, singulier et différent des projets classiques des autres étudiants, tout en restant parfaitement réalisable par une étudiante de Bac+2.

L'originalité ne doit PAS venir d'une complexité artificielle.

Elle doit venir principalement :

1. du choix du dataset ;
2. de la problématique ;
3. de l'angle d'analyse ;
4. de la manière de raconter les données ;
5. de la qualité des visualisations ;
6. de l'interactivité du dashboard.

---

## 2. CONTRAINTES DU DATASET

La consigne actuelle donnée par l'étudiant/professeur est :

- dataset provenant de Kaggle ;
- au moins 30 000 lignes ;
- au moins 50 colonnes ;
- présence de variables numériques ET catégorielles ;
- dataset suffisamment riche pour permettre plusieurs types d'analyses.

IMPORTANT :

Ne pas choisir un dataset simplement parce qu'il possède beaucoup de colonnes.

Le dataset doit permettre de construire une problématique intéressante.

Éviter les datasets extrêmement classiques utilisés dans les tutoriels et projets étudiants, par exemple :

- Titanic ;
- Iris ;
- simple Student Performance ;
- simple Supermarket Sales ;
- simple House Prices ;
- datasets trop petits ;
- datasets artificiellement générés sans intérêt analytique ;
- datasets dont l'analyse se résume à une variable cible.

Privilégier un domaine permettant une vraie histoire de données, par exemple :

- mobilité ;
- transport ;
- comportement des consommateurs ;
- e-commerce ;
- environnement ;
- énergie ;
- tourisme ;
- événements ;
- services urbains ;
- logistique ;
- santé publique ;
- réseaux sociaux ;
- livraison ;
- comportements humains ;
- économie ;
- sécurité ;
- sport ;
- phénomènes temporels.

Le domaine exact doit être choisi en fonction des datasets réellement disponibles, **et si possible, en fonction d'un domaine qui pourrait m'intéresser professionnellement (voir section 0)**, ce qui donne une meilleure accroche en entretien.

---

## 3. RECHERCHE DU DATASET

Avant d'écrire le code du projet, rechercher plusieurs datasets Kaggle correspondant aux contraintes.

Pour chaque candidat, analyser :

- nombre de lignes ;
- nombre de colonnes ;
- types de variables ;
- variables numériques ;
- variables catégorielles ;
- présence éventuelle de dates ;
- variables géographiques éventuelles ;
- variables temporelles ;
- valeurs manquantes ;
- doublons ;
- richesse des relations entre variables ;
- potentiel pour analyses univariées ;
- potentiel pour analyses bivariées ;
- potentiel pour analyses multivariées ;
- potentiel pour dashboard ;
- potentiel de storytelling ;
- originalité du sujet.

Ne pas choisir automatiquement le premier dataset trouvé.

Faire une comparaison des candidats et expliquer clairement pourquoi le dataset final permet de construire un projet original.

---

## 4. PROBLÉMATIQUE

Une fois le dataset choisi, ne pas commencer directement par les graphiques.

Commencer par définir une problématique centrale.

La problématique doit être formulée comme une vraie question d'analyse.

Exemple de structure :

« Quels facteurs permettent d'expliquer / comprendre / comparer / détecter X dans le contexte Y ? »

La problématique doit permettre de construire plusieurs sous-questions.

Par exemple :

**Question principale** — Quel phénomène cherche-t-on à comprendre ?

**Sous-question 1** — Comment le phénomène évolue-t-il ?

**Sous-question 2** — Quelles catégories ou groupes présentent les différences les plus importantes ?

**Sous-question 3** — Existe-t-il des relations entre certaines variables ?

**Sous-question 4** — Existe-t-il des profils ou comportements différents ?

**Sous-question 5** — Quels facteurs semblent associés au phénomène étudié ?

Les questions doivent être directement liées aux variables disponibles dans le dataset.

---

## 5. ÉCHANTILLONNAGE

Le projet doit intégrer plusieurs méthodes d'échantillonnage.

IMPORTANT :

Ne pas appliquer des méthodes d'échantillonnage uniquement pour « remplir une obligation ».

Pour chaque méthode :

- expliquer son principe ;
- expliquer pourquoi elle est utilisée ;
- montrer comment elle est appliquée ;
- comparer l'échantillon obtenu avec le dataset complet ;
- vérifier si l'échantillon reste représentatif.

Étudier plusieurs approches pertinentes, par exemple :

1. Échantillonnage aléatoire simple
2. Échantillonnage systématique
3. Échantillonnage stratifié
4. Échantillonnage par grappes / clusters
5. Une méthode supplémentaire pertinente au dataset, éventuellement temporelle si les données contiennent une dimension temporelle.

Ne pas utiliser une méthode si elle n'a pas de sens pour le dataset.

Pour chaque méthode, calculer et/ou visualiser des indicateurs permettant de comparer l'échantillon au dataset complet.

Par exemple :

- distribution des variables principales ;
- proportions des catégories ;
- moyenne / médiane ;
- dispersion ;
- distribution temporelle ;
- distribution de la variable principale.

Créer une petite section « Comparaison des échantillons ».

---

## 6. ENVIRONNEMENT TECHNIQUE

Le projet doit être développé principalement en Python.

Utiliser autant que nécessaire :

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

Le notebook doit être réalisé avec Jupyter Notebook ou environnement équivalent.

Le dashboard doit être développé avec Streamlit, sauf raison technique sérieuse justifiant une autre solution.

Le code doit être propre, structuré et compréhensible.

---

## 7. ORGANISATION DU PROJET

Créer une structure professionnelle similaire à :

```
data-viz-project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── data_loading.py
│   ├── preprocessing.py
│   ├── sampling.py
│   ├── analysis.py
│   └── visualizations.py
│
├── dashboard/
│   └── app.py
│
├── reports/
│   └── rapport.pdf
│
├── presentation/
│   └── presentation.pptx
│
├── requirements.txt
└── README.md
```

Adapter la structure si le projet l'exige, mais garder une organisation claire.

**Ajout objectif carrière :** ce dépôt sera hébergé sur GitHub en public (voir section 31). Le README.md à la racine doit être pensé dès le départ comme la première chose qu'un recruteur verra.

---

## 8. EXPLORATION DES DONNÉES

Commencer par une exploration complète.

Inclure :

- dimensions du dataset ;
- aperçu des premières lignes ;
- types des variables ;
- description statistique ;
- variables numériques ;
- variables catégorielles ;
- variables temporelles ;
- valeurs manquantes ;
- doublons ;
- valeurs aberrantes ;
- cardinalité des variables catégorielles ;
- distributions principales ;
- éventuelles incohérences.

Créer un résumé clair de la qualité des données.

Exemple :

| Élément | Résultat |
|---|---|
| Nombre de lignes | ... |
| Nombre de colonnes | ... |
| Variables numériques | ... |
| Variables catégorielles | ... |
| Valeurs manquantes | ... |
| Doublons | ... |
| Variables temporelles | ... |

---

## 9. NETTOYAGE DES DONNÉES

Effectuer uniquement les transformations réellement nécessaires.

Traiter :

- valeurs manquantes ;
- doublons ;
- types incorrects ;
- valeurs aberrantes ;
- catégories incohérentes ;
- dates mal formatées ;
- colonnes inutiles.

IMPORTANT :

Ne jamais supprimer une colonne ou une observation sans expliquer pourquoi.

Conserver autant que possible le dataset original et créer une version nettoyée.

Documenter les décisions de nettoyage.

---

## 10. ANALYSE UNIVARIÉE

Réaliser une analyse univariée suffisamment riche.

Selon les variables disponibles :

**Variables numériques** — Utiliser par exemple :
- histogrammes ;
- KDE si pertinent ;
- boxplots ;
- statistiques descriptives.

**Variables catégorielles** — Utiliser :
- bar charts ;
- proportions ;
- classement des catégories.

Ne pas produire 30 graphiques simplement parce que le dataset possède 50 colonnes.

Sélectionner les variables les plus pertinentes pour la problématique.

Chaque visualisation doit répondre à une question.

Pour chaque graphique, ajouter une courte interprétation :

« Cette visualisation montre que... »

L'objectif est de transformer les graphiques en insights, pas seulement de les afficher.

---

## 11. ANALYSE BIVARIÉE

Étudier les relations entre deux variables.

Selon le dataset :

- numérique × numérique → scatter plot ;
- catégorielle × numérique → boxplot / violin plot / bar chart ;
- catégorielle × catégorielle → stacked bar / grouped bar ;
- temporelle × numérique → line chart ;
- corrélations → heatmap.

Ne pas utiliser automatiquement une heatmap de corrélation avec toutes les colonnes.

Sélectionner les relations pertinentes.

Pour chaque relation importante :

1. présenter la visualisation ;
2. décrire le résultat ;
3. interpréter prudemment ;
4. préciser que corrélation ≠ causalité lorsque nécessaire.

---

## 12. ANALYSE MULTIVARIÉE

Cette partie doit être particulièrement intéressante.

Chercher des relations impliquant plusieurs dimensions.

Exemples :

- X + Y + catégorie ;
- évolution temporelle + catégorie + mesure ;
- plusieurs variables numériques ;
- profils de groupes ;
- interactions entre plusieurs facteurs.

Utiliser selon la pertinence :

- pairplot ;
- scatter plots avec couleur/taille ;
- facettes ;
- heatmaps ;
- parallel coordinates ;
- bubble charts ;
- visualisations Plotly interactives.

Ne pas surcharger les graphiques.

La lisibilité est prioritaire.

---

## 13. STORYTELLING

Le projet doit suivre une histoire logique.

Ne pas présenter :

« Graphique 1 → Graphique 2 → Graphique 3 → Graphique 4 »

sans logique.

Construire plutôt une progression :

**Étape 1 — Comprendre le phénomène** — « Que se passe-t-il ? »

**Étape 2 — Identifier les différences** — « Où / quand / chez qui cela se produit-il ? »

**Étape 3 — Chercher les facteurs associés** — « Quelles variables semblent liées au phénomène ? »

**Étape 4 — Identifier des profils** — « Quels groupes ou comportements apparaissent ? »

**Étape 5 — Synthétiser** — « Quelles conclusions peut-on tirer des données ? »

Chaque graphique doit avoir une fonction dans cette histoire.

---

## 14. PRINCIPES DE VISUALISATION

Appliquer réellement les principes vus dans le cours :

- Data-Ink Ratio ;
- hiérarchie visuelle ;
- attributs pré-attentifs ;
- couleurs cohérentes ;
- titres explicites ;
- labels compréhensibles ;
- unités ;
- légendes utiles ;
- suppression des éléments décoratifs inutiles ;
- choix du graphique adapté au type de données.

Éviter :

- graphiques 3D inutiles ;
- camemberts lorsque plusieurs catégories rendent la lecture difficile ;
- couleurs excessives ;
- graphiques surchargés ;
- titres vagues comme « Graphique 1 » ;
- axes sans unité ;
- palettes incohérentes.

---

## 15. DASHBOARD INTERACTIF

Le dashboard représente une partie très importante du projet.

Il doit être pensé comme une interface d'analyse, pas comme une collection de graphiques.

Utiliser Streamlit.

**Structure proposée**

**HEADER** — Nom du projet + problématique principale.

**SECTION 1 — KPIs** — Afficher 3 à 5 KPI réellement utiles. Par exemple : volume total ; moyenne ; médiane ; évolution ; taux ; nombre de catégories ; indicateur spécifique au domaine. Les KPI doivent être directement liés à la problématique.

**SECTION 2 — VUE GÉNÉRALE** — Quelques visualisations permettant de comprendre rapidement le phénomène.

**SECTION 3 — EXPLORATION** — Filtres dynamiques : catégorie ; période ; région ; type ; groupe ; variable pertinente. Les filtres doivent réellement modifier les graphiques.

**SECTION 4 — ANALYSE** — Graphiques plus détaillés.

**SECTION 5 — COMPARAISON** — Permettre à l'utilisateur de comparer différents groupes.

**SECTION 6 — INSIGHTS** — Afficher quelques conclusions importantes issues des analyses.

**Ajout objectif carrière :** ce dashboard sera déployé en ligne (voir section 31) — le concevoir en gardant à l'esprit qu'un inconnu (recruteur) doit pouvoir le comprendre et l'utiliser sans aucune explication orale préalable.

---

## 16. INTERACTIVITÉ

Le dashboard doit contenir de vraies interactions.

Exemples :

- dropdown ;
- multiselect ;
- slider ;
- sélection de période ;
- sélection de catégorie ;
- comparaison entre groupes ;
- graphiques Plotly interactifs ;
- tooltips ;
- zoom ;
- filtres liés.

Éviter les interactions artificielles.

Chaque interaction doit permettre à l'utilisateur de répondre à une question.

---

## 17. DESIGN DU DASHBOARD

Créer une identité visuelle cohérente.

Le dashboard doit être :

- moderne ;
- propre ;
- lisible ;
- professionnel ;
- sobre ;
- cohérent avec le sujet.

Utiliser une palette limitée.

Hiérarchie :

```
Titre
 ↓
Problématique
 ↓
KPIs
 ↓
Vue générale
 ↓
Exploration
 ↓
Analyse détaillée
 ↓
Insights
```

Ne pas mettre 15 graphiques sur une seule page.

Si nécessaire, utiliser plusieurs sections/tabs.

---

## 18. NOTE IMPORTANTE SUR L'ORIGINALITÉ

L'originalité est une priorité.

Avant de finaliser le projet, vérifier :

1. **Le sujet** — Est-il suffisamment intéressant ?
2. **L'angle** — Est-ce une analyse différente d'une simple exploration descriptive ?
3. **Les visualisations** — Est-ce que chaque graphique apporte quelque chose ?
4. **Le dashboard** — Est-ce qu'il permet réellement d'explorer le phénomène ?
5. **Le storytelling** — Est-ce qu'une personne qui ne connaît pas le dataset comprend rapidement l'histoire ?
6. **La présentation** — Est-ce que le projet peut être expliqué clairement en 10 minutes ?

Chercher un concept identifiable.

Le projet doit pouvoir être résumé en une phrase mémorable.

Exemple de structure :

« Nous utilisons les données X pour comprendre Y et construire un outil interactif permettant d'explorer Z. »

---

## 19. NOTE IMPORTANTE SUR LE NIVEAU

Ne pas transformer le projet en projet de Master ou en projet de Data Science extrêmement complexe.

Je suis étudiante en Bac+2, en fin de cycle (voir section 0).

Le projet doit être :

- techniquement réalisable ;
- compréhensible ;
- défendable à l'oral ;
- suffisamment ambitieux pour être intéressant ;
- mais sans algorithmes inutiles.

La priorité est :

**qualité + pertinence + visualisation + storytelling + dashboard**

et non la complexité du code.

**Rappel :** l'objectif carrière (section 0) ne justifie jamais d'ajouter de la complexité technique artificielle (modèles de machine learning avancés, etc.). Il justifie seulement plus de soin sur le code, le README et la mise en ligne.

---

## 20. NOTEBOOK

Le notebook doit être organisé en sections claires :

1. Introduction
2. Présentation du dataset
3. Problématique
4. Chargement des données
5. Exploration
6. Qualité des données
7. Nettoyage
8. Échantillonnage
9. Comparaison des échantillons
10. Analyse univariée
11. Analyse bivariée
12. Analyse multivariée
13. Insights principaux
14. Conclusion

Le notebook doit être lisible même par quelqu'un qui ne connaît pas le code.

Ajouter des commentaires Markdown expliquant les décisions.

---

## 21. INSIGHTS

À la fin des analyses, produire une liste claire des principaux insights.

Par exemple :

**Insight 1** — ...

**Insight 2** — ...

**Insight 3** — ...

**Insight 4** — ...

Chaque insight doit être soutenu par les données.

Ne jamais inventer une conclusion simplement pour rendre l'histoire intéressante.

---

## 22. LIMITATIONS

Ajouter une section sur les limites.

Par exemple :

- biais possible du dataset ;
- données manquantes ;
- représentativité ;
- période couverte ;
- variables absentes ;
- qualité des données ;
- impossibilité d'établir une causalité.

Cette partie doit montrer une réflexion critique.

---

## 23. RAPPORT PDF

Produire un rapport de 4 à 6 pages maximum, conformément aux attentes du projet.

Structure :

1. **Introduction** — Contexte + problématique.
2. **Dataset et méthodologie** — Source, dimensions, variables, nettoyage, échantillonnage.
3. **Analyse** — Principales visualisations univariées, bivariées et multivariées.
4. **Dashboard** — Présentation des fonctionnalités et interactions.
5. **Insights** — Résultats principaux.
6. **Limites** — Limites des données et de l'analyse.
7. **Conclusion** — Synthèse.

Ne pas remplir les pages avec du texte inutile.

Privilégier :

- graphiques pertinents ;
- explications courtes ;
- résultats ;
- interprétation.

---

## 24. PRÉSENTATION ORALE — 10 MINUTES

Préparer une présentation de 10 minutes maximum.

Structure recommandée :

- **0:00–1:00** — Introduction + problème.
- **1:00–2:00** — Dataset + pourquoi ce dataset.
- **2:00–4:00** — Méthodologie + échantillonnage.
- **4:00–6:00** — Analyses principales.
- **6:00–8:30** — Démonstration du dashboard.
- **8:30–9:30** — Insights principaux.
- **9:30–10:00** — Conclusion + limites.

La démonstration du dashboard doit être préparée à l'avance.

Ne pas passer 8 minutes à expliquer le code.

---

## 25. PRÉPARATION AUX QUESTIONS DU PROFESSEUR

Préparer des réponses à des questions comme :

- Pourquoi avez-vous choisi ce dataset ?
- Pourquoi cette problématique ?
- Pourquoi cette visualisation ?
- Pourquoi ce type d'échantillonnage ?
- Votre échantillon est-il représentatif ?
- Pourquoi avez-vous supprimé cette variable ?
- Comment avez-vous traité les valeurs manquantes ?
- Pourquoi utiliser un scatter plot ici ?
- Que montre la corrélation ?
- Pourquoi cette couleur ?
- Pourquoi Streamlit ?
- Quelle est votre principale découverte ?
- Quelles sont les limites de votre analyse ?
- Peut-on parler de causalité ?
- Que changeriez-vous si vous aviez plus de données ?

Créer une section "Defense / Questions" contenant les réponses.

**Ajout objectif carrière :** préparer en plus une réponse courte à « Parlez-moi de ce projet » utilisable telle quelle en entretien de stage/embauche (30 secondes, sans jargon académique).

---

## 26. QUALITÉ DU CODE

Le code doit :

- fonctionner sans erreur ;
- être reproductible ;
- utiliser des "random_state" lorsque nécessaire ;
- éviter les répétitions inutiles ;
- utiliser des fonctions lorsque cela améliore la lisibilité ;
- avoir des noms de variables clairs ;
- séparer autant que possible préparation, analyse et visualisation.

**Ajout objectif carrière (voir section 0) :** le code sera lu par des recruteurs techniques sur GitHub, pas seulement corrigé par le professeur. En plus des points ci-dessus :
- chaque fonction dans `src/` doit avoir une courte docstring (ce qu'elle fait, ses paramètres) ;
- pas de cellule de notebook laissée avec du code de test ou de débogage inutile ;
- un fichier `requirements.txt` à jour et testé (installation propre dans un environnement neuf).

Avant de considérer le projet terminé :

- exécuter tout le notebook depuis le début ;
- vérifier qu'il fonctionne sur une nouvelle exécution ;
- lancer le dashboard ;
- tester tous les filtres ;
- vérifier les graphiques ;
- vérifier les données ;
- vérifier les exports éventuels.

---

## 27. MÉTHODE DE TRAVAIL AVEC CLAUDE CODE

IMPORTANT :

Ne génère PAS tout le projet en une seule fois.

Nous allons travailler progressivement.

- **PHASE 1** — Recherche et sélection du dataset.
- **PHASE 2** — Compréhension du dataset et définition de la problématique.
- **PHASE 2 bis — RENDU LUNDI** — Une fois les phases 1 et 2 validées, préparer un support PowerPoint (.pptx) court présentant : le dataset choisi et pourquoi, la problématique et les sous-questions, et les toutes premières observations si l'exploration a commencé. C'est le premier rendu d'étape (voir section 0.2), à livrer avant de continuer sur la phase 3.
- **PHASE 3** — Exploration et nettoyage.
- **PHASE 4** — Échantillonnage.
- **PHASE 5** — Analyse univariée.
- **PHASE 6** — Analyse bivariée.
- **PHASE 7** — Analyse multivariée.
- **PHASE 8** — Storytelling et sélection des insights.
- **PHASE 9** — Dashboard Streamlit.
- **PHASE 10** — Tests et amélioration du design.
- **PHASE 11** — Rapport.
- **PHASE 12** — Présentation orale.
- **PHASE 13 (ajout objectif carrière)** — Mise en ligne : dépôt GitHub public + déploiement du dashboard sur Streamlit Community Cloud + rédaction du README « portfolio ».

Après chaque phase :

1. exécuter le code ;
2. vérifier les résultats ;
3. expliquer ce qui a été obtenu ;
4. identifier les problèmes ;
5. seulement ensuite passer à la phase suivante.

Ne jamais remplacer massivement du code existant sans expliquer pourquoi.

---

## 28. RÈGLE ESSENTIELLE

Si une décision peut influencer la qualité scientifique ou la direction du projet, demander mon accord avant de la prendre.

Par exemple :

- changer de dataset ;
- changer la problématique ;
- supprimer une grande partie des variables ;
- modifier complètement l'architecture ;
- ajouter une méthode statistique importante ;
- changer le framework du dashboard.

Pour les petites corrections techniques, tu peux les effectuer directement.

---

## 29. CRITÈRE FINAL DE RÉUSSITE

À la fin, je veux pouvoir montrer le projet à mon professeur (et à un recruteur) et expliquer :

« Voici un dataset réel, voici la question que nous avons voulu étudier, voici comment nous avons préparé et échantillonné les données, voici les analyses que nous avons réalisées, voici ce que nous avons découvert et voici un dashboard interactif qui permet à l'utilisateur d'explorer ces résultats. »

Le projet doit être cohérent du début à la fin.

Dataset → Problématique → Échantillonnage → Nettoyage → Analyse → Visualisations → Insights → Dashboard → Rapport → Présentation → Mise en ligne (GitHub + dashboard déployé).

Aucune partie ne doit sembler ajoutée uniquement pour satisfaire une checklist.

---

## 30. PREMIÈRE ÉTAPE

Commencer directement par la **PHASE 1** (section 27) : recherche et comparaison de plusieurs datasets Kaggle candidats, selon les contraintes de la section 2, avant toute écriture de code d'analyse.

---

## 31. MISE EN LIGNE ET PORTFOLIO (NOUVELLE SECTION — OBJECTIF CARRIÈRE)

Cette section s'exécute en toute fin de projet (Phase 13), une fois les sections 1 à 29 validées par le professeur ou considérées comme terminées.

### 31.1 Dépôt GitHub

- Créer un dépôt public sur GitHub avec la structure de la section 7.
- Historique de commits propre : un commit par étape logique, avec un message clair (éviter "update", "fix", "wip").
- Ajouter un fichier `.gitignore` adapté (exclure les gros fichiers de données brutes si nécessaire, les fichiers d'environnement, les caches).
- Ne jamais committer de clé API ou d'identifiant Kaggle en clair.

### 31.2 README.md — rôle de mini-CV technique

Doit contenir, dans cet ordre :

1. Le nom du projet et une phrase d'accroche (la « phrase mémorable » de la section 18).
2. Un lien direct vers le dashboard déployé, tout en haut.
3. 2-3 captures d'écran du dashboard.
4. Le contexte et la problématique (résumés en quelques lignes).
5. Le dataset utilisé (source, taille) et pourquoi ce choix.
6. La méthodologie en bref (échantillonnage, nettoyage, analyses).
7. Les principaux insights (2-3 phrases, pas tout le détail).
8. Les technologies utilisées (badges ou simple liste : Python, Pandas, Streamlit, Plotly...).
9. Comment lancer le projet en local (instructions testées).
10. Les limites du projet (lien vers la section 22).

### 31.3 Déploiement du dashboard

- Déployer sur Streamlit Community Cloud (gratuit, lié directement au dépôt GitHub).
- Vérifier que le dashboard déployé fonctionne réellement (pas seulement en local) avant de mettre le lien dans le README.
- Tester tous les filtres sur la version en ligne, pas seulement en local.

### 31.4 Après la mise en ligne

- Ajouter le lien du dépôt et/ou du dashboard sur le profil LinkedIn et dans le CV, dans la section projets.
- Optionnel : un court post LinkedIn présentant le projet, écrit simplement, sans survendre les résultats.
