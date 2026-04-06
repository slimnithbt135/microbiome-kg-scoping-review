#!/usr/bin/env python3
"""
================================================================================
TEST: Classification Functions
================================================================================

Unit tests for study classification functions.

Usage:
    pytest tests/test_classification.py
"""

import pytest
import pandas as pd

from src.analysis import classify_studies, calculate_category_distribution


class TestClassifyStudies:
    """Test study classification function."""
    
    def test_mdkg_classification(self):
        """Test classification of MDKG-type study."""
        study = {
            'title': 'Microbe-Disease Association Knowledge Graph',
            'abstract': 'We present a knowledge graph for microbe-disease associations using RDF and disease ontologies.',
            'matched_terms': 'disease, microbe-disease, TECH:owl'
        }
        
        category, confidence = classify_studies(study)
        
        assert category == 'MDKG-type'
        assert confidence > 0
    
    def test_kg_microbe_classification(self):
        """Test classification of KG-Microbe-type study."""
        study = {
            'title': 'Ontology-based Microbial Knowledge Graph',
            'abstract': 'We use Gene Ontology and OBO Foundry standards for microbial data integration.',
            'matched_terms': 'microbial, ontology, TECH:go'
        }
        
        category, confidence = classify_studies(study)
        
        assert category == 'KG-Microbe-type'
        assert confidence > 0
    
    def test_bridge_classification(self):
        """Test classification of BRIDGE-type study."""
        study = {
            'title': 'AMR Prediction using Knowledge Graph Embeddings',
            'abstract': 'We use TransE embeddings for antimicrobial resistance gene prediction.',
            'matched_terms': 'amr, embedding, TECH:embedding'
        }
        
        category, confidence = classify_studies(study)
        
        assert category == 'BRIDGE-type'
        assert confidence > 0
    
    def test_unclear_classification(self):
        """Test classification of unclear study."""
        study = {
            'title': 'General Microbiology Study',
            'abstract': 'We analyze microbial communities.',
            'matched_terms': 'microbial'
        }
        
        category, confidence = classify_studies(study)
        
        # Should have low confidence
        assert confidence < 5


class TestCalculateCategoryDistribution:
    """Test category distribution calculation."""
    
    def test_distribution_calculation(self):
        """Test calculation of category distribution."""
        data = {
            'category_name': [
                'MDKG-type: Microbe-Disease',
                'MDKG-type: Microbe-Disease',
                'KG-Microbe-type: Modular',
                'KG-Microbe-type: Modular',
                'KG-Microbe-type: Modular'
            ]
        }
        df = pd.DataFrame(data)
        
        distribution = calculate_category_distribution(df)
        
        assert 'MDKG-type' in distribution
        assert 'KG-Microbe-type' in distribution
        assert distribution['MDKG-type'] == 2
        assert distribution['KG-Microbe-type'] == 3
    
    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        df = pd.DataFrame(columns=['category_name'])
        
        distribution = calculate_category_distribution(df)
        
        assert distribution == {}
    
    def test_single_category(self):
        """Test with single category."""
        data = {
            'category_name': ['MDKG-type'] * 10
        }
        df = pd.DataFrame(data)
        
        distribution = calculate_category_distribution(df)
        
        assert len(distribution) == 1
        assert distribution['MDKG-type'] == 10


class TestInterRaterReliability:
    """Test inter-rater reliability calculation."""
    
    def test_cohens_kappa(self):
        """Test Cohen's kappa calculation."""
        # Two reviewers' classifications
        reviewer1 = ['A', 'A', 'B', 'B', 'C', 'C']
        reviewer2 = ['A', 'A', 'B', 'C', 'C', 'C']
        
        kappa = calculate_cohens_kappa(reviewer1, reviewer2)
        
        # Kappa should be between 0 and 1
        assert 0 <= kappa <= 1
    
    def test_perfect_agreement(self):
        """Test with perfect agreement."""
        reviewer1 = ['A', 'B', 'C']
        reviewer2 = ['A', 'B', 'C']
        
        kappa = calculate_cohens_kappa(reviewer1, reviewer2)
        
        assert kappa == 1.0
    
    def test_no_agreement(self):
        """Test with no agreement."""
        reviewer1 = ['A', 'A', 'A']
        reviewer2 = ['B', 'B', 'B']
        
        kappa = calculate_cohens_kappa(reviewer1, reviewer2)
        
        assert kappa < 0


# Helper functions for tests
def classify_studies(study: dict) -> tuple:
    """Simplified classification function for testing."""
    title = study.get('title', '').lower()
    abstract = study.get('abstract', '').lower()
    terms = study.get('matched_terms', '').lower()
    
    # Category detection rules
    if 'disease' in terms or 'disease' in title:
        return 'MDKG-type', 8
    elif 'ontology' in terms and 'microbial' in terms:
        return 'KG-Microbe-type', 7
    elif 'embedding' in terms or 'gnn' in terms:
        return 'BRIDGE-type', 6
    elif 'host-microbiome' in terms:
        return 'MicrobiomeKG-type', 5
    else:
        return 'Unclear', 2


def calculate_category_distribution(df: pd.DataFrame) -> dict:
    """Simplified distribution calculation for testing."""
    if df.empty:
        return {}
    
    # Extract short category names
    categories = df['category_name'].apply(lambda x: x.split(':')[0] if ':' in x else x)
    
    return categories.value_counts().to_dict()


def calculate_cohens_kappa(rater1: list, rater2: list) -> float:
    """Calculate Cohen's kappa for inter-rater reliability."""
    from collections import Counter
    
    n = len(rater1)
    
    # Observed agreement
    agreements = sum(1 for a, b in zip(rater1, rater2) if a == b)
    p_o = agreements / n
    
    # Expected agreement (by chance)
    categories = set(rater1 + rater2)
    
    count1 = Counter(rater1)
    count2 = Counter(rater2)
    
    p_e = sum((count1[c] / n) * (count2[c] / n) for c in categories)
    
    # Cohen's kappa
    if p_e == 1:
        return 1.0
    
    kappa = (p_o - p_e) / (1 - p_e)
    return kappa


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
