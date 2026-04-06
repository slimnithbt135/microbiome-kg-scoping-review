#!/usr/bin/env python3
"""
================================================================================
SKGI EXAMPLE IMPLEMENTATION
================================================================================

This script demonstrates how to use the Semantic Knowledge Graph Infrastructure
(SKGI) for microbiome data integration and analysis.

Usage:
    python example_implementation.py

Requirements:
    - rdflib >= 7.0.0
    - pyshacl >= 0.25.0
    - requests >= 2.31.0

Author: Thabet Slimani
License: MIT
================================================================================
"""

import json
from pathlib import Path
from datetime import datetime

import requests
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, OWL
from pyshacl import validate

#================================================================================
# SKGI Namespaces
#================================================================================

SKGI = Namespace("http://skgi.org/ontology/")
NCBITAXON = Namespace("http://purl.obolibrary.org/obo/NCBITaxon_")
GO = Namespace("http://purl.obolibrary.org/obo/GO_")
CHEBI = Namespace("http://purl.obolibrary.org/obo/CHEBI_")
MONDO = Namespace("http://purl.obolibrary.org/obo/MONDO_")
CARD = Namespace("https://card.mcmaster.ca/aro/")
#================================================================================
# Core Schema Definition
#================================================================================

SKGI_CORE_TRIPLES = """
@prefix skgi: <http://skgi.org/ontology/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Core Classes
skgi:MicrobialSample a owl:Class ;
    rdfs:label "Microbial Sample" ;
    rdfs:comment "A biological sample containing microbial communities" .

skgi:MicrobialTaxon a owl:Class ;
    rdfs:label "Microbial Taxon" ;
    rdfs:comment "A taxonomic classification of a microorganism" .

skgi:HostOrganism a owl:Class ;
    rdfs:label "Host Organism" ;
    rdfs:comment "An organism that harbors a microbial community" .

skgi:MicrobialFunction a owl:Class ;
    rdfs:label "Microbial Function" ;
    rdfs:comment "A biological function performed by microorganisms" .

skgi:ChemicalCompound a owl:Class ;
    rdfs:label "Chemical Compound" ;
    rdfs:comment "A chemical substance of biological relevance" .

skgi:Disease a owl:Class ;
    rdfs:label "Disease" ;
    rdfs:comment "A disease or pathological condition" .

skgi:ARG a owl:Class ;
    rdfs:label "Antimicrobial Resistance Gene" ;
    rdfs:comment "A gene conferring antimicrobial resistance" .

# Object Properties
skgi:hasTaxonomicClassification a owl:ObjectProperty ;
    rdfs:label "has taxonomic classification" ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:MicrobialTaxon .

skgi:hasFunctionalAnnotation a owl:ObjectProperty ;
    rdfs:label "has functional annotation" ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:MicrobialFunction .

skgi:collectedFromHost a owl:ObjectProperty ;
    rdfs:label "collected from host" ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range skgi:HostOrganism .

skgi:associatedWith a owl:ObjectProperty ;
    rdfs:label "associated with" ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:Disease .

skgi:confersResistanceTo a owl:ObjectProperty ;
    rdfs:label "confers resistance to" ;
    rdfs:domain skgi:ARG ;
    rdfs:range skgi:ChemicalCompound .

skgi:carriesARG a owl:ObjectProperty ;
    rdfs:label "carries ARG" ;
    rdfs:domain skgi:MicrobialTaxon ;
    rdfs:range skgi:ARG .

# Data Properties
skgi:sampleId a owl:DatatypeProperty ;
    rdfs:label "sample identifier" ;
    rdfs:domain skgi:MicrobialSample ;
    rdfs:range xsd:string .

skgi:abundance a owl:DatatypeProperty ;
    rdfs:label "relative abundance" ;
    rdfs:range xsd:float .

skgi:associationScore a owl:DatatypeProperty ;
    rdfs:label "association score" ;
    rdfs:range xsd:float .

skgi:pValue a owl:DatatypeProperty ;
    rdfs:label "p-value" ;
    rdfs:range xsd:float .
"""
#================================================================================
# SKGI Knowledge Graph Class
#================================================================================

