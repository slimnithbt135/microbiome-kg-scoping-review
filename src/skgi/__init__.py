"""
================================================================================
SKGI - SEMANTIC KNOWLEDGE GRAPH INFRASTRUCTURE
================================================================================

Implementation of the Semantic Knowledge Graph Infrastructure for 
Microbiome Intelligence as proposed in the scoping review.

This module provides:
    - Core schema definitions (OWL, SHACL)
    - Data ingestion pipelines
    - Validation utilities
    - Query templates
    - Benchmarking tools

Usage:
    from src.skgi import MicrobiomeKG
    
    # Create a new knowledge graph
    kg = MicrobiomeKG()
    
    # Load ontologies
    kg.load_ontologies()
    
    # Add sample data
    kg.add_sample(sample_id="S001", taxa=["562", "1613"])

Author: Thabet Slimani
License: MIT
"""

__version__ = "1.0.0"

from .core_schema import SKGI_SCHEMA, SKGI_NAMESPACES
from .validation import SHACLValidator
from .ingestion import MGnifyIngestor, CARDIngestor
from .knowledge_graph import MicrobiomeKG

__all__ = [
    "SKGI_SCHEMA",
    "SKGI_NAMESPACES",
    "SHACLValidator",
    "MGnifyIngestor",
    "CARDIngestor",
    "MicrobiomeKG",
]
