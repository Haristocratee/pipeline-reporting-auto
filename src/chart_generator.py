"""
Module de génération des graphiques pour le rapport PDF.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import io

plt.style.use('seaborn-v0_8-whitegrid')


def fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()


def histogram_grid(df: pd.DataFrame) -> bytes:
    """Grille d'histogrammes pour toutes les colonnes numériques."""
    num_cols = df.select_dtypes(include='number').columns.tolist()
    if not num_cols:
        return None
    n = len(num_cols)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
    axes = [axes] if n == 1 else axes.flatten()
    for i, col in enumerate(num_cols):
        axes[i].hist(df[col].dropna(), bins=30, color='steelblue', alpha=0.8, edgecolor='white')
        axes[i].set_title(col, fontweight='bold')
        axes[i].set_xlabel('Valeur')
        axes[i].set_ylabel('Fréquence')
    for j in range(i+1, len(axes)):
        axes[j].set_visible(False)
    plt.suptitle('Distributions des variables numériques', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig_to_bytes(fig)


def boxplot_grid(df: pd.DataFrame) -> bytes:
    """Boxplots pour détecter les outliers."""
    num_cols = df.select_dtypes(include='number').columns.tolist()
    if not num_cols:
        return None
    fig, ax = plt.subplots(figsize=(10, 5))
    df_norm = df[num_cols].apply(lambda x: (x - x.mean()) / (x.std() + 1e-9))
    df_norm.boxplot(ax=ax, patch_artist=True,
                    boxprops=dict(facecolor='steelblue', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))
    ax.set_title('Boxplots — Détection des valeurs aberrantes (valeurs normalisées)',
                 fontweight='bold')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    return fig_to_bytes(fig)


def correlation_heatmap(df: pd.DataFrame) -> bytes:
    """Heatmap des corrélations."""
    num_df = df.select_dtypes(include='number')
    if num_df.shape[1] < 2:
        return None
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(num_df.corr(), annot=True, fmt='.2f', cmap='RdYlGn',
                center=0, ax=ax, linewidths=0.5, square=True)
    ax.set_title('Matrice de corrélation', fontweight='bold', fontsize=13)
    plt.tight_layout()
    return fig_to_bytes(fig)
