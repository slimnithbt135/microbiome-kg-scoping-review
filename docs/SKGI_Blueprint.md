# SKGI Implementation Blueprint
## Semantic Knowledge Graph Infrastructure for Microbiome Intelligence

IMPORTANT: This document provides recommended specifications and illustrative examples based on community best practices and vendor documentation. Software versions, hardware requirements, and code examples should be verified against current releases and tested before production deployment.

---

## Part 1: Core Schema Specification

### 1.1 Namespace Declarations

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

### 1.2 Core Classes

Microbial Taxon:
skgi:MicrobialTaxon
    a owl:Class ;
    rdfs:label "Microbial Taxon"@en ;
    rdfs:comment "A taxonomic classification of a microorganism according to NCBI Taxonomy"@en ;
    owl:equivalentClass ncbitaxon:Organism ;
    skos:definition "Any organism classified in the NCBI Taxonomy database" .

Microbial Sample:
skgi:MicrobialSample
    a owl:Class ;
    rdfs:label "Microbial Sample"@en ;
    rdfs:comment "A biological sample containing microbial communities"@en ;
    skos:definition "A collected specimen containing microorganisms for analysis" .

Host Organism:
skgi:HostOrganism
    a owl:Class ;
    rdfs:label "Host Organism"@en ;
    rdfs:comment "An organism that harbors a microbial community"@en ;
    owl:equivalentClass ncbitaxon:Organism .

Microbial Function:
skgi:MicrobialFunction
    a owl:Class ;
    rdfs:label "Microbial Function"@en ;
    rdfs:comment "A biological function or process performed by microorganisms"@en ;
    owl:equivalentClass go:GO_0008150 .

Chemical Compound:
skgi:ChemicalCompound
    a owl:Class ;
    rdfs:label "Chemical Compound"@en ;
    rdfs:comment "A chemical substance of biological relevance"@en ;
    owl:equivalentClass chebi:CHEBI_24431 .

Disease:
skgi:Disease
    a owl:Class ;
    rdfs:label "Disease"@en ;
    rdfs:comment "A disease or pathological condition"@en ;
    owl:equivalentClass mondo:MONDO_0000001 .

Antimicrobial Resistance Gene:
skgi:ARG
    a owl:Class ;
    rdfs:label "Antimicrobial Resistance Gene"@en ;
    rdfs:comment "A gene conferring resistance to antimicrobial agents"@en ;
    skos:definition "A gene that reduces the effectiveness of antimicrobial drugs" .

Environment:
skgi:Environment
    a owl:Class ;
    rdfs:label "Environment"@en ;
    rdfs:comment "An environmental context or habitat"@en ;
    owl:equivalentClass envo:ENVO_01000254 .

### 1.3 Object Properties (Relationships)

Taxonomic classification:
skgi:hasTaxonomicClassification
    a owl:ObjectProperty ;
    rdfs:label "has taxonomic classification"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:MicrobialTaxon ;
    skos:definition "Links a sample to its constituent microbial taxa" .

Functional annotation:
skgi:hasFunctionalAnnotation
    a owl:ObjectProperty ;
    rdfs:label "has functional annotation"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:MicrobialFunction ;
    skos:definition "Links a microbe to its functional capabilities" .

Host association:
skgi:collectedFromHost
    a owl:ObjectProperty ;
    rdfs:label "collected from host"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:HostOrganism ;
    skos:definition "Indicates the host organism from which a sample was collected" .

Host body site:
skgi:collectedFromSite
    a owl:ObjectProperty ;
    rdfs:label "collected from site"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range uberon:UBERON_0001062 ;
    skos:definition "Indicates the anatomical site from which a sample was collected" .

Disease association:
skgi:associatedWith
    a owl:ObjectProperty ;
    rdfs:label "associated with"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:Disease ;
    skos:definition "Indicates an association between a microbe and a disease" .

Chemical interaction:
skgi:produces
    a owl:ObjectProperty ;
    rdfs:label "produces"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:ChemicalCompound ;
    skos:definition "Indicates that a microbe produces a chemical compound" .

AMR relationship - confers resistance:
skgi:confersResistanceTo
    a owl:ObjectProperty ;
    rdfs:label "confers resistance to"@en ;
    rdfs:domain skgi:ARG ;
    rdfs:range skgi:ChemicalCompound ;
    skos:definition "Indicates that an ARG confers resistance to an antimicrobial compound" .

