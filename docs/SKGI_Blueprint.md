# SKGI Implementation Blueprint
## Semantic Knowledge Graph Infrastructure for Microbiome Intelligence

---

## Executive Summary

This document provides concrete technical specifications for implementing the Semantic Knowledge Graph Infrastructure (SKGI) proposed in the scoping review. It transforms the conceptual four-layer architecture into an actionable blueprint with specific technologies, schemas, and evaluation protocols.

---

## Part 1: Core Schema Specification

### 1.1 Namespace Declarations

```turtle
@prefix skgi: <http://skgi.org/ontology/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ncbitaxon: <http://purl.obolibrary.org/obo/NCBITaxon_> .
@prefix go: <http://purl.obolibrary.org/obo/GO_> .
@prefix chebi: <http://purl.obolibrary.org/obo/CHEBI_> .
@prefix mondo: <http://purl.obolibrary.org/obo/MONDO_> .
@prefix uberon: <http://purl.obolibrary.org/obo/UBERON_> .
@prefix envo: <http://purl.obolibrary.org/obo/ENVO_> .
@prefix foodon: <http://purl.obolibrary.org/obo/FOODON_> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix sio: <http://semanticscience.org/resource/> .
```

### 1.2 Core Classes

```turtle
# Microbial Taxon
skgi:MicrobialTaxon
    a owl:Class ;
    rdfs:label "Microbial Taxon"@en ;
    rdfs:comment "A taxonomic classification of a microorganism according to NCBI Taxonomy"@en ;
    owl:equivalentClass ncbitaxon:Organism ;
    skos:definition "Any organism classified in the NCBI Taxonomy database" .

# Microbial Sample
skgi:MicrobialSample
    a owl:Class ;
    rdfs:label "Microbial Sample"@en ;
    rdfs:comment "A biological sample containing microbial communities"@en ;
    skos:definition "A collected specimen containing microorganisms for analysis" .

# Host Organism
skgi:HostOrganism
    a owl:Class ;
    rdfs:label "Host Organism"@en ;
    rdfs:comment "An organism that harbors a microbial community"@en ;
    owl:equivalentClass ncbitaxon:Organism .

# Microbial Function
skgi:MicrobialFunction
    a owl:Class ;
    rdfs:label "Microbial Function"@en ;
    rdfs:comment "A biological function or process performed by microorganisms"@en ;
    owl:equivalentClass go:GO_0008150 .  # biological_process

# Chemical Compound
skgi:ChemicalCompound
    a owl:Class ;
    rdfs:label "Chemical Compound"@en ;
    rdfs:comment "A chemical substance of biological relevance"@en ;
    owl:equivalentClass chebi:CHEBI_24431 .  # chemical entity

# Disease
skgi:Disease
    a owl:Class ;
    rdfs:label "Disease"@en ;
    rdfs:comment "A disease or pathological condition"@en ;
    owl:equivalentClass mondo:MONDO_0000001 .  # disease

# Antimicrobial Resistance Gene
skgi:ARG
    a owl:Class ;
    rdfs:label "Antimicrobial Resistance Gene"@en ;
    rdfs:comment "A gene conferring resistance to antimicrobial agents"@en ;
    skos:definition "A gene that reduces the effectiveness of antimicrobial drugs" .

# Environment
skgi:Environment
    a owl:Class ;
    rdfs:label "Environment"@en ;
    rdfs:comment "An environmental context or habitat"@en ;
    owl:equivalentClass envo:ENVO_01000254 .  # environmental system
```

### 1.3 Object Properties (Relationships)

