# SKGI Benchmark Protocol

## Evaluation Framework for Microbiome Knowledge Graph Systems

---

## 1. Overview

This document defines standardized benchmarking protocols for evaluating Semantic Knowledge Graph Infrastructure (SKGI) implementations. The protocols cover four evaluation dimensions:

1. Link Prediction Accuracy
2. Entity Resolution Performance
3. Query Response Time
4. Explainability Metrics

---

## 2. Competency Queries

### CQ1: Find Microbes Associated with a Disease

**Purpose:** Retrieve microbial taxa associated with a specific disease, ranked by association strength.

**SPARQL Query:**
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX mondo: <http://purl.obolibrary.org/obo/MONDO_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?microbe ?microbeName ?associationScore ?pValue
WHERE {
  ?microbe skgi:associatedWith mondo:0005148 ;  # Type 2 diabetes
           skgi:associationScore ?associationScore .
  OPTIONAL { ?microbe skgi:pValue ?pValue }
  ?microbe rdfs:label ?microbeName .
}
ORDER BY DESC(?associationScore)
LIMIT 10
```

**Target Performance:**
- Execution time: < 2 seconds (graphs < 500K nodes)
- Execution time: < 5 seconds (graphs < 1M nodes)

---

### CQ2: Identify ARGs in a Taxonomic Clade

**Purpose:** Find antimicrobial resistance genes carried by taxa within a specific clade.

**SPARQL Query:**
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/NCBITaxon_>
PREFIX card: <https://card.mcmaster.ca/aro/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?taxon ?taxonName ?arg ?argName ?drug ?mechanism
WHERE {
  ?taxon skgi:carriesARG ?arg ;
         rdfs:label ?taxonName .
  ?arg rdfs:label ?argName ;
       skgi:confersResistanceTo ?drug ;
       card:hasResistanceMechanism ?mechanism .
  
  # Filter by taxonomic clade (e.g., Enterobacteriaceae: NCBITaxon:543)
  FILTER (strstarts(str(?taxon), str(ncbitaxon:543)))
}
ORDER BY ?taxon
```

**Target Performance:**
- Execution time: < 5 seconds (graphs < 1M nodes)

---

### CQ3: Find Metabolic Pathways in Gut Samples

**Purpose:** Identify metabolic pathways enriched in gut microbiome samples.

**SPARQL Query:**
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX go: <http://purl.obolibrary.org/obo/GO_>
PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?sample ?pathway ?pathwayName (COUNT(?taxon) AS ?taxonCount)
WHERE {
  ?sample skgi:collectedFromSite uberon:0001155 ;  # large intestine
          skgi:hasTaxonomicClassification ?taxon .
  ?taxon skgi:hasFunctionalAnnotation ?pathway .
  ?pathway rdfs:label ?pathwayName .
}
GROUP BY ?sample ?pathway ?pathwayName
ORDER BY DESC(?taxonCount)
LIMIT 20
```

**Target Performance:**
- Execution time: < 10 seconds (graphs < 1M nodes)

---

### CQ4: Multi-hop Path Query (Gut Microbiome → Disease)

**Purpose:** Discover indirect relationships between gut microbes and diseases through intermediate entities.

**SPARQL Query:**
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?microbe ?compound ?disease (count(*) as ?pathCount)
WHERE {
  ?sample skgi:collectedFromSite uberon:0001155 ;
          skgi:hasTaxonomicClassification ?microbe .
  ?microbe skgi:produces ?compound .
  ?compound skgi:associatedWith ?disease .
}
GROUP BY ?microbe ?compound ?disease
ORDER BY DESC(?pathCount)
LIMIT 10
```

**Target Performance:**
- Execution time: < 15 seconds (graphs < 1M nodes)

---

### CQ5: Federated Query (External Database Integration)

**Purpose:** Query across multiple distributed knowledge graphs.

**SPARQL Query:**
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX service: <http://skgi.org/service/>

SELECT ?sample ?taxon ?externalData
WHERE {
  ?sample skgi:hasTaxonomicClassification ?taxon .
  
  SERVICE service:ncbi {
    ?taxon skgi:ncbiTaxonId ?ncbiId .
  }
  
  SERVICE service:ebi {
    ?taxon skgi:ebiReference ?externalData .
  }
}
```

**Target Performance:**
- Execution time: < 30 seconds

---

## 3. Link Prediction Benchmark

### 3.1 Dataset: CARD Gene-Drug Associations

**Source:** Comprehensive Antibiotic Resistance Database (CARD)

**Statistics:**
- Total associations: ~3,000
- Training set: 2,400 (80%)
- Test set: 600 (20%)

**Format:**
```
gene_id,drug_id,relationship
ARO:3002532,CHEBI:28971,resistance
ARO:3003982,CHEBI:28001,resistance
...
```

### 3.2 Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **MRR** | (1/\|Q\|) Σ (1/rank_i) | > 0.30 |
| **Hits@1** | \|rank ≤ 1\| / \|Q\| | > 0.20 |
| **Hits@3** | \|rank ≤ 3\| / \|Q\| | > 0.35 |
| **Hits@10** | \|rank ≤ 10\| / \|Q\| | > 0.50 |
| **AUC-ROC** | Area under ROC curve | > 0.85 |

### 3.3 Baseline Methods

```python
# TransE implementation
from pykeen.models import TransE

model = TransE(
    triples_factory=tf,
    embedding_dim=128,
    random_seed=42
)

# RotatE implementation
from pykeen.models import RotatE

model = RotatE(
    triples_factory=tf,
    embedding_dim=128,
    random_seed=42
)

# R-GCN implementation
from torch_geometric.nn import RGCNConv

