
## **Analyse des données de la base Open Medic**
---
### **Information générales**
L'application développée ici permet d'explorer la consommation de médicament (HUMIRA) à partir des données de la base Open Medic.
Elle a été développée en Python avec Streamlit et s'appuie sur une base SQLite en mémoire pour interroger les fichiers de données chargées. 

**1. Lien d'accès à l'app**

L'application est accessible ici: https://testsanoia-58sngdxrtvbxfflvxvqkuh.streamlit.app/

**2. Téléchargement les fichiers**

Les fichiers utilisés ont été téléchargés sur ce site: https://www.data.gouv.fr/fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes/

Les trois fichiers téléchargés sont les suivants:
* NB_2024_cip13_age_sexe_reg_spe.CSV
* NB_2023_cip13_age_sexe_reg_spe.CSV
* NB_2022_cip13_age_sexe_reg_spe.CSV

Afin de charger ces fichiers dans l'application un renommage des noms de fichier a été nécessaire. Ci-après le renommage effectué pour les fichiers:
* NB_2024.csv
* NB_2023.csv
* NB_2022.csv

**3. Fonctionnalités pricipales**

* Chargement des fichiers CSV pour les années 2024, 2023, 2022
* Affichage des analyses sous forme de tableaux et/ou de graphiques interactifs
* Requêtes SQL pour la consommation d'HUMIRA
	* Au total
	* Par dispositif d'injection (seringue/stylo)
	* Par tranche d'âge
	* Par région
	* Par prescripteur 
	* Le tout combiné

**4. Données attendues**

Les fichiers doivent être les fichiers renommés encodés en Latin-1 avec les colonnes tel que l_cip13, age, BEN_REG, PSP_SPE.

**5. Lancement de l'application en local**

*a. Cloner le dépôt*

```bash
git clone https://github.com/Colombe17/Test_Sanoia.git
cd Test_Sanoia/src
```

*b. Créer et activer un environnement virtuel*

```bash
python3 -m venv .venv
source .venv/bin/activate # Sur macOS/Linue
.venv\Scripts\activate # Sur Windows
```

*c. Installer les dépendances*
```bash
pip install -r requirement.txt
```

Si requirement.txt ne fonctionne pas il faudrait installer les dépendances manuellement. 

```bash
pip install streamlit pandas matplotlib
```

*d. Lancer l'application Streamlit*

```bash
streamlit run test_sanoia_app.py
```