```turtle
# Taxonomic classification
skgi:hasTaxonomicClassification
    a owl:ObjectProperty ;
    rdfs:label "has taxonomic classification"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:MicrobialTaxon ;
    skos:definition "Links a sample to its constituent microbial taxa" .

# Functional annotation
skgi:hasFunctionalAnnotation
    a owl:ObjectProperty ;
    rdfs:label "has functional annotation"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:MicrobialFunction ;
    skos:definition "Links a microbe to its functional capabilities" .

# Host association
skgi:collectedFromHost
    a owl:ObjectProperty ;
    rdfs:label "collected from host"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:HostOrganism ;
    skos:definition "Indicates the host organism from which a sample was collected" .

# Host body site
skgi:collectedFromSite
    a owl:ObjectProperty ;
    rdfs:label "collected from site"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range uberon:UBERON_0001062 ;  # anatomical entity
    skos:definition "Indicates the anatomical site from which a sample was collected" .

# Disease association
skgi:associatedWith
    a owl:ObjectProperty ;
    rdfs:label "associated with"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:Disease ;
    skos:definition "Indicates an association between a microbe and a disease" .

# Chemical interaction
skgi:produces
    a owl:ObjectProperty ;
    rdfs:label "produces"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:ChemicalCompound ;
    skos:definition "Indicates that a microbe produces a chemical compound" .

# AMR relationship
skgi:confersResistanceTo
    a owl:ObjectProperty ;
    rdfs:label "confers resistance to"@en ;
    rdfs:domain skgi:ARG ;
    rdfs:range skgi:ChemicalCompound ;
    skos:definition "Indicates that an ARG confers resistance to an antimicrobial compound" .

skgi:carriesARG
    a owl:ObjectProperty ;
    rdfs:label "carries ARG"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:ARG ;
    skos:definition "Indicates that a microbe carries an antimicrobial resistance gene" .

# Environmental context
skgi:collectedFromEnvironment
    a owl:ObjectProperty ;
    rdfs:label "collected from environment"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:Environment ;
    skos:definition "Indicates the environmental context of a sample" .

# Provenance
skgi:derivedFrom
    a owl:ObjectProperty ;
    rdfs:label "derived from"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range prov:Entity ;
    skos:definition "Links a sample to its source data or study" .
```

### 1.4 Data Properties

```turtle
# Sample metadata
skgi:sampleId
    a owl:DatatypeProperty ;
    rdfs:label "sample identifier"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range xsd:string .

skgi:collectionDate
    a owl:DatatypeProperty ;
    rdfs:label "collection date"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range xsd:date .

skgi:abundance
    a owl:DatatypeProperty ;
    rdfs:label "abundance"@en ;
    rdfs:domain skgi:hasTaxonomicClassification ;
    rdfs:range xsd:float ;
    skos:definition "Relative abundance of a taxon in a sample (0.0 to 1.0)" .

# Association scores
skgi:associationScore
    a owl:DatatypeProperty ;
    rdfs:label "association score"@en ;
    rdfs:domain skgi:associatedWith ;
    rdfs:range xsd:float ;
    skos:definition "Statistical score indicating strength of association" .

skgi:pValue
    a owl:DatatypeProperty ;
    rdfs:label "p-value"@en ;
    rdfs:domain skgi:associatedWith ;
    rdfs:range xsd:float .

# Provenance
skgi:dataSource
    a owl:DatatypeProperty ;
    rdfs:label "data source"@en ;
    rdfs:domain prov:Entity ;
    rdfs:range xsd:string ;
    skos:definition "Original database or repository of the data" .

skgi:accessDate
    a owl:DatatypeProperty ;
    rdfs:label "access date"@en ;
    rdfs:domain prov:Entity ;
    rdfs:range xsd:dateTime .
```

---

## Part 2: Technology Stack Recommendations

### 2.1 By Scale

#### Small Scale (< 100,000 nodes)

| Component | Recommendation | Version | Rationale |
|-----------|---------------|---------|-----------|
| Triple Store | Apache Jena Fuseki | 4.10.0 | Free, open-source, good OWL reasoning |
| Reasoning | OWL 2 DL | - | Full expressivity for complex ontologies |
| Query | SPARQL 1.1 | - | Standard query language |
| Python RDF | RDFlib | 7.0.0 | Mature Python library |
| Validation | SHACL | - | Data quality constraints |

**Hardware requirements:**
- RAM: 8 GB minimum
- Storage: 50 GB SSD
- CPU: 4 cores

#### Medium Scale (100,000 - 1,000,000 nodes)

| Component | Recommendation | Version | Rationale |
|-----------|---------------|---------|-----------|
| Triple Store | GraphDB | 10.5 | Commercial-grade performance |
| Reasoning | OWL 2 RL | - | Optimized for performance |
| Query | SPARQL 1.1 + GraphDB extensions | - | Advanced query features |
| Python RDF | RDFlib + Oxigraph | 7.0.0 | Performance optimization |
| Validation | SHACL + GraphDB constraints | - | Integrated validation |

**Hardware requirements:**
- RAM: 32 GB minimum
- Storage: 500 GB SSD
- CPU: 8 cores

#### Large Scale (> 1,000,000 nodes)

| Component | Recommendation | Version | Rationale |
|-----------|---------------|---------|-----------|
| Triple Store | Amazon Neptune | Latest | Cloud-native, auto-scaling |
| Alternative | Stardog | 9.x | Enterprise features |
| Reasoning | Rule-based (SHACL/Datalog) | - | Scalable reasoning |
| Query | SPARQL 1.1 + federation | - | Distributed queries |
| Graph Analytics | Neptune ML / Stardog BI | - | Integrated analytics |