AMR relationship - carries ARG:
skgi:carriesARG
    a owl:ObjectProperty ;
    rdfs:label "carries ARG"@en ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:ARG ;
    skos:definition "Indicates that a microbe carries an antimicrobial resistance gene" .

Environmental context:
skgi:collectedFromEnvironment
    a owl:ObjectProperty ;
    rdfs:label "collected from environment"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:Environment ;
    skos:definition "Indicates the environmental context of a sample" .

Provenance:
skgi:derivedFrom
    a owl:ObjectProperty ;
    rdfs:label "derived from"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range prov:Entity ;
    skos:definition "Links a sample to its source data or study" .

### 1.4 Data Properties

Sample identifier:
skgi:sampleId
    a owl:DatatypeProperty ;
    rdfs:label "sample identifier"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range xsd:string .

Collection date:
skgi:collectionDate
    a owl:DatatypeProperty ;
    rdfs:label "collection date"@en ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range xsd:date .

Abundance:
skgi:abundance
    a owl:DatatypeProperty ;
    rdfs:label "abundance"@en ;
    rdfs:domain skgi:hasTaxonomicClassification ;
    rdfs:range xsd:float ;
    skos:definition "Relative abundance of a taxon in a sample (0.0 to 1.0)" .

Association score:
skgi:associationScore
    a owl:DatatypeProperty ;
    rdfs:label "association score"@en ;
    rdfs:domain skgi:associatedWith ;
    rdfs:range xsd:float ;
    skos:definition "Statistical score indicating strength of association" .

P-value:
skgi:pValue
    a owl:DatatypeProperty ;
    rdfs:label "p-value"@en ;
    rdfs:domain skgi:associatedWith ;
    rdfs:range xsd:float .

Data source:
skgi:dataSource
    a owl:DatatypeProperty ;
    rdfs:label "data source"@en ;
    rdfs:domain prov:Entity ;
    rdfs:range xsd:string ;
    skos:definition "Original database or repository of the data" .

Access date:
skgi:accessDate
    a owl:DatatypeProperty ;
    rdfs:label "access date"@en ;
    rdfs:domain prov:Entity ;
    rdfs:range xsd:dateTime .

---

## Part 2: Technology Stack Recommendations

Note: Recommendations based on community best practices and vendor documentation. Verify current versions and test before production deployment.

### 2.1 By Scale

Small Scale (< 100,000 nodes):

| Component | Recommendation | Version* | Rationale |
|-----------|---------------|----------|-----------|
| Triple Store | Apache Jena Fuseki | 4.x | Free, open-source, good OWL reasoning |
| Reasoning | OWL 2 DL | - | Full expressivity for complex ontologies |
| Query | SPARQL 1.1 | - | Standard query language |
| Python RDF | RDFlib | 7.x | Mature Python library |
| Validation | SHACL | - | Data quality constraints |

Estimated Hardware Requirements:
- RAM: 8 GB minimum
- Storage: 50 GB SSD
- CPU: 4 cores

*Verify current versions at implementation time.

Medium Scale (100,000 - 1,000,000 nodes):

| Component | Recommendation | Version* | Rationale |
|-----------|---------------|----------|-----------|
| Triple Store | GraphDB | 10.x | Commercial-grade performance |
| Reasoning | OWL 2 RL | - | Optimized for performance |
| Query | SPARQL 1.1 + GraphDB extensions | - | Advanced query features |
| Python RDF | RDFlib + Oxigraph | 7.x | Performance optimization |
| Validation | SHACL + GraphDB constraints | - | Integrated validation |

Estimated Hardware Requirements:
- RAM: 32 GB minimum
- Storage: 500 GB SSD
- CPU: 8 cores

*Verify current versions at implementation time.

Large Scale (> 1,000,000 nodes):

| Component | Recommendation | Version* | Rationale |
|-----------|---------------|----------|-----------|
| Triple Store | Amazon Neptune | Latest | Cloud-native, auto-scaling |
| Alternative | Stardog | 9.x | Enterprise features |
| Reasoning | Rule-based (SHACL/Datalog) | - | Scalable reasoning |
| Query | SPARQL 1.1 + federation | - | Distributed queries |
| Graph Analytics | Neptune ML / Stardog BI | - | Integrated analytics |

Estimated Hardware Requirements:
- Cloud deployment recommended
- RAM: 128 GB+ (auto-scaling)
- Storage: 2 TB+ SSD
- CPU: 16+ cores (auto-scaling)

*Verify current versions at implementation time.

### 2.2 Property Graph Component (Optional)

