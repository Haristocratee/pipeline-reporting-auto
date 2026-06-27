"""
Module de traitement et d'analyse des données CSV.
"""
import pandas as pd
import numpy as np


def load_and_clean(filepath: str) -> pd.DataFrame:
    """Charge un CSV et effectue un nettoyage basique."""
    df = pd.read_csv(filepath, parse_dates=True, infer_datetime_format=True)

    # Doublons
    n_dup = df.duplicated().sum()
    df = df.drop_duplicates()

    # Valeurs manquantes
    n_missing = df.isnull().sum().sum()
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Inconnu')

    print(f"  Doublons supprimés : {n_dup}")
    print(f"  Valeurs manquantes imputées : {n_missing}")
    return df


def compute_stats(df: pd.DataFrame) -> dict:
    """Calcule les statistiques descriptives pour les colonnes numériques."""
    num_df = df.select_dtypes(include='number')
    stats = {}
    for col in num_df.columns:
        series = num_df[col].dropna()
        stats[col] = {
            'count': len(series),
            'mean': round(series.mean(), 2),
            'median': round(series.median(), 2),
            'std': round(series.std(), 2),
            'min': round(series.min(), 2),
            'max': round(series.max(), 2),
            'q25': round(series.quantile(0.25), 2),
            'q75': round(series.quantile(0.75), 2),
        }
    return stats


def generate_insights(df: pd.DataFrame, stats: dict) -> list[str]:
    """Génère des insights automatiques en langage naturel."""
    insights = []
    insights.append(f"Le dataset contient {len(df):,} lignes et {len(df.columns)} colonnes.")

    num_cols = list(stats.keys())
    if num_cols:
        main_col = num_cols[0]
        s = stats[main_col]
        insights.append(
            f"La variable principale '{main_col}' présente une moyenne de {s['mean']:,} "
            f"(médiane : {s['median']:,}), avec un écart-type de {s['std']:,}."
        )
        if s['std'] / (abs(s['mean']) + 1e-9) > 0.5:
            insights.append(
                f"La forte dispersion de '{main_col}' (CV={s['std']/abs(s['mean']):.1%}) "
                f"suggère une hétérogénéité significative dans les données."
            )

    # Détection valeurs aberrantes
    for col, s in stats.items():
        iqr = s['q75'] - s['q25']
        n_outliers = ((df[col] < s['q25'] - 1.5*iqr) | (df[col] > s['q75'] + 1.5*iqr)).sum()
        if n_outliers > 0:
            insights.append(
                f"Attention : {n_outliers} valeurs aberrantes détectées dans '{col}' "
                f"(méthode IQR)."
            )

    return insights