**Hardware requirements:**
- Cloud deployment recommended
- RAM: 128 GB+ (auto-scaling)
- Storage: 2 TB+ SSD
- CPU: 16+ cores (auto-scaling)

### 2.2 Property Graph Component (Optional)

For use cases requiring high-performance graph traversal:

| Component | Recommendation | Version |
|-----------|---------------|---------|
| Graph Database | Neo4j | 5.x |
| Query Language | Cypher | - |
| Python Driver | neo4j-python-driver | 5.x |
| APOC Plugin | APOC | 5.x |

**Integration pattern:** Use Neo4j for graph analytics, synchronize key entities with RDF store via ETL pipeline.

---

## Part 3: Data Ingestion Pipeline

### 3.1 MGnify Integration

```python
# mgnify_ingestion.py
import requests
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

SKGI = Namespace("http://skgi.org/ontology/")

def fetch_mgnify_study(study_id):
    """Fetch study metadata from MGnify API"""
    url = f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{study_id}"
    response = requests.get(url, headers={"Accept": "application/json"})
    return response.json()

def transform_to_rdf(study_data):
    """Transform MGnify JSON to RDF triples"""
    g = Graph()
    g.bind("skgi", SKGI)
    
    study_uri = URIRef(f"http://skgi.org/study/{study_data['id']}")
    g.add((study_uri, RDF.type, SKGI.MicrobialSample))
    g.add((study_uri, SKGI.sampleId, Literal(study_data['id'])))
    g.add((study_uri, RDFS.label, Literal(study_data['attributes']['study-name'])))
    
    # Add biome information
    if 'biome' in study_data['attributes']:
        biome = study_data['attributes']['biome']
        g.add((study_uri, SKGI.collectedFromEnvironment, 
               URIRef(f"http://purl.obolibrary.org/obo/ENVO_{biome['lineage']}")))
    
    return g

def validate_against_schema(graph, shacl_graph):
    """Validate RDF graph against SHACL constraints"""
    from pyshacl import validate
    conforms, results_graph, results_text = validate(
        graph,
        shacl_graph=shacl_graph,
        inference='rdfs'
    )
    return conforms, results_text
```

### 3.2 CARD Integration

```python
# card_ingestion.py
def fetch_card_data():
    """Fetch AMR data from CARD database"""
    url = "https://card.mcmaster.ca/download/0/broadstreet-v3.2.6.tar.bz2"
    # Download and extract
    # Parse ARO (Antibiotic Resistance Ontology)
    pass

def transform_arg_to_rdf(arg_data):
    """Transform CARD ARG data to RDF"""
    g = Graph()
    g.bind("skgi", SKGI)
    
    arg_uri = URIRef(f"http://skgi.org/arg/{arg_data['aro_id']}")
    g.add((arg_uri, RDF.type, SKGI.ARG))
    g.add((arg_uri, RDFS.label, Literal(arg_data['gene_name'])))
    
    # Link to resistance compounds
    for drug in arg_data['resistance_to']:
        drug_uri = URIRef(f"http://purl.obolibrary.org/obo/CHEBI_{drug['chebi_id']}")
        g.add((arg_uri, SKGI.confersResistanceTo, drug_uri))
    
    return g
```

---

## Part 4: Benchmarking Protocol

### 4.1 Competency Queries

#### CQ1: Find microbes associated with a disease
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX mondo: <http://purl.obolibrary.org/obo/MONDO_>

SELECT ?microbe ?microbeName ?associationScore
WHERE {
  ?microbe skgi:associatedWith mondo:0005148 ;  # Type 2 diabetes
           skgi:associationScore ?associationScore ;
           rdfs:label ?microbeName .
}
ORDER BY DESC(?associationScore)
LIMIT 10
```

**Expected performance:** < 2 seconds for graphs with < 500K nodes

#### CQ2: Identify ARGs in a taxonomic clade
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX ncbitaxon: <http://purl.obolibrary.org/obo/NCBITaxon_>

SELECT ?taxon ?taxonName ?arg ?argName
WHERE {
  ?taxon skgi:carriesARG ?arg ;
         rdfs:label ?taxonName .
  ?arg rdfs:label ?argName .
  
  # Filter by taxonomic clade (e.g., Enterobacteriaceae)
  FILTER (strstarts(str(?taxon), str(ncbitaxon:543)))
}
```

