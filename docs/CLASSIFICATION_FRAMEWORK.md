# Classification Framework

## Six-Category Taxonomy for Microbiome Knowledge Graph Systems

---

## Overview

Based on analysis of 54 included studies, we developed a six-category classification framework that captures the major approaches to microbiome knowledge graph construction and analysis.

---

## Category 1: MDKG-type (Microbe-Disease Knowledge Graphs)

### Definition
Systems focusing on modeling associations between microbial entities and disease phenotypes, typically integrating taxonomic data with disease ontologies.

### Inclusion Criteria
- [ ] Primary focus on microbe-disease associations
- [ ] Integration of taxonomic data with disease ontologies (DOID, MONDO)
- [ ] Support for association scoring or pathway analysis
- [ ] Human health or disease context

### Key Characteristics
| Feature | Typical Implementation |
|---------|----------------------|
| Graph type | RDF/OWL |
| Primary ontologies | NCBITaxon, DOID/MONDO |
| Scale | ~5K-50K nodes |
| Analytics | Association scoring, Pathway analysis |
| FAIR compliance | Low-Moderate |

### Representative Studies
- MDADP (Wang et al., 2022)
- MINERVA (Langarica et al., 2025)
- MMiKG (Sun et al., 2023)

### Strengths
- Clear clinical relevance
- Interpretable associations
- Well-established methods

### Limitations
- Limited contextual factors (host, environment)
- Static associations
- Custom schemas

---

## Category 2: KG-Microbe-type (Modular Microbial Knowledge Graphs)

### Definition
Systems emphasizing semantic rigor through ontology-driven design with modular architecture, typically aligned with OBO Foundry standards.

### Inclusion Criteria
- [ ] RDF/OWL representation
- [ ] Integration of multiple OBO Foundry ontologies
- [ ] Support for SPARQL querying and logical reasoning
- [ ] Modular, extensible architecture

### Key Characteristics
| Feature | Typical Implementation |
|---------|----------------------|
| Graph type | RDF/OWL (OBO compliant) |
| Primary ontologies | NCBITaxon, GO, ChEBI, OMP, MCO |
| Scale | ~10K-500K nodes |
| Analytics | Ontology reasoning, SPARQL queries |
| FAIR compliance | High |

### Representative Studies
- Gene Ontology microbial extensions (Godbold et al., 2025)
- Ontology-aware neural networks (Zha & Ning, 2022)
- OHMI (He et al., 2019)

### Strengths
- High semantic rigor
- Strong interoperability
- Formal reasoning capabilities
- FAIR compliance

### Limitations
- Complexity
- Computational requirements
- Limited analytical flexibility

---

## Category 3: MicrobiomeKG-type (Host-Microbiome Integration)

### Definition
Systems capturing complex interactions between microbial communities and host biological processes, often leveraging cross-domain schema frameworks.

### Inclusion Criteria
- [ ] Integration of microbiome data with host ontologies
- [ ] Multi-layered analysis capabilities
- [ ] Use of schema frameworks (Biolink, etc.)
- [ ] Host-microbe interaction focus

### Key Characteristics
| Feature | Typical Implementation |
|---------|----------------------|
| Graph type | RDF/OWL + Schema frameworks |
| Primary ontologies | Biolink, GO, ChEBI, UBERON |
| Scale | ~25K-50K nodes |
| Analytics | Centrality, embeddings, multi-layer analysis |
| FAIR compliance | High |

### Representative Studies
- Polarity-Aware KG (Li et al., 2026)
- Host-microbiome integrative systems

### Strengths
- Captures host-microbe complexity
- Cross-domain integration
- Advanced analytics

### Limitations
- Data harmonization challenges
- Limited number of systems
- Scalability concerns

---

## Category 4: BRIDGE-type (AMR Prediction using KG Embeddings)

### Definition
Systems using knowledge graph embeddings for antimicrobial resistance prediction and gene-drug association discovery.

### Inclusion Criteria
- [ ] Use of embedding methods (TransE, RotatE, etc.)
- [ ] Focus on AMR gene-drug associations
- [ ] Link prediction capabilities
- [ ] CARD or similar AMR database integration

### Key Characteristics
| Feature | Typical Implementation |
|---------|----------------------|
| Graph type | KG Embeddings |
| Primary ontologies | CARD, DrugBank, KEGG |
| Scale | ~50K-150K nodes |
| Analytics | Link prediction, embedding scoring |
| FAIR compliance | Moderate |

### Representative Studies
- AMR-BRIDGE (Santos et al., 2024)
- Knowledge graph embedding for microbial interactions (Khatbane et al., 2025)

### Strengths
- Strong predictive performance
- Handles large-scale data
- Discovers novel associations

### Limitations
- Limited interpretability
- "Black box" nature
- Semantic transparency issues

---

## Category 5: MINERVA-type (Diet-Environment-Microbiome)

### Definition
Systems modeling interactions among dietary exposures, environmental factors, and microbial communities, typically employing property graph databases.

