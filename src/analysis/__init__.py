"""
================================================================================
ANALYSIS MODULE - Scoping Review Analysis Scripts
================================================================================

This module contains scripts for:
    - Classification analysis of included studies
    - Trend visualization
    - Statistical summaries
    - Ontology usage analysis

Scripts:
    - classification_analysis.py: Analyze study classifications
    - trend_visualization.py: Generate trend figures
    - statistics.py: Calculate summary statistics

Usage:
    python -m src.analysis.classification_analysis --help

Author: Thabet Slimani
License: MIT
"""

__version__ = "1.0.0"

from .classification import classify_studies, calculate_category_distribution
from .trends import analyze_temporal_trends, generate_trend_figures
from .statistics import calculate_summary_stats, generate_report

__all__ = [
    "classify_studies",
    "calculate_category_distribution",
    "analyze_temporal_trends",
    "generate_trend_figures",
    "calculate_summary_stats",
    "generate_report",
]