**Expected performance:** < 5 seconds for graphs with < 1M nodes

#### CQ3: Find metabolic pathways in gut samples
```sparql
PREFIX skgi: <http://skgi.org/ontology/>
PREFIX go: <http://purl.obolibrary.org/obo/GO_>
PREFIX uberon: <http://purl.obolibrary.org/obo/UBERON_>

SELECT ?sample ?pathway ?pathwayName (COUNT(?taxon) AS ?taxonCount)
WHERE {
  ?sample skgi:collectedFromSite uberon:0001155 ;  # large intestine
          skgi:hasTaxonomicClassification ?taxon .
  ?taxon skgi:hasFunctionalAnnotation ?pathway .
  ?pathway rdfs:label ?pathwayName .
}
GROUP BY ?sample ?pathway ?pathwayName
ORDER BY DESC(?taxonCount)
```

**Expected performance:** < 10 seconds for graphs with < 1M nodes

### 4.2 Link Prediction Benchmark

#### Dataset: CARD Gene-Drug Associations
- **Source:** Comprehensive Antibiotic Resistance Database
- **Size:** ~3,000 gene-drug associations
- **Format:** Training/test split (80/20)

#### Evaluation Metrics
| Metric | Target | Description |
|--------|--------|-------------|
| MRR | > 0.30 | Mean Reciprocal Rank |
| Hits@1 | > 0.20 | Proportion of correct predictions at rank 1 |
| Hits@10 | > 0.50 | Proportion of correct predictions in top 10 |
| AUC-ROC | > 0.85 | Area under ROC curve |

#### Baseline Methods
1. **TransE:** Translational embeddings
2. **RotatE:** Rotational embeddings in complex space
3. **R-GCN:** Relational Graph Convolutional Networks
4. **ComplEx:** Complex embeddings

### 4.3 Entity Resolution Benchmark

#### Task: Taxonomic Identifier Alignment
- **Input:** Taxon names from different sources (NCBI, GTDB, SILVA)
- **Output:** Aligned identifiers with confidence scores

#### Evaluation Metrics
| Metric | Target | Description |
|--------|--------|-------------|
| Precision | > 0.90 | Proportion of correct alignments |
| Recall | > 0.80 | Proportion of alignments found |
| F1-score | > 0.85 | Harmonic mean of precision and recall |

### 4.4 Query Performance Benchmark

#### Test Suite
| Query ID | Description | Target Time |
|----------|-------------|-------------|
| CQ1 | Disease-microbe associations | < 2 sec |
| CQ2 | ARG identification | < 5 sec |
| CQ3 | Metabolic pathway analysis | < 10 sec |
| CQ4 | Multi-hop path queries | < 15 sec |
| CQ5 | Federated queries | < 30 sec |

---

## Part 5: SHACL Validation Rules

```turtle
# skgi_validation.shacl
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix skgi: <http://skgi.org/ontology/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

skgi:MicrobialSampleShape
    a sh:NodeShape ;
    sh:targetClass skgi:MicrobialSample ;
    sh:property [
        sh:path skgi:sampleId ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path skgi:hasTaxonomicClassification ;
        sh:class skgi:MicrobialTaxon ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path skgi:collectionDate ;
        sh:datatype xsd:date ;
        sh:maxCount 1 ;
    ] .

skgi:AssociationShape
    a sh:NodeShape ;
    sh:targetClass skgi:associatedWith ;
    sh:property [
        sh:path skgi:associationScore ;
        sh:datatype xsd:float ;
        sh:minInclusive 0.0 ;
        sh:maxInclusive 1.0 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path skgi:pValue ;
        sh:datatype xsd:float ;
        sh:minInclusive 0.0 ;
        sh:maxInclusive 1.0 ;
        sh:maxCount 1 ;
    ] .
```

---

## Part 6: Example Implementation

See `src/skgi/example_implementation.py` for a complete working example of:
- Loading ontologies
- Creating RDF graphs
- Validating against SHACL
- Querying with SPARQL
- Exporting to various formats

---

## References

1. Hogan, A., et al. (2022). Knowledge graphs. ACM Computing Surveys, 54(4), 1-37.
2. Ji, S., et al. (2022). A survey on knowledge graphs. IEEE Transactions on Neural Networks and Learning Systems, 33(2), 494-514.
3. Wilkinson, M. D., et al. (2016). The FAIR guiding principles. Scientific Data, 3, 160018.

---

**Document version:** 1.0  
**Last updated:** April 5, 2026  
**Maintainer:** Thabet Slimani (t.slimani@tu.edu.sa)
