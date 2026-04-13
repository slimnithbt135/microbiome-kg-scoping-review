# SKGI Benchmark Protocol

## Evaluation Framework for Microbiome Knowledge Graph Systems

---

## 1. Overview

This document defines proposed benchmarking protocols for evaluating Semantic Knowledge Graph Infrastructure (SKGI) implementations. These are aspirational targets for future evaluation, not validated metrics from existing systems.

The protocols cover four proposed evaluation dimensions:
1. Link Prediction Accuracy
2. Entity Resolution Performance
3. Query Response Time
4. Explainability Metrics

---

## 2. Competency Queries (Proposed)

### CQ1: Find Microbes Associated with a Disease

Purpose: Retrieve microbial taxa associated with a specific disease, ranked by association strength.
```
SPARQL Query:
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX mondo: <http://purl.obolibrary.org/obo/MONDO_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?microbe ?microbeName ?associationScore ?pValue
WHERE {
  ?microbe skgi:associatedWith mondo:0005148 ;
           skgi:associationScore ?associationScore .
  OPTIONAL { ?microbe skgi:pValue ?pValue }
  ?microbe rdfs:label ?microbeName .
}
ORDER BY DESC(?associationScore)
LIMIT 10
```
Proposed Target Performance:
- Execution time: < 2 seconds (graphs < 500K nodes)
- Execution time: < 5 seconds (graphs < 1M nodes)

Status: Not benchmarked. Targets based on community best practices.

---

### CQ2: Identify ARGs in a Taxonomic Clade

Purpose: Find antimicrobial resistance genes carried by taxa within a specific clade.
```
SPARQL Query:
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
  FILTER (strstarts(str(?taxon), str(ncbitaxon:543)))
}
ORDER BY ?taxon
```
Proposed Target Performance:
- Execution time: < 5 seconds (graphs < 1M nodes)

Status: Not benchmarked.

---

### CQ3: Find Metabolic Pathways in Gut Samples

Purpose: Identify metabolic pathways enriched in gut microbiome samples.
```
SPARQL Query:
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX go: <http://purl.obolibrary.org/obo/GO_>
PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?sample ?pathway ?pathwayName (COUNT(?taxon) AS ?taxonCount)
WHERE {
  ?sample skgi:collectedFromSite uberon:0001155 ;
          skgi:hasTaxonomicClassification ?taxon .
  ?taxon skgi:hasFunctionalAnnotation ?pathway .
  ?pathway rdfs:label ?pathwayName .
}
GROUP BY ?sample ?pathway ?pathwayName
ORDER BY DESC(?taxonCount)
LIMIT 20
```
Proposed Target Performance:
- Execution time: < 10 seconds (graphs < 1M nodes)

Status: Not benchmarked.

---

### CQ4: Multi-hop Path Query (Gut Microbiome -> Disease)

Purpose: Discover indirect relationships between gut microbes and diseases through intermediate entities.
```
SPARQL Query:
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
Proposed Target Performance:
- Execution time: < 15 seconds (graphs < 1M nodes)

Status: Not benchmarked.

---

### CQ5: Federated Query (External Database Integration)

Purpose: Query across multiple distributed knowledge graphs.
```
SPARQL Query:
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
Proposed Target Performance:
- Execution time: < 30 seconds

Status: Not benchmarked. No federated systems found in review.

---

## 3. Link Prediction Benchmark (Proposed)

### 3.1 Dataset: CARD Gene-Drug Associations

Source: Comprehensive Antibiotic Resistance Database (CARD)

Statistics:
- Total associations: ~3,000 (estimated from CARD documentation)
- Training set: 2,400 (80%) - proposed split
- Test set: 600 (20%) - proposed split

Status: Splits not created or validated.

Format:
gene_id,drug_id,relationship
ARO:3002532,CHEBI:28971,resistance
ARO:3003982,CHEBI:28001,resistance

### 3.2 Proposed Target Metrics

| Metric | Formula | Proposed Target | Status |
|--------|---------|---------------|--------|
| MRR | (1/|Q|) sum (1/rank_i) | > 0.30 | Not validated |
| Hits@1 | |rank <= 1| / |Q| | > 0.20 | Not validated |
| Hits@3 | |rank <= 3| / |Q| | > 0.35 | Not validated |
| Hits@10 | |rank <= 10| / |Q| | > 0.50 | Not validated |
| AUC-ROC | Area under ROC curve | > 0.85 | Not validated |

Note: Targets based on general KG embedding literature, not microbiome-specific benchmarks.

### 3.3 Baseline Methods (Illustrative)

TransE implementation - EXAMPLE CODE, NOT TESTED:
```
from pykeen.models import TransE
model = TransE(triples_factory=tf, embedding_dim=128, random_seed=42)

RotatE implementation - EXAMPLE CODE, NOT TESTED:
from pykeen.models import RotatE
model = RotatE(triples_factory=tf, embedding_dim=128, random_seed=42)

R-GCN implementation - EXAMPLE CODE, NOT TESTED:
from torch_geometric.nn import RGCNConv
class RGCNModel(torch.nn.Module):
    def __init__(self, num_nodes, num_relations, hidden_dim):
        super().__init__()
        self.conv1 = RGCNConv(num_nodes, hidden_dim, num_relations)
        self.conv2 = RGCNConv(hidden_dim, hidden_dim, num_relations)

```

