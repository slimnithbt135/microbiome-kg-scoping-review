#!/usr/bin/env python3
"""
classification_analysis.py

Analysis script for microbiome knowledge graph scoping review.
Generates statistical summaries and distributions from the classified studies.

Usage:
    python classification_analysis.py --input data/supplementary/Supplementary_Table_1_All_Studies.csv --output outputs/reports/

Author: Thabet Slimani
Date: April 2026
"""

import pandas as pd
import numpy as np
import argparse
import json
from pathlib import Path
from collections import Counter


def load_data(filepath):
    """Load and validate the supplementary table."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} studies from {filepath}")
    return df


def analyze_category_distribution(df):
    """Analyze category distribution (Figure 1B)."""
    category_counts = df['Category'].value_counts()
    category_pct = (category_counts / len(df) * 100).round(1)

    results = {
        'total_studies': len(df),
        'categories': {}
    }

    for cat in category_counts.index:
        results['categories'][cat] = {
            'count': int(category_counts[cat]),
            'percentage': float(category_pct[cat])
        }

    return results


def analyze_technology_distribution(df):
    """Analyze technology/graph type distribution (Figure 1C)."""
    tech_counts = df['Graph_Type'].value_counts()
    tech_pct = (tech_counts / len(df) * 100).round(1)

    results = {'technologies': {}}

    for tech in tech_counts.index:
        results['technologies'][tech] = {
            'count': int(tech_counts[tech]),
            'percentage': float(tech_pct[tech])
        }

    return results


def analyze_fair_compliance(df):
    """Analyze FAIR compliance distribution (Figure 1D)."""
    fair_counts = df['FAIR_Compliance'].value_counts()
    fair_pct = (fair_counts / len(df) * 100).round(1)

    results = {'fair_compliance': {}}

    for level in fair_counts.index:
        results['fair_compliance'][level] = {
            'count': int(fair_counts[level]),
            'percentage': float(fair_pct[level])
        }

    return results


def analyze_source_distribution(df):
    """Analyze source database distribution (Figure 1E)."""
    source_counts = df['Source'].value_counts()
    source_pct = (source_counts / len(df) * 100).round(1)

    results = {'sources': {}}

    for src in source_counts.index:
        results['sources'][src] = {
            'count': int(source_counts[src]),
            'percentage': float(source_pct[src])
        }

    return results


def analyze_ontology_usage(df):
    """Analyze ontology usage across studies (Figure 1F)."""
    all_ontologies = []

    for ontologies in df['Ontologies_Used'].dropna():
        ont_list = [o.strip() for o in str(ontologies).split(',')]
        all_ontologies.extend(ont_list)

    ontology_counts = pd.Series(all_ontologies).value_counts()
    ontology_pct = (ontology_counts / len(df) * 100).round(1)

    results = {'ontologies': {}}

    for ont in ontology_counts.index:
        results['ontologies'][ont] = {
            'count': int(ontology_counts[ont]),
            'percentage_of_studies': float(ontology_pct[ont])
        }

    return results


def analyze_temporal_trends(df):
    """Analyze temporal distribution of studies (Figure 1A)."""
    year_counts = df['Year'].value_counts().sort_index()

    # Calculate period statistics
    post_2022 = df[df['Year'] >= 2022]['Year'].count()
    pre_2020 = df[df['Year'] < 2020]['Year'].count()
    between = df[(df['Year'] >= 2020) & (df['Year'] < 2022)]['Year'].count()

    results = {
        'years': {},
        'periods': {
            '2022_2026': {
                'count': int(post_2022),
                'percentage': round(post_2022 / len(df) * 100, 1)
            },
            '2020_2021': {
                'count': int(between),
                'percentage': round(between / len(df) * 100, 1)
            },
            'before_2020': {
                'count': int(pre_2020),
                'percentage': round(pre_2020 / len(df) * 100, 1)
            }
        },
        'peak_year': int(year_counts.idxmax()),
        'peak_count': int(year_counts.max())
    }

    for year, count in year_counts.items():
        results['years'][str(int(year))] = int(count)

    return results


def analyze_classification_confidence(df):
    """Analyze classification confidence distribution."""
    df['Classification_Confidence'] = pd.to_numeric(df['Classification_Confidence'], errors='coerce')

    high_conf = df[df['Classification_Confidence'] >= 7]['Classification_Confidence'].count()
    med_conf = df[(df['Classification_Confidence'] >= 4) & (df['Classification_Confidence'] < 7)]['Classification_Confidence'].count()
    low_conf = df[df['Classification_Confidence'] < 4]['Classification_Confidence'].count()

    results = {
        'confidence_levels': {
            'high': {
                'threshold': '>=7',
                'count': int(high_conf),
                'percentage': round(high_conf / len(df) * 100, 1)
            },
            'medium': {
                'threshold': '4-6',
                'count': int(med_conf),
                'percentage': round(med_conf / len(df) * 100, 1)
            },
            'low': {
                'threshold': '<4',
                'count': int(low_conf),
                'percentage': round(low_conf / len(df) * 100, 1)
            }
        }
    }

    return results


def generate_summary_statistics(df):
    """Generate overall summary statistics."""
    df['Classification_Confidence'] = pd.to_numeric(df['Classification_Confidence'], errors='coerce')

    results = {
        'summary': {
            'total_studies': len(df),
            'publication_range': {
                'earliest': int(df['Year'].min()),
                'latest': int(df['Year'].max()),
                'span_years': int(df['Year'].max() - df['Year'].min() + 1)
            },
            'mean_publication_year': round(df['Year'].mean(), 1),
            'median_publication_year': int(df['Year'].median()),
            'mean_classification_confidence': round(df['Classification_Confidence'].mean(), 2),
            'categories_identified': df['Category'].nunique(),
            'unique_ontologies_used': len(set([o.strip() for ont in df['Ontologies_Used'].dropna() for o in str(ont).split(',')]))
        }
    }

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Analyze microbiome KG scoping review data'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to Supplementary_Table_1_All_Studies.csv'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for analysis reports'
    )

    args = parser.parse_args()

    # Load data
    df = load_data(args.input)

    # Run all analyses
    results = {}
    results.update(generate_summary_statistics(df))
    results['category_distribution'] = analyze_category_distribution(df)
    results['technology_distribution'] = analyze_technology_distribution(df)
    results['fair_compliance'] = analyze_fair_compliance(df)
    results['source_distribution'] = analyze_source_distribution(df)
    results['ontology_usage'] = analyze_ontology_usage(df)
    results['temporal_trends'] = analyze_temporal_trends(df)
    results['classification_confidence'] = analyze_classification_confidence(df)

    # Save results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'classification_analysis_report.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nAnalysis complete. Results saved to {output_file}")

    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total studies analyzed: {results['summary']['total_studies']}")
    print(f"Publication range: {results['summary']['publication_range']['earliest']}-{results['summary']['publication_range']['latest']}")
    print(f"Categories identified: {results['summary']['categories_identified']}")
    print(f"Unique ontologies: {results['summary']['unique_ontologies_used']}")
    print("\nKey Findings:")
    print(f"  - {results['temporal_trends']['periods']['2022_2026']['percentage']}% of studies published 2022-2026")
    print(f"  - {results['technology_distribution']['technologies']['RDF/OWL']['percentage']}% use RDF/OWL technology")
    print(f"  - {results['ontology_usage']['ontologies']['NCBITaxon']['percentage_of_studies']}% use NCBI Taxonomy")


if __name__ == '__main__':
    main()
