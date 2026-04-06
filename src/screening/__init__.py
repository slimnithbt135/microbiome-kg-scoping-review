"""
================================================================================
SCREENING MODULE - Scoping Review Screening Scripts
================================================================================

This module contains scripts for:
    - Deduplication of records across databases
    - Automated pre-screening using keyword matching
    - PRISMA diagram generation

Scripts:
    - 01_dedup_and_screen.py: Phase 1 - Deduplication and auto-screening
    - 02_fulltext_and_synthesis.py: Phase 2 - Full-text analysis and synthesis
    - prisma_diagram.py: PRISMA-ScR flow diagram generation

Usage:
    python -m src.screening.01_dedup_and_screen --help

Author: Thabet Slimani
License: MIT
"""

__version__ = "1.0.0"

from .deduplication import deduplicate_records, calculate_similarity
from .auto_screen import auto_screen_records, score_record
from .prisma_generator import generate_prisma_diagram

__all__ = [
    "deduplicate_records",
    "calculate_similarity",
    "auto_screen_records",
    "score_record",
    "generate_prisma_diagram",
]