## 4. Entity Resolution Benchmark (Proposed)

### 4.1 Task: Taxonomic Identifier Alignment

Objective: Align taxon identifiers from different sources (NCBI, GTDB, SILVA).

Proposed Dataset:
- Source: 500 taxa from MGnify human gut studies (not curated)
- Reference: NCBI Taxonomy
- Target: GTDB and SILVA identifiers

Status: Dataset not assembled.

### 4.2 Proposed Target Metrics

| Metric | Formula | Proposed Target | Status |
|--------|---------|---------------|--------|
| Precision | TP / (TP + FP) | > 0.90 | Not validated |
| Recall | TP / (TP + FN) | > 0.80 | Not validated |
| F1-score | 2 * (P * R) / (P + R) | > 0.85 | Not validated |

### 4.3 Alignment Tools (Reference Only)

| Tool | Type | Best For |
|------|------|----------|
| LogMap | Logic-based | Large taxonomies |
| AML | Biomedical | High precision |
| PARIS | Probabilistic | Schema integration |

Note: Tool recommendations based on OAEI literature, not tested in this context.

---

## 5. Query Performance Benchmark (Proposed)

### 5.1 Proposed Test Suite

| Query ID | Description | Proposed Target Time | Status |
|----------|-------------|---------------------|--------|
| CQ1 | Disease-microbe associations | < 2 sec | Not tested |
| CQ2 | ARG identification | < 5 sec | Not tested |
| CQ3 | Metabolic pathway analysis | < 10 sec | Not tested |
| CQ4 | Multi-hop path queries | < 15 sec | Not tested |
| CQ5 | Federated queries | < 30 sec | Not tested |

### 5.2 Measurement Protocol (Illustrative)

Example benchmarking function - NOT TESTED:
```
import time
def benchmark_query(kg, query, num_runs=10):
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
### 5.3 Proposed Scalability Testing

| Graph Size | Nodes | Edges | Proposed CQ1 Time |
|------------|-------|-------|-------------------|
| Small | < 100K | < 500K | < 1 sec |
| Medium | 100K-1M | 500K-5M | < 3 sec |
| Large | 1M-10M | 5M-50M | < 10 sec |
| Very Large | > 10M | > 50M | < 30 sec |

Status: Not tested. Estimates based on general graph database performance literature.

---

## 6. Explainability Metrics (Proposed)

### 6.1 Attention-Based Explainability

For GNN models with attention mechanisms:

Example function - NOT TESTED:
```
def compute_attention_explainability(model, graph, target):
    model.eval()
    _, attention_weights = model(graph.x, graph.edge_index, return_attention_weights=True)
    edge_importance = attention_weights.argsort(descending=True)
    return edge_importance
```
### 6.2 Path-Based Explainability

Example function - NOT TESTED:
```
def extract_explanation_paths(kg, source, target, max_length=3):
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
### 6.3 Proposed Evaluation Criteria

| Criterion | Metric | Proposed Target | Status |
|-----------|--------|---------------|--------|
| Path completeness | % of true positives with explanation | > 80% | Not validated |
| Path conciseness | Average path length | < 4 hops | Not validated |
| Human interpretability | User study rating (1-5) | > 3.5 | Not validated |

---

## 7. Benchmarking Tools (Illustrative)

### 7.1 Python Script (Example Structure)

benchmark_skgi.py - EXAMPLE STRUCTURE, NOT IMPLEMENTED:
```
import json
from pathlib import Path
from datetime import datetime
from src.skgi import MicrobiomeKG  # Hypothetical module

def run_benchmarks(kg_path: Path, output_dir: Path):
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
    for cq_id, query in COMPETENCY_QUERIES.items():
        results['competency_queries'][cq_id] = benchmark_query(kg, query)
    output_file = output_dir / f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    return results
```
### 7.2 Output Format (Proposed)
```
Example output structure (values illustrative, not from actual benchmarks):
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

## 8. Reporting Results (Proposed Guidelines)

### 8.1 Minimum Reporting Requirements

When reporting benchmark results, include:
1. System specifications (Hardware, Software versions, Triple store / graph database)
2. Dataset characteristics (Number of nodes and edges, Ontologies used, Data sources)
3. Benchmark configuration (Query parameters, Number of runs, Warm-up iterations)
4. Raw results (Mean, median, min, max, std, Confidence intervals)

---

## 9. References

1. Ji S, et al. (2022). A survey on knowledge graphs. IEEE TNNLS.
2. Wu Z, et al. (2021). A comprehensive survey on graph neural networks. IEEE TNNLS.
3. Alshahrani M, et al. (2017). Neuro-symbolic representation learning on biological knowledge graphs. Bioinformatics.

---

Document version: 1.0
Last updated: April , 2026
Status: PROPOSED FRAMEWORK - Not validated or benchmarked
Maintainer: [Thabet Slimani - thabet.slimani@gmail.com]