class MicrobiomeKG:
    """
    Semantic Knowledge Graph for Microbiome Data
    
    This class provides methods for creating, validating, and querying
    microbiome knowledge graphs following the SKGI specification.
    
    Example:
        >>> kg = MicrobiomeKG()
        >>> kg.load_core_schema()
        >>> kg.add_sample("S001", taxa=["562", "1613"])
        >>> kg.validate()
        >>> results = kg.query("SELECT * WHERE { ?s ?p ?o }")
    """
    
    def __init__(self):
        """Initialize an empty knowledge graph."""
        self.graph = Graph()
        self._bind_namespaces()
        self.validation_report = None
        
    def _bind_namespaces(self):
        """Bind all SKGI namespaces to the graph."""
        self.graph.bind("skgi", SKGI)
        self.graph.bind("ncbitaxon", NCBITAXON)
        self.graph.bind("go", GO)
        self.graph.bind("chebi", CHEBI)
        self.graph.bind("mondo", MONDO)
        self.graph.bind("card", CARD)
        
    def load_core_schema(self):
        """Load the SKGI core schema into the graph."""
        self.graph.bind("xsd", XSD)   
        self.graph.parse(data=SKGI_CORE_TRIPLES, format="turtle")
        print("✓ Core schema loaded")
        
    def load_shacl_rules(self, shacl_file: Path):
        """Load SHACL validation rules from file."""
        with open(shacl_file, 'r') as f:
            shacl_graph = Graph()
            shacl_graph.parse(data=f.read(), format="turtle")
        return shacl_graph
        
    def add_sample(self, sample_id: str, taxa: list, 
                   host_id: str = None, body_site: str = None,
                   collection_date: str = None):
        """
        Add a microbial sample to the knowledge graph.
        
        Args:
            sample_id: Unique identifier for the sample
            taxa: List of NCBI taxonomy IDs present in the sample
            host_id: Optional NCBI taxonomy ID of the host
            body_site: Optional anatomical site (UBERON ID)
            collection_date: Optional collection date (YYYY-MM-DD)
        """
        sample_uri = URIRef(f"http://skgi.org/sample/{sample_id}")
        
        # Add sample type
        self.graph.add((sample_uri, RDF.type, SKGI.MicrobialSample))
        self.graph.add((sample_uri, SKGI.sampleId, Literal(sample_id)))
        
        # Add taxonomic classifications
        for taxon_id in taxa:
            taxon_uri = NCBITAXON[taxon_id]
            self.graph.add((sample_uri, SKGI.hasTaxonomicClassification, taxon_uri))
            self.graph.add((taxon_uri, RDF.type, SKGI.MicrobialTaxon))
            
        # Add host if provided
        if host_id:
            host_uri = NCBITAXON[host_id]
            self.graph.add((sample_uri, SKGI.collectedFromHost, host_uri))
            self.graph.add((host_uri, RDF.type, SKGI.HostOrganism))
            
        # Add collection date if provided
        if collection_date:
            self.graph.add((sample_uri, SKGI.collectionDate, 
                          Literal(collection_date, datatype=XSD.date)))
                          
        print(f"✓ Added sample {sample_id} with {len(taxa)} taxa")
        
    def add_taxon_function(self, taxon_id: str, go_terms: list):
        """
        Add functional annotations to a taxon.
        
        Args:
            taxon_id: NCBI taxonomy ID
            go_terms: List of Gene Ontology IDs
        """
        taxon_uri = NCBITAXON[taxon_id]
        
        for go_id in go_terms:
            go_uri = GO[go_id]
            self.graph.add((taxon_uri, SKGI.hasFunctionalAnnotation, go_uri))
            self.graph.add((go_uri, RDF.type, SKGI.MicrobialFunction))
            
        print(f"✓ Added {len(go_terms)} functions to taxon {taxon_id}")
        
    def add_disease_association(self, taxon_id: str, disease_id: str,
                                 score: float = None, p_value: float = None):
        """
        Add a disease association for a taxon.
        
        Args:
            taxon_id: NCBI taxonomy ID
            disease_id: MONDO disease ID
            score: Optional association score (0-1)
            p_value: Optional p-value (0-1)
        """
        taxon_uri = NCBITAXON[taxon_id]
        disease_uri = MONDO[disease_id]
        
        # Create association as reified statement
        association = BNode()
        self.graph.add((association, RDF.type, RDF.Statement))
        self.graph.add((association, RDF.subject, taxon_uri))
        self.graph.add((association, RDF.predicate, SKGI.associatedWith))
        self.graph.add((association, RDF.object, disease_uri))
        
        if score is not None:
            self.graph.add((association, SKGI.associationScore, Literal(score)))
        if p_value is not None:
            self.graph.add((association, SKGI.pValue, Literal(p_value)))
            
        print(f"✓ Added disease association: taxon {taxon_id} → disease {disease_id}")
        
    def add_arg(self, aro_id: str, gene_name: str, 
                resistant_to: list = None):
        """
        Add an antimicrobial resistance gene.
        
        Args:
            aro_id: CARD ARO ID (format: ARO:XXXXX)
            gene_name: Gene name
            resistant_to: List of ChEBI IDs for compounds
        """
        arg_uri = CARD[aro_id]
        
        self.graph.add((arg_uri, RDF.type, SKGI.ARG))
        self.graph.add((arg_uri, RDFS.label, Literal(gene_name)))
        
        if resistant_to:
            for chebi_id in resistant_to:
                compound_uri = CHEBI[chebi_id]
                self.graph.add((arg_uri, SKGI.confersResistanceTo, compound_uri))
                self.graph.add((compound_uri, RDF.type, SKGI.ChemicalCompound))
                
        print(f"✓ Added ARG {gene_name} ({aro_id})")
        
    def validate(self, shacl_graph: Graph = None) -> tuple:
        """
        Validate the knowledge graph against SHACL rules.
        
        Args:
            shacl_graph: Optional pre-loaded SHACL graph
            
        Returns:
            Tuple of (conforms: bool, report_text: str)
        """
        if shacl_graph is None:
            # Try to load from default location
            shacl_path = Path(__file__).parent / "core_schema.shacl"
            if shacl_path.exists():
                shacl_graph = self.load_shacl_rules(shacl_path)
            else:
                print("⚠ No SHACL rules found, skipping validation")
                return True, "No validation performed"
                
        conforms, results_graph, results_text = validate(
            self.graph,
            shacl_graph=shacl_graph,
            inference='rdfs'
        )
        
        self.validation_report = results_text
        
        if conforms:
            print("✓ Validation passed")
        else:
            print(f"✗ Validation failed with {len(results_text.split(chr(10)))} issues")
            
        return conforms, results_text
        
    def query(self, sparql_query: str):
        """
        Execute a SPARQL query against the knowledge graph.
        
        Args:
            sparql_query: SPARQL query string
            
        Returns:
            Query results
        """
        return self.graph.query(sparql_query)
        
    def export(self, output_path: Path, format: str = "turtle"):
        """
        Export the knowledge graph to a file.
        
        Args:
            output_path: Path to output file
            format: RDF format (turtle, xml, json-ld, etc.)
        """
        self.graph.serialize(destination=str(output_path), format=format)
        print(f"✓ Exported graph to {output_path}")
        
    def get_statistics(self) -> dict:
        """Get basic statistics about the knowledge graph."""
        stats = {
            "total_triples": len(self.graph),
            "samples": len(list(self.graph.subjects(RDF.type, SKGI.MicrobialSample))),
            "taxa": len(list(self.graph.subjects(RDF.type, SKGI.MicrobialTaxon))),
            "hosts": len(list(self.graph.subjects(RDF.type, SKGI.HostOrganism))),
            "args": len(list(self.graph.subjects(RDF.type, SKGI.ARG))),
        }
        return stats

