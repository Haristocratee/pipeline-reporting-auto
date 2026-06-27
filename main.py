"""
Pipeline de Reporting Automatisé — CSV vers PDF
Usage : python main.py --input data/sample_sales.csv --output rapport.pdf
"""
import argparse
import pandas as pd
import numpy as np
from pathlib import Path

from src.data_processor import load_and_clean, compute_stats, generate_insights
from src.chart_generator import histogram_grid, boxplot_grid, correlation_heatmap
from src.pdf_builder import build_pdf


def generate_sample_data():
    """Crée un CSV de démonstration (données de ventes simulées)."""
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d'),
        'Agence': np.random.choice(['Paris','Lyon','Marseille','Bordeaux'], n),
        'Produit': np.random.choice(['Compte Courant','Épargne','Crédit Auto','Assurance'], n),
        'Chiffre_Affaires': np.round(np.random.lognormal(10, 0.8, n), 2),
        'Nb_Clients': np.random.poisson(45, n),
        'Taux_Satisfaction': np.round(np.random.beta(8, 2, n) * 10, 1),
        'Nb_Reclamations': np.random.poisson(3, n),
    })
    Path('data').mkdir(exist_ok=True)
    df.to_csv('data/sample_sales.csv', index=False)
    print("✅ Données de démonstration créées : data/sample_sales.csv")
    return 'data/sample_sales.csv'


def main():
    parser = argparse.ArgumentParser(description='Génère un rapport PDF depuis un CSV')
    parser.add_argument('--input', '-i', default=None, help='Fichier CSV source')
    parser.add_argument('--output', '-o', default='rapport_auto.pdf', help='Fichier PDF de sortie')
    parser.add_argument('--title', '-t', default='Rapport Analytique Automatisé', help='Titre du rapport')
    args = parser.parse_args()

    print("\n🚀 Pipeline de Reporting Automatisé")
    print("=" * 45)

    # Données source
    input_path = args.input
    if input_path is None or not Path(input_path).exists():
        print("\n📊 Génération des données de démonstration...")
        input_path = generate_sample_data()

    # Traitement
    print(f"\n📂 Chargement de : {input_path}")
    df = load_and_clean(input_path)
    print(f"   {len(df):,} lignes · {len(df.columns)} colonnes")

    print("\n📐 Calcul des statistiques...")
    stats = compute_stats(df)

    print("\n💡 Génération des insights...")
    insights = generate_insights(df, stats)
    for ins in insights:
        print(f"   → {ins}")

    print("\n📈 Création des graphiques...")
    charts = {
        'Distributions': histogram_grid(df),
        'Valeurs aberrantes (Boxplots)': boxplot_grid(df),
        'Corrélations': correlation_heatmap(df),
    }

    print("\n📄 Construction du PDF...")
    build_pdf(args.output, args.title, df, stats, insights, charts)

    print(f"\n✨ Terminé ! Rapport disponible : {args.output}")


if __name__ == '__main__':
    main()
