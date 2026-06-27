# ⚡ Pipeline de Reporting Automatisé — CSV → PDF

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-DC143C?style=flat)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

> Transformez n'importe quel fichier CSV en rapport PDF professionnel en une commande — avec statistiques, graphiques et synthèse exécutive.

---

## 🎯 Contexte

Automatisation des reportings récurrents — directement inspiré de mon travail chez **Afriland First Bank** où je produisais des rapports mensuels de KPIs manuellement sous Excel.

---

## ⚙️ Lancement rapide

```bash
pip install -r requirements.txt

# Avec les données de démonstration
python main.py --input data/sample_sales.csv --output rapport_ventes.pdf

# Avec votre propre CSV
python main.py --input votre_fichier.csv --output rapport.pdf --title "Mon Rapport"
```

---

## 📄 Contenu du rapport généré

1. **Page de garde** — Titre, date, résumé
2. **Statistiques descriptives** — Min, max, moyenne, médiane, écart-type
3. **Graphiques** — Histogrammes, boxplots, corrélations
4. **Top 10 & Bottom 10** — Meilleures et pires performances
5. **Synthèse exécutive** — Insights automatiques en langage naturel

---

## 🗂️ Structure

```
pipeline-reporting-auto/
├── src/
│   ├── data_processor.py    # Nettoyage et analyse des données
│   ├── chart_generator.py   # Génération des graphiques
│   └── pdf_builder.py       # Construction du PDF
├── data/
│   └── sample_sales.csv     # Données de démonstration
├── main.py                  # Point d'entrée
└── requirements.txt
```

---

## 👤 Auteur

**Harry TEGUE** — Data Analyst | Automatisation & Reporting
📧 harrytegue@gmail.com
