"""
================================================================================
SCOPING REVIEW - MICROBIOME KNOWLEDGE GRAPHS
================================================================================

A reproducible scoping review following PRISMA-ScR guidelines.

This package contains:
    - screening: Deduplication and screening scripts
    - analysis: Classification and trend analysis
    - skgi: Semantic Knowledge Graph Infrastructure implementation

Author: Thabet Slimani
License: MIT
Repository: https://github.com/username/microbiome-kg-scoping-review
"""

__version__ = "1.0.0"
__author__ = "Thabet Slimani"
__email__ = "t.slimani@tu.edu.sa"

from pathlib import Path

# Define package root
PACKAGE_ROOT = Path(__file__).parent
DATA_DIR = PACKAGE_ROOT.parent / "data"
OUTPUTS_DIR = PACKAGE_ROOT.parent / "outputs"

__all__ = [
    "PACKAGE_ROOT",
    "DATA_DIR",
    "OUTPUTS_DIR",
]