For use cases requiring high-performance graph traversal:

| Component | Recommendation | Version* |
|-----------|---------------|----------|
| Graph Database | Neo4j | 5.x |
| Query Language | Cypher | - |
| Python Driver | neo4j-python-driver | 5.x |
| APOC Plugin | APOC | 5.x |

Integration pattern: Use Neo4j for graph analytics, synchronize key entities with RDF store via ETL pipeline.

*Verify current versions at implementation time.

---

## Part 3: Data Ingestion Pipeline

Note: Code examples are illustrative. Test and adapt for production use.

### 3.1 MGnify Integration

mgnify_ingestion.py - EXAMPLE CODE, NOT TESTED:
import requests
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

SKGI = Namespace("http://skgi.org/ontology/")

def fetch_mgnify_study(study_id):
    """Example function - NOT TESTED"""
    url = f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{study_id}"
    response = requests.get(url, headers={"Accept": "application/json"})
    return response.json()

def transform_to_rdf(study_data):
    """Example function - NOT TESTED"""
    g = Graph()
    g.bind("skgi", SKGI)
    study_uri = URIRef(f"http://skgi.org/study/{study_data['id']}")
    g.add((study_uri, RDF.type, SKGI.MicrobialSample))
    g.add((study_uri, SKGI.sampleId, Literal(study_data['id'])))
    g.add((study_uri, RDFS.label, Literal(study_data['attributes']['study-name'])))
    if 'biome' in study_data['attributes']:
        biome = study_data['attributes']['biome']
        g.add((study_uri, SKGI.collectedFromEnvironment, 
               URIRef(f"http://purl.obolibrary.org/obo/ENVO_{biome['lineage']}")))
    return g

def validate_against_schema(graph, shacl_graph):
    """Example function - NOT TESTED"""
    from pyshacl import validate
    conforms, results_graph, results_text = validate(
        graph,
        shacl_graph=shacl_graph,
        inference='rdfs'
    )
    return conforms, results_text

### 3.2 CARD Integration

card_ingestion.py - EXAMPLE CODE, NOT TESTED:
def fetch_card_data():
    """Example function - NOT TESTED"""
    url = "https://card.mcmaster.ca/download/0/broadstreet-v3.2.6.tar.bz2"
    # Download and extract
    # Parse ARO (Antibiotic Resistance Ontology)
    pass

def transform_arg_to_rdf(arg_data):
    """Example function - NOT TESTED"""
    g = Graph()
    g.bind("skgi", SKGI)
    arg_uri = URIRef(f"http://skgi.org/arg/{arg_data['aro_id']}")
    g.add((arg_uri, RDF.type, SKGI.ARG))
    g.add((arg_uri, RDFS.label, Literal(arg_data['gene_name'])))
    for drug in arg_data['resistance_to']:
        drug_uri = URIRef(f"http://purl.obolibrary.org/obo/CHEBI_{drug['chebi_id']}")
        g.add((arg_uri, SKGI.confersResistanceTo, drug_uri))
    return g

---

## Part 4: Benchmarking Protocol

Note: See BENCHMARK_PROTOCOL.md for detailed proposed benchmarks. All metrics are aspirational targets, not validated results.

4.1 Competency Queries (Proposed): See BENCHMARK_PROTOCOL.md Section 2
4.2 Link Prediction Benchmark (Proposed): See BENCHMARK_PROTOCOL.md Section 3
4.3 Entity Resolution Benchmark (Proposed): See BENCHMARK_PROTOCOL.md Section 4
4.4 Query Performance Benchmark (Proposed): See BENCHMARK_PROTOCOL.md Section 5

---

## Part 5: SHACL Validation Rules

skgi_validation.shacl - EXAMPLE, NOT TESTED:
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

---

## Part 6: Example Implementation

See src/skgi/example_implementation.py for illustrative code (not tested in production).

---

## References

1. Hogan, A., et al. (2022). Knowledge graphs. ACM Computing Surveys, 54(4), 1-37.
2. Ji, S., et al. (2022). A survey on knowledge graphs. IEEE Transactions on Neural Networks and Learning Systems, 33(2), 494-514.
3. Wilkinson, M. D., et al. (2016). The FAIR guiding principles. Scientific Data, 3, 160018.

---

Document version: 1.0
Last updated: April 9, 2026
Status: RECOMMENDED SPECIFICATIONS - Verify before implementation
Maintainer: [Thabet Slimani - t.slimani@tu.edu.sa]