### Inclusion Criteria
- [ ] Property graph representation (Neo4j)
- [ ] Multi-dimensional relationship modeling
- [ ] Network exploration capabilities
- [ ] Diet/environment context

### Key Characteristics
| Feature | Typical Implementation |
|---------|----------------------|
| Graph type | Property Graph (Neo4j) |
| Primary ontologies | Custom schemas, FOODON, ENVO |
| Scale | ~40K-80K nodes |
| Analytics | Network exploration, Path analysis |
| FAIR compliance | Moderate |

### Representative Studies
- HerbMicrobeDB (Bastola, 2018)
- Food4healthKG (Fu et al., 2023)

### Strengths
- Flexible schema
- High-performance traversal
- Intuitive visualization

### Limitations
- Limited standardization
- Interoperability challenges
- Custom schema maintenance

---

## Category 6: AMR-GNN-type (Graph Neural Network Approaches)

### Definition
Systems employing graph neural networks for antimicrobial resistance classification and predictive analytics.

### Inclusion Criteria
- [ ] Use of GNN architectures (R-GCN, GAT, etc.)
- [ ] Multi-modal genomic and interaction data
- [ ] Attention mechanisms for explainability
- [ ] Classification or prediction focus

### Key Characteristics
| Feature | Typical Implementation |
|---------|----------------------|
| Graph type | Multi-modal GNN |
| Primary ontologies | CARD, KEGG, UniProt |
| Scale | ~150K-500K nodes |
| Analytics | R-GCN, GAT, attention-based models |
| FAIR compliance | Moderate |

### Representative Studies
- GNN-GBA (Aamer Naafey et al., 2025)
- DeepARG (Arango-Argoty et al., 2018)

### Strengths
- State-of-the-art predictive performance
- Handles heterogeneous data
- Attention-based explainability

### Limitations
- Complex training requirements
- Limited semantic grounding
- Computational intensity


## Classification Decision Tree
```
Start
│
├─► Microbiome-related? ──► NO ──► Exclude (E1)
│
├─► Knowledge graph approach? ──► NO ──► Exclude (E2)
│
├─► Disease association focus? ──► YES ──► MDKG-type
│
├─► OBO Foundry ontologies? ──► YES ──► KG-Microbe-type
│
├─► Host-microbiome integration? ──► YES ──► MicrobiomeKG-type
│
├─► KG embeddings for AMR? ──► YES ──► BRIDGE-type
│
├─► Property graph (Neo4j)? ──► YES ──► MINERVA-type
│
├─► GNN for AMR? ──► YES ──► AMR-GNN-type
│
└─► Other ──► Review manually

```

## Classification Validation and Limitations

### Single-Reviewer Process
Classification was conducted by a single reviewer (the author) using the decision logic illustrated in Figure 7. No inter-rater reliability assessment was performed. The taxonomy should be interpreted as an organizational framework requiring external validation in future work.

### Classification Confidence
To flag borderline cases, a qualitative confidence score (1–10) was self-assigned based on the clarity of match between a study's stated objective, its data model, and its graph technology stack:

| Confidence Level | Score Range | Studies | Percentage |
|------------------|-------------|---------|------------|
| High | ≥7 | 6 | 11.1% |
| Medium | 4-6 | 22 | 40.7% |
| Low | <4 | 26 | 48.1% |

Low confidence scores indicate cases where primary objectives spanned multiple categories or methodological details were ambiguous.

---

## Category Distribution
```
MDKG-type        ██████████████████████████  46.3% (25)
KG-Microbe-type  ████████████████████████    42.6% (23)
MicrobiomeKG-type ██                         3.7% (2)
BRIDGE-type      ██                         3.7% (2)
MINERVA-type     █                          1.9% (1)
AMR-GNN-type     █                          1.9% (1)

```
## Temporal Trends by Category

| Period | MDKG-type | KG-Microbe-type | Other |
|--------|-----------|-----------------|-------|
| 2006-2015 | 4 | 8 | 0 |
| 2016-2020 | 6 | 5 | 1 |
| 2021-2026 | 15 | 10 | 4 |

Recent growth is observed in all categories, with MDKG-type showing the strongest acceleration.

---

## References

1. Wang L, et al. (2022). MDADP: A webserver integrating database and prediction tools for microbe-disease associations. IEEE JBHI.
2. Langarica S, et al. (2025). MINERVA-microbiome network research and visualization atlas. Brief Bioinform.
3. Godbold G, et al. (2025). New and revised gene ontology biological process terms. J Biomed Semantics.
4. Zha Y, Ning K. (2022). Ontology-aware neural network for pattern mining from microbiome data. Brief Bioinform.
5. Santos RAD, et al. (2024). A web-based network analysis tool for metagenomic analysis of resistomes. IISA.

---

**Document version:** 1.0  
**Last updated:** April 13, 2026  
**Maintainer:** [Thabet Slimani - thabet.slimani@gmail.com]