class RGCNModel(torch.nn.Module):
    def __init__(self, num_nodes, num_relations, hidden_dim):
        super().__init__()
        self.conv1 = RGCNConv(num_nodes, hidden_dim, num_relations)
        self.conv2 = RGCNConv(hidden_dim, hidden_dim, num_relations)
```

---

## 4. Entity Resolution Benchmark

### 4.1 Task: Taxonomic Identifier Alignment

**Objective:** Align taxon identifiers from different sources (NCBI, GTDB, SILVA).

**Dataset:**
- Source: 500 taxa from MGnify human gut studies
- Reference: NCBI Taxonomy
- Target: GTDB and SILVA identifiers

### 4.2 Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Precision** | TP / (TP + FP) | > 0.90 |
| **Recall** | TP / (TP + FN) | > 0.80 |
| **F1-score** | 2 × (P × R) / (P + R) | > 0.85 |

### 4.3 Alignment Tools

| Tool | Type | Best For |
|------|------|----------|
| LogMap | Logic-based | Large taxonomies |
| AML | Biomedical | High precision |
| PARIS | Probabilistic | Schema integration |

---

## 5. Query Performance Benchmark

### 5.1 Test Suite

| Query ID | Description | Target Time |
|----------|-------------|-------------|
| CQ1 | Disease-microbe associations | < 2 sec |
| CQ2 | ARG identification | < 5 sec |
| CQ3 | Metabolic pathway analysis | < 10 sec |
| CQ4 | Multi-hop path queries | < 15 sec |
| CQ5 | Federated queries | < 30 sec |

### 5.2 Measurement Protocol

```python
import time

def benchmark_query(kg, query, num_runs=10):
    """Benchmark a SPARQL query."""
    times = []
    
    for _ in range(num_runs):
        start = time.time()
        kg.query(query)
        elapsed = time.time() - start
        times.append(elapsed)
    
    return {
        'mean': sum(times) / len(times),
        'median': sorted(times)[len(times)//2],
        'min': min(times),
        'max': max(times),
        'std': statistics.stdev(times)
    }
```

### 5.3 Scalability Testing

| Graph Size | Nodes | Edges | Expected CQ1 Time |
|------------|-------|-------|-------------------|
| Small | < 100K | < 500K | < 1 sec |
| Medium | 100K-1M | 500K-5M | < 3 sec |
| Large | 1M-10M | 5M-50M | < 10 sec |
| Very Large | > 10M | > 50M | < 30 sec |

---

## 6. Explainability Metrics

### 6.1 Attention-Based Explainability

For GNN models with attention mechanisms:

```python
def compute_attention_explainability(model, graph, target):
    """Compute attention-based explainability scores."""
    model.eval()
    
    # Get attention weights
    _, attention_weights = model(graph.x, graph.edge_index, return_attention_weights=True)
    
    # Rank edges by attention weight
    edge_importance = attention_weights.argsort(descending=True)
    
    return edge_importance
```

### 6.2 Path-Based Explainability

```python
def extract_explanation_paths(kg, source, target, max_length=3):
    """Extract paths between source and target entities."""
    query = f"""
    PREFIX skgi: <http://skgi.org/ontology/>
    
    SELECT ?path
    WHERE {{
      ?path skgi:connects <{source}> , <{target}> .
    }}
    LIMIT {max_length}
    """
    
    return kg.query(query)
```

### 6.3 Evaluation Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| Path completeness | % of true positives with explanation | > 80% |
| Path conciseness | Average path length | < 4 hops |
| Human interpretability | User study rating (1-5) | > 3.5 |

---

## 7. Benchmarking Tools

### 7.1 Python Script

```python
# benchmark_skgi.py
import json
from pathlib import Path
from datetime import datetime

from src.skgi import MicrobiomeKG

def run_benchmarks(kg_path: Path, output_dir: Path):
    """Run all SKGI benchmarks."""
    
    kg = MicrobiomeKG()
    kg.load(kg_path)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'kg_size': kg.get_statistics(),
        'competency_queries': {},
        'link_prediction': {},
        'entity_resolution': {},
        'explainability': {}
    }
    
    # Run competency queries
    for cq_id, query in COMPETENCY_QUERIES.items():
        results['competency_queries'][cq_id] = benchmark_query(kg, query)
    
    # Save results
    output_file = output_dir / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results
```

### 7.2 Output Format

```json
{
  "timestamp": "2026-04-05T10:30:00",
  "kg_size": {
    "nodes": 150000,
    "edges": 750000
  },
  "competency_queries": {
    "CQ1": {
      "mean": 1.23,
      "median": 1.15,
      "min": 0.98,
      "max": 1.45,
      "std": 0.12
    }
  },
  "link_prediction": {
    "mrr": 0.32,
    "hits@1": 0.22,
    "hits@10": 0.54,
    "auc_roc": 0.87
  }
}
```

---

## 8. Reporting Results

### 8.1 Minimum Reporting Requirements

When reporting benchmark results, include:

1. **System specifications**
   - Hardware (CPU, RAM, storage)
   - Software versions
   - Triple store / graph database

2. **Dataset characteristics**
   - Number of nodes and edges
   - Ontologies used
   - Data sources

3. **Benchmark configuration**
   - Query parameters
   - Number of runs
   - Warm-up iterations

4. **Raw results**
   - Mean, median, min, max, std
   - Confidence intervals

---

## 9. References

1. Ji S, et al. (2022). A survey on knowledge graphs. IEEE TNNLS.
2. Wu Z, et al. (2021). A comprehensive survey on graph neural networks. IEEE TNNLS.
3. Alshahrani M, et al. (2017). Neuro-symbolic representation learning on biological knowledge graphs. Bioinformatics.

---

**Document version:** 1.0  
**Last updated:** April 5, 2026  
**Maintainer:** Thabet Slimani (t.slimani@tu.edu.sa)
