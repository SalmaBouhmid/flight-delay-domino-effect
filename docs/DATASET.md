# Le dataset en détail

## D'où viennent les données ?

| | |
|---|---|
| **Plateforme** | Kaggle — [Flight Status Prediction](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022) (auteur : Rob Mulla, « robikscube ») |
| **Source d'origine** | Bureau of Transportation Statistics (**BTS**), l'organisme officiel des statistiques de transport des États-Unis. Chaque compagnie aérienne américaine doit déclarer chaque vol. |
| **Fichier téléchargé** | `Combined_Flights_2022.parquet` (150 Mo) : **4 078 318 vols × 61 colonnes**, de janvier à juillet 2022 (le fichier 2022 s'arrête en juillet) |
| **Notre périmètre** | Vols **au départ d'Atlanta (ATL)**, **juin + juillet 2022** → **54 461 vols × 61 colonnes** |
| **Fichier de travail** | `data/raw/vols_atlanta_ete_2022.csv` (19 Mo), créé par `src/data_loading.py` |
| **Fichier nettoyé** | `data/processed/vols_atlanta_ete_2022_propre.csv`, créé par `src/preprocessing.py` |

**Une ligne = un vol** (un départ d'Atlanta, un jour donné, par une compagnie).

## Pourquoi ce périmètre ? (à savoir expliquer)

1. **Consigne respectée** : 54 461 lignes (≥ 30 000) et 61 colonnes (≥ 50), numériques + catégorielles.
2. **Atlanta** = aéroport le plus fréquenté du monde → beaucoup de compagnies, de destinations et d'avions.
3. **Juin–juillet** = pic des retards de l'année (≈ 26 % à Atlanta contre ≈ 14-16 % en janvier-février).
   Juillet seul ne faisait que 27 533 vols (< 30 000), d'où les deux mois.
4. **Un seul aéroport** permet de suivre le même avion qui repart plusieurs fois dans la journée → étude de l'effet domino.
5. **Fichier léger** : tout s'exécute en quelques secondes sur un PC normal.

> ⚠️ Ce choix de périmètre n'est **pas** un échantillonnage : c'est la **délimitation du sujet**
> (« j'étudie Atlanta en été »). L'échantillonnage est fait **ensuite**, sur les 54 461 vols.

## Dictionnaire des 61 colonnes

Légende du type : **N** = numérique, **C** = catégorielle (texte), **B** = vrai/faux, **D** = date.
Les colonnes en **gras** sont celles utilisées dans l'analyse.

### Date et calendrier
| Colonne | Type | Signification |
|---|---|---|
| **`FlightDate`** | D | Date du vol |
| `Year` | N | Année (toujours 2022 → supprimée au nettoyage) |
| `Quarter` | N | Trimestre (2 = juin, 3 = juillet) |
| **`Month`** | N | Mois (6 ou 7) |
| `DayofMonth` | N | Jour du mois (1 à 31) |
| **`DayOfWeek`** | N | Jour de la semaine (1 = lundi … 7 = dimanche) |

### Compagnie aérienne
| Colonne | Type | Signification |
|---|---|---|
| **`Airline`** | C | Nom de la compagnie qui **opère** le vol (ex. « Delta Air Lines Inc. ») |
| `Operating_Airline`, `IATA_Code_Operating_Airline`, `DOT_ID_Operating_Airline` | C / N | Codes de cette même compagnie opérante (ex. DL) |
| `Marketing_Airline_Network`, `IATA_Code_Marketing_Airline`, `DOT_ID_Marketing_Airline` | C / N | Compagnie qui **vend** le billet. Ex. : un vol Endeavor Air est vendu sous la marque Delta |
| `Operated_or_Branded_Code_Share_Partners` | C | Type de partenariat (vol opéré par la compagnie elle-même ou par un partenaire) |
| `Flight_Number_Marketing_Airline`, `Flight_Number_Operating_Airline` | N | Numéro de vol |
| **`Tail_Number`** | C | **Immatriculation de l'avion** (ex. N526EA) → permet de suivre un même avion (effet domino) |

### Aéroport de départ (toujours Atlanta ici)
| Colonne | Type | Signification |
|---|---|---|
| `Origin` | C | Code de l'aéroport de départ (toujours « ATL ») |
| `OriginAirportID`, `OriginAirportSeqID`, `OriginCityMarketID`, `OriginCityName`, `OriginState`, `OriginStateFips`, `OriginStateName`, `OriginWac` | N / C | Codes et noms de l'aéroport / ville / État de départ. **Tous constants → supprimés au nettoyage** |

### Aéroport d'arrivée
| Colonne | Type | Signification |
|---|---|---|
| **`Dest`** | C | Code de l'aéroport d'arrivée (ex. MCO = Orlando, JFK = New York) — 147 destinations |
| `DestCityName`, `DestState`, `DestStateName` | C | Ville et État d'arrivée |
| `DestAirportID`, `DestAirportSeqID`, `DestCityMarketID`, `DestStateFips`, `DestWac` | N | Codes numériques de la destination |

### Départ
| Colonne | Type | Signification |
|---|---|---|
| **`CRSDepTime`** | N | Heure de départ **prévue**, au format HHMM (ex. 1435 = 14 h 35). CRS = système de réservation |
| `DepTime` | N | Heure de départ **réelle** (HHMM) |
| **`DepDelay`** | N | **Retard au départ en minutes** (négatif = parti en avance) — variable principale |
| `DepDelayMinutes` | N | Même chose, mais les avances sont mises à 0 |
| **`DepDel15`** | N | **1 si retard au départ > 15 min, sinon 0** — définition officielle du retard |
| `DepartureDelayGroups` | N | Retard regroupé par tranches de 15 min (−1 = en avance, 0 = 0-14 min, 1 = 15-29 min…) |
| `DepTimeBlk` | C | Tranche horaire de départ prévue (ex. « 1400-1459 ») |
| **`TaxiOut`** | N | Minutes de **roulage** entre la porte et le décollage |
| `WheelsOff` | N | Heure du décollage (HHMM) |

### Arrivée
| Colonne | Type | Signification |
|---|---|---|
| `CRSArrTime` | N | Heure d'arrivée prévue (HHMM) |
| `ArrTime` | N | Heure d'arrivée réelle |
| `WheelsOn` | N | Heure de l'atterrissage |
| **`TaxiIn`** | N | Minutes de roulage entre l'atterrissage et la porte |
| **`ArrDelay`** | N | **Retard à l'arrivée en minutes** (négatif = arrivé en avance) |
| `ArrDelayMinutes` | N | Même chose, avances mises à 0 |
| **`ArrDel15`** | N | 1 si retard à l'arrivée > 15 min |
| `ArrivalDelayGroups` | N | Retard à l'arrivée par tranches de 15 min |
| `ArrTimeBlk` | C | Tranche horaire d'arrivée prévue |

### Durée, distance, statut
| Colonne | Type | Signification |
|---|---|---|
| `CRSElapsedTime` | N | Durée totale prévue (porte à porte), en minutes |
| `ActualElapsedTime` | N | Durée totale réelle |
| **`AirTime`** | N | Temps en vol (décollage → atterrissage), en minutes |
| **`Distance`** | N | Distance en **miles** (1 mile = 1,6 km) |
| `DistanceGroup` | N | Distance par tranches de 250 miles |
| **`Cancelled`** | B | Vol **annulé** |
| **`Diverted`** | B | Vol **dévié** (a atterri dans un autre aéroport) |
| `DivAirportLandings` | N | Nombre d'atterrissages dans un aéroport de déroutement |

## Colonnes ajoutées au nettoyage (8)

| Colonne | Comment elle est calculée | À quoi elle sert |
|---|---|---|
| `heure_depart_prevue` | `CRSDepTime // 100` (1435 → 14) | Analyser le retard heure par heure |
| `jour_semaine` | `DayOfWeek` traduit (1 → Lundi) | Graphiques lisibles |
| `mois` | `Month` traduit (6 → Juin) | Graphiques lisibles |
| `compagnie` | Nom court ; compagnies < 1 000 vols → « Autres » | Comparer des compagnies avec assez de vols |
| `statut` | Annulé / Dévié / En retard (`DepDel15` = 1) / À l'heure | Vue d'ensemble |
| `minutes_rattrapees` | `DepDelay − ArrDelay` | Le retard se rattrape-t-il en vol ? |
| `rang_rotation` | 1er, 2e, 3e départ de la journée du même avion | Effet domino |
| `vol_precedent_en_retard` | `DepDel15` du départ précédent du même avion, le même jour | **Effet domino** |

## Qualité des données (résumé)

| Élément | Résultat |
|---|---|
| Lignes / colonnes | 54 461 / 61 |
| Types | 41 numériques, 17 catégorielles, 2 vrai/faux, 1 date |
| Doublons | 0 |
| Valeurs manquantes | 17 colonnes, **toutes expliquées** par les 1 009 vols annulés et 123 vols déviés |
| Outliers | ≈ 12 % selon la règle de l'IQR (retard > 44,5 min) : **gardés**, ce sont de vrais retards |
| Incohérences | 13 vols annulés avec une heure de départ (annulés après avoir quitté la porte) : gardés |
