# Mettre le projet en ligne (phase 13)

Le dépôt git local est prêt : historique propre, un commit par étape.
Il reste deux actions à faire **avec vos comptes** (je ne peux pas me connecter à votre place).

---

## 1. Publier le code sur GitHub (≈ 5 min)

1. Aller sur <https://github.com/new>.
2. Nom du dépôt : `flight-delay-domino-effect` · visibilité **Public** · **ne cochez rien** (pas de README, pas de .gitignore : ils existent déjà).
3. Cliquer sur **Create repository**.
4. Dans un terminal, depuis le dossier du projet :

```bash
cd C:\Users\123\Documents\dataviz-retards-vols
git remote add origin https://github.com/SalmaBouhmid/flight-delay-domino-effect.git
git push -u origin main
```

Le fichier Kaggle de 143 Mo n'est **pas** envoyé (il est dans `.gitignore`, GitHub refuse les fichiers de plus de 100 Mo).
Les fichiers de travail (19 Mo) sont envoyés, donc le projet fonctionne directement après un `git clone`.

## 2. Mettre le dashboard en ligne sur Streamlit Community Cloud (≈ 5 min, gratuit)

1. Aller sur <https://share.streamlit.io> et se connecter **avec GitHub**.
2. **Create app** → *Deploy a public app from GitHub*.
3. Remplir :
   - Repository : `SalmaBouhmid/flight-delay-domino-effect`
   - Branch : `main`
   - Main file path : `dashboard/app.py`
   - *Advanced settings* → Python version : **3.12**
4. Cliquer sur **Deploy**. Le premier lancement prend 2-3 minutes (installation de `dashboard/requirements.txt`).
5. Copier l'adresse obtenue (du type `https://....streamlit.app`).

**Vérifier en ligne** (exigence du cahier des charges, section 31.3) : changer chaque filtre, ouvrir chaque onglet.

## 3. Après la mise en ligne

1. Me donner le lien : je l'ajoute en haut du README et je fais le commit.
2. Ajouter le lien du dépôt et du dashboard sur LinkedIn et dans le CV (section « Projets »).
3. Optionnel : un court post LinkedIn, simple, sans survendre (je peux vous aider à l'écrire).
