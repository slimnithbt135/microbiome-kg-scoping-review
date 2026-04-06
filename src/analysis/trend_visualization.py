#!/usr/bin/env python3
"""
trend_visualization.py

Visualization script for microbiome knowledge graph scoping review.
Generates publication-ready figures for the manuscript.

Figures generated:
    - Figure 1A: Temporal distribution of studies
    - Figure 1B: Category distribution (pie/bar chart)
    - Figure 1C: Technology distribution (pie/bar chart)
    - Figure 1D: FAIR compliance distribution
    - Figure 1E: Source database distribution
    - Figure 1F: Ontology usage analysis
    - Supplementary Figure 1: Combined trend analysis

Usage:
    python trend_visualization.py --input data/supplementary/Supplementary_Table_1_All_Studies.csv --output outputs/figures/

Author: Thabet Slimani
Date: April 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
import matplotlib.patches as mpatches


def load_data(filepath):
    """Load the supplementary table."""
    df = pd.read_csv(filepath)
    df['Classification_Confidence'] = pd.to_numeric(df['Classification_Confidence'], errors='coerce')
    return df


def plot_temporal_trends(df, output_dir):
    """Generate Figure 1A: Temporal distribution of studies."""
    fig, ax = plt.subplots(figsize=(12, 6))

    year_counts = df['Year'].value_counts().sort_index()

    # Create bar plot
    bars = ax.bar(year_counts.index, year_counts.values, color='#2E86AB', edgecolor='black', linewidth=0.5)

    # Highlight peak years
    max_count = year_counts.max()
    for bar, count in zip(bars, year_counts.values):
        if count == max_count:
            bar.set_color('#A23B72')

    # Add trend line
    z = np.polyfit(year_counts.index, year_counts.values, 2)
    p = np.poly1d(z)
    ax.plot(year_counts.index, p(year_counts.index), "r--", linewidth=2, label='Trend')

    # Styling
    ax.set_xlabel('Publication Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Studies', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1A: Temporal Distribution of Microbiome KG Studies', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_dir / 'Figure_1A_Temporal_Distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1A_Temporal_Distribution.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Figure 1A generated")


def plot_category_distribution(df, output_dir):
    """Generate Figure 1B: Category distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    category_counts = df['Category'].value_counts()
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#95C623']

    # Pie chart
    wedges, texts, autotexts = ax1.pie(
        category_counts.values, 
        labels=None,
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.05 if i == 0 else 0 for i in range(len(category_counts))],
        shadow=True
    )
    ax1.set_title('Category Distribution', fontsize=12, fontweight='bold')

    # Bar chart
    bars = ax2.barh(range(len(category_counts)), category_counts.values, color=colors, edgecolor='black')
    ax2.set_yticks(range(len(category_counts)))
    ax2.set_yticklabels(category_counts.index, fontsize=10)
    ax2.set_xlabel('Number of Studies', fontsize=11, fontweight='bold')
    ax2.set_title('Studies per Category', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, category_counts.values)):
        ax2.text(count + 0.5, i, f'{count} ({count/len(df)*100:.1f}%)', 
                va='center', fontsize=9)

    plt.suptitle('Figure 1B: Category Distribution of Microbiome KG Systems', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'Figure_1B_Category_Distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1B_Category_Distribution.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Figure 1B generated")


def plot_technology_distribution(df, output_dir):
    """Generate Figure 1C: Technology distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    tech_counts = df['Graph_Type'].value_counts()
    colors = ['#2E86AB', '#F18F01', '#A23B72', '#95C623']

    # Pie chart
    wedges, texts, autotexts = ax1.pie(
        tech_counts.values,
        labels=tech_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.05 if i == 0 else 0 for i in range(len(tech_counts))],
        shadow=True
    )
    ax1.set_title('Technology Distribution', fontsize=12, fontweight='bold')

    # Horizontal bar chart
    bars = ax2.barh(range(len(tech_counts)), tech_counts.values, color=colors, edgecolor='black')
    ax2.set_yticks(range(len(tech_counts)))
    ax2.set_yticklabels(tech_counts.index, fontsize=10)
    ax2.set_xlabel('Number of Studies', fontsize=11, fontweight='bold')
    ax2.set_title('Studies by Technology', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, tech_counts.values)):
        ax2.text(count + 0.5, i, f'{count} ({count/len(df)*100:.1f}%)', 
                va='center', fontsize=9)

    plt.suptitle('Figure 1C: Knowledge Graph Technology Distribution', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / 'Figure_1C_Technology_Distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1C_Technology_Distribution.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Figure 1C generated")


def plot_fair_compliance(df, output_dir):
    """Generate Figure 1D: FAIR compliance distribution."""
    fig, ax = plt.subplots(figsize=(10, 6))

    fair_counts = df['FAIR_Compliance'].value_counts()

    # Define colors based on compliance level
    color_map = {'High': '#95C623', 'Moderate': '#F18F01', 'Low-Moderate': '#C73E1D'}
    colors = [color_map.get(f, '#2E86AB') for f in fair_counts.index]

    bars = ax.bar(fair_counts.index, fair_counts.values, color=colors, edgecolor='black', linewidth=1)

    # Add value labels
    for bar, count in zip(bars, fair_counts.values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}\n({count/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_xlabel('FAIR Compliance Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Studies', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1D: FAIR Compliance Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(fair_counts.values) * 1.2)

    plt.tight_layout()
    plt.savefig(output_dir / 'Figure_1D_FAIR_Compliance.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1D_FAIR_Compliance.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Figure 1D generated")


def plot_source_distribution(df, output_dir):
    """Generate Figure 1E: Source database distribution."""
    fig, ax = plt.subplots(figsize=(10, 6))

    source_counts = df['Source'].value_counts()
    colors = ['#2E86AB', '#A23B72', '#F18F01']

    bars = ax.bar(source_counts.index, source_counts.values, color=colors, edgecolor='black', linewidth=1)

    # Add value labels
    for bar, count in zip(bars, source_counts.values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}\n({count/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_xlabel('Database Source', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Studies', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1E: Source Database Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(source_counts.values) * 1.2)

    plt.tight_layout()
    plt.savefig(output_dir / 'Figure_1E_Source_Distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1E_Source_Distribution.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Figure 1E generated")


def plot_ontology_usage(df, output_dir):
    """Generate Figure 1F: Ontology usage analysis."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Parse ontologies
    all_ontologies = []
    for ontologies in df['Ontologies_Used'].dropna():
        ont_list = [o.strip() for o in str(ontologies).split(',')]
        all_ontologies.extend(ont_list)

    ontology_counts = pd.Series(all_ontologies).value_counts()
    ontology_pct = (ontology_counts / len(df) * 100).round(1)

    # Select top ontologies
    top_ontologies = ontology_counts.head(10)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(top_ontologies)))

    bars = ax.barh(range(len(top_ontologies)), top_ontologies.values, color=colors, edgecolor='black')
    ax.set_yticks(range(len(top_ontologies)))
    ax.set_yticklabels(top_ontologies.index, fontsize=10)
    ax.set_xlabel('Number of Mentions', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1F: Top 10 Ontology Usage in Microbiome KG Systems', 
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()

    # Add percentage labels
    for i, (bar, count) in enumerate(zip(bars, top_ontologies.values)):
        pct = ontology_pct[top_ontologies.index[i]]
        ax.text(count + 0.5, i, f'{count} ({pct}%)', 
                va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'Figure_1F_Ontology_Usage.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1F_Ontology_Usage.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Figure 1F generated")


def plot_combined_figure(df, output_dir):
    """Generate combined figure with all subplots."""
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # 1A: Temporal
    ax1 = fig.add_subplot(gs[0, :])
    year_counts = df['Year'].value_counts().sort_index()
    ax1.bar(year_counts.index, year_counts.values, color='#2E86AB', edgecolor='black')
    ax1.set_xlabel('Publication Year', fontweight='bold')
    ax1.set_ylabel('Number of Studies', fontweight='bold')
    ax1.set_title('A. Temporal Distribution', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # 1B: Category
    ax2 = fig.add_subplot(gs[1, 0])
    category_counts = df['Category'].value_counts()
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#95C623']
    ax2.pie(category_counts.values, labels=None, autopct='%1.0f%%', colors=colors)
    ax2.set_title('B. Category Distribution', fontweight='bold')

    # 1C: Technology
    ax3 = fig.add_subplot(gs[1, 1])
    tech_counts = df['Graph_Type'].value_counts()
    colors_tech = ['#2E86AB', '#F18F01', '#A23B72', '#95C623']
    ax3.pie(tech_counts.values, labels=tech_counts.index, autopct='%1.0f%%', colors=colors_tech)
    ax3.set_title('C. Technology Distribution', fontweight='bold')

    # 1D: FAIR
    ax4 = fig.add_subplot(gs[1, 2])
    fair_counts = df['FAIR_Compliance'].value_counts()
    color_map = {'High': '#95C623', 'Moderate': '#F18F01', 'Low-Moderate': '#C73E1D'}
    colors_fair = [color_map.get(f, '#2E86AB') for f in fair_counts.index]
    ax4.bar(fair_counts.index, fair_counts.values, color=colors_fair, edgecolor='black')
    ax4.set_title('D. FAIR Compliance', fontweight='bold')
    ax4.set_ylabel('Studies')

    # 1E: Source
    ax5 = fig.add_subplot(gs[2, 0])
    source_counts = df['Source'].value_counts()
    colors_src = ['#2E86AB', '#A23B72', '#F18F01']
    ax5.bar(source_counts.index, source_counts.values, color=colors_src, edgecolor='black')
    ax5.set_title('E. Source Database', fontweight='bold')
    ax5.set_ylabel('Studies')

    # 1F: Ontologies
    ax6 = fig.add_subplot(gs[2, 1:])
    all_ontologies = []
    for ontologies in df['Ontologies_Used'].dropna():
        ont_list = [o.strip() for o in str(ontologies).split(',')]
        all_ontologies.extend(ont_list)
    ontology_counts = pd.Series(all_ontologies).value_counts().head(8)
    colors_ont = plt.cm.viridis(np.linspace(0.2, 0.8, len(ontology_counts)))
    ax6.barh(range(len(ontology_counts)), ontology_counts.values, color=colors_ont, edgecolor='black')
    ax6.set_yticks(range(len(ontology_counts)))
    ax6.set_yticklabels(ontology_counts.index)
    ax6.set_xlabel('Mentions', fontweight='bold')
    ax6.set_title('F. Top Ontology Usage', fontweight='bold')
    ax6.invert_yaxis()

    plt.suptitle('Figure 1: Quantitative Analysis of Microbiome Knowledge Graph Systems (n=54)', 
                 fontsize=16, fontweight='bold', y=0.98)

    plt.savefig(output_dir / 'Figure_1_Combined_Analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'Figure_1_Combined_Analysis.pdf', bbox_inches='tight')
    plt.close()
    print("  ✓ Combined Figure 1 generated")


def main():
    parser = argparse.ArgumentParser(
        description='Generate visualizations for microbiome KG scoping review'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to Supplementary_Table_1_All_Studies.csv'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for figures'
    )

    args = parser.parse_args()

    # Load data
    df = load_data(args.input)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nGenerating figures...")
    print("-" * 40)

    # Generate all figures
    plot_temporal_trends(df, output_dir)
    plot_category_distribution(df, output_dir)
    plot_technology_distribution(df, output_dir)
    plot_fair_compliance(df, output_dir)
    plot_source_distribution(df, output_dir)
    plot_ontology_usage(df, output_dir)
    plot_combined_figure(df, output_dir)

    print("-" * 40)
    print(f"\nAll figures saved to: {output_dir}")
    print("\nGenerated files:")
    for f in sorted(output_dir.glob('Figure_1*')):
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