#================================================================================
# Data Ingestion Functions
#================================================================================

def fetch_mgnify_study(study_id: str) -> dict:
    """
    Fetch study metadata from MGnify API.
    
    Args:
        study_id: MGnify study accession (e.g., "MGYS00001234")
        
    Returns:
        Dictionary with study metadata
    """
    url = f"https://www.ebi.ac.uk/metagenomics/api/v1/studies/{study_id}"
    
    try:
        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching MGnify study: {e}")
        return None
        
def transform_mgnify_to_skgi(study_data: dict) -> Graph:
    """
    Transform MGnify API response to SKGI RDF graph.
    
    Args:
        study_data: Dictionary from MGnify API
        
    Returns:
        RDFlib Graph with SKGI triples
    """
    g = Graph()
    g.bind("skgi", SKGI)
    
    study_id = study_data['id']
    study_uri = URIRef(f"http://skgi.org/study/{study_id}")
    
    # Add study as sample
    g.add((study_uri, RDF.type, SKGI.MicrobialSample))
    g.add((study_uri, SKGI.sampleId, Literal(study_id)))
    
    # Add biome information
    if 'biome' in study_data.get('attributes', {}):
        biome = study_data['attributes']['biome']
        g.add((study_uri, RDFS.label, Literal(biome.get('lineage', 'Unknown'))))
        
    # Add provenance
    g.add((study_uri, SKGI.dataSource, Literal("MGnify")))
    g.add((study_uri, SKGI.accessDate, Literal(datetime.now().isoformat())))
    
    return g

#================================================================================
# Benchmarking Functions
#================================================================================

def benchmark_query_performance(kg: MicrobiomeKG, query_file: Path) -> dict:
    """
    Benchmark SPARQL query performance.
    
    Args:
        kg: MicrobiomeKG instance
        query_file: Path to file containing competency queries
        
    Returns:
        Dictionary with timing results
    """
    import time
    
    results = {}
    
    with open(query_file, 'r') as f:
        queries = f.read().split("\n\n")
        
    for i, query in enumerate(queries, 1):
        if query.strip():
            start = time.time()
            kg.query(query)
            elapsed = time.time() - start
            results[f"CQ{i}"] = elapsed
            
    return results

#================================================================================
# Example Usage
#================================================================================

def main():
    """
    Demonstrate SKGI functionality with example data.
    """
    print("=" * 70)
    print("SKGI EXAMPLE IMPLEMENTATION")
    print("=" * 70)
    
    # Create a new knowledge graph
    kg = MicrobiomeKG()
    
    # Load core schema
    print("\n1. Loading core schema...")
    kg.load_core_schema()
    
    # Add sample data
    print("\n2. Adding sample data...")
    
    # Add a gut microbiome sample from human
    kg.add_sample(
        sample_id="S001",
        taxa=["562", "1613", "816"],  # E. coli, B. bifidum, B.acteroides
        host_id="9606",  # Homo sapiens
        body_site="UBERON:0001155",  # large intestine
        collection_date="2026-01-15"
    )
    
    # Add functional annotations
    print("\n3. Adding functional annotations...")
    kg.add_taxon_function("562", ["0008152", "0005975"])  # metabolic process, carbohydrate metabolism
    
    # Add disease association
    print("\n4. Adding disease association...")
    kg.add_disease_association(
        taxon_id="562",
        disease_id="0005148",  # type 2 diabetes
        score=0.75,
        p_value=0.001
    )
    
    # Add ARG
    print("\n5. Adding antimicrobial resistance gene...")
    kg.add_arg(
        aro_id="ARO:3002532",  # blaCTX-M-15
        gene_name="blaCTX-M-15",
        resistant_to=["28971", "28001"]  # ceftriaxone, cefotaxime
    )
    
    # Get statistics
    print("\n6. Knowledge graph statistics:")
    stats = kg.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
        
    # Example SPARQL query
    print("\n7. Running example query...")
    query = """
    PREFIX skgi: <http://skgi.org/ontology/>
    SELECT ?sample ?taxon
    WHERE {
        ?sample a skgi:MicrobialSample ;
                skgi:hasTaxonomicClassification ?taxon .
    }
    """
    results = kg.query(query)
    for row in results:
        print(f"   Sample: {row.sample}, Taxon: {row.taxon}")
        
    # Export to file
    print("\n8. Exporting knowledge graph...")
    output_path = Path("example_kg.ttl")
    kg.export(output_path)
    
    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print(f"Output saved to: {output_path.absolute()}")
    print("=" * 70)

if __name__ == "__main__":
    main()
