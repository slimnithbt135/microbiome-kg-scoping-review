# Enhancement Proposal for Microbiome Knowledge Graph Scoping Review
## Target: ~60% Acceptance Probability through Addressing Core Reviewer Objections

---

## Executive Summary

This proposal outlines strategic enhancements to the current scoping review manuscript that directly address the most common objections raised by reviewers in high-impact bioinformatics journals such as Briefings in Bioinformatics. The current manuscript presents a valuable synthesis of 54 microbiome knowledge graph systems identified through a systematic PRISMA-ScR search across PubMed, IEEE Xplore, and bioRxiv. However, to elevate the work from its present state to a plausible acceptance threshold of approximately 60%, we must fundamentally strengthen three pillars: methodological reproducibility, classification framework validation, and the operational feasibility of the proposed Semantic Knowledge Graph Infrastructure (SKGI). The enhancements described below transform the manuscript from a descriptive mapping exercise into a rigorously documented, reproducible, and actionable contribution that meets contemporary standards for systematic reviews in computational biology.

---

## 1. Establishing Full Reproducibility: The Foundation of Scientific Rigor

The single most significant barrier to acceptance in its current form is the lack of comprehensive reproducibility documentation. While the manuscript states that the review followed PRISMA-ScR guidelines, reviewers will inevitably demand evidence that the entire workflow—from initial database queries to final study selection—can be independently verified and replicated. To address this critical gap, the manuscript must include a complete data and code availability statement that goes beyond generic assurances.

The full search strings for each database should be prominently displayed either in the main Methods section or in a clearly linked Supplementary Material document. For PubMed, this means providing the exact query executed on March 31, 2026, including all Boolean operators, field tags, and any filters applied. Similarly, the precise search syntax for IEEE Xplore and bioRxiv must be documented, as each platform employs distinct query languages and search field specifications. This transparency allows other researchers to verify the completeness of the literature capture and to extend the review with updated searches.

Beyond search strings, reproducibility requires the publication of the complete dataset of 769 records identified during the initial search phase. This dataset should include, at minimum: unique record identifiers, publication titles, author lists, publication years, journal or source names, Digital Object Identifiers (DOIs), and abstracts where available. The dataset should be deposited in a persistent, citable repository such as Zenodo or Figshare, with an associated DOI that can be referenced in the manuscript. This deposition serves multiple purposes: it demonstrates transparency, enables other researchers to verify the screening decisions, and provides a foundation for future updates or complementary reviews.

The Python scripts developed for deduplication and screening—already functional in the current workflow—must be cleaned, documented, and released under an open-source license in a public GitHub repository. This repository should include the complete source code for all three phases of the review: the initial deduplication and auto-screening script (`01_dedup_and_screen.py`), the full-text analysis and synthesis script (`02_fulltext_and_synthesis_CORRECTED.py`), and the PRISMA diagram generation utility (`prisma_diagram.py`). Each script should include comprehensive inline documentation, a README file explaining installation and execution procedures, and example input/output files to facilitate independent verification. The repository should also include a requirements.txt file listing all Python dependencies with version numbers, ensuring that the exact computational environment can be reconstructed.

A completed PRISMA-ScR checklist must accompany the manuscript submission. This checklist, available from the PRISMA statement website, should be filled out completely with section references indicating where each reporting item is addressed in the manuscript. The checklist serves as a quality assurance tool for both authors and reviewers, ensuring that no essential reporting elements are overlooked. Particular attention should be paid to items related to reproducibility, such as registration of the review protocol, funding sources, and declarations of interest.

---

## 2. Validating the Classification Framework: Addressing Single-Reviewer Limitations

A second major concern that reviewers will raise is the reliance on a single reviewer for study classification. The current framework categorizes the 54 included studies into six distinct system types—MDKG-type, KG-Microbe-type, MicrobiomeKG-type, BRIDGE-type, MINERVA-type, and AMR-GNN-type—based on automated keyword matching and manual review by one investigator. While this approach is efficient, it introduces potential bias and limits the generalizability of the classification scheme.

To strengthen the methodological rigor, an inter-rater reliability assessment should be conducted on a representative subset of the included studies. A second independent reviewer, ideally with expertise in both microbiology and knowledge engineering, should classify approximately 20-25% of the included studies (n=11-14) using the same six-category framework. The agreement between the two reviewers should be quantified using Cohen's kappa statistic, which accounts for chance agreement and provides a more robust measure of reliability than simple percent agreement. A kappa value above 0.6 would indicate substantial agreement and provide strong evidence for the validity of the classification framework. If the kappa falls below this threshold, the framework should be refined and the assessment repeated until acceptable agreement is achieved.

In cases where resources for a full second review are limited, an alternative approach is to conduct a focused validation on the most ambiguous or borderline cases. The 54 included studies include several with classification confidence scores of 2-4 (on a 10-point scale), indicating uncertainty in the automated categorization. These cases represent the most challenging classification decisions and would benefit most from independent verification. Documenting this validation process, including any disagreements and how they were resolved, adds transparency and demonstrates methodological sophistication.

The classification framework itself should be more explicitly operationalized in the manuscript. For each of the six categories, the manuscript should provide clear inclusion criteria that define what characteristics a study must exhibit to be assigned to that category. For example, the KG-Microbe-type category might be defined as "systems employing RDF/OWL representations with integration of multiple OBO Foundry ontologies, supporting SPARQL querying and logical reasoning." These operational definitions enable readers to understand the basis for classification decisions and to apply the framework to new studies as they emerge.

---

## 3. Transforming SKGI from Concept to Actionable Blueprint

The proposed Semantic Knowledge Graph Infrastructure (SKGI) represents one of the most innovative contributions of this review, yet in its current form it remains largely conceptual. Reviewers will rightly question whether SKGI is merely an aspirational vision or a genuinely implementable architecture. To address this concern, the manuscript must evolve the SKGI section from a high-level description to an actionable implementation blueprint.

A new subsection titled "SKGI Implementation Blueprint" should be added to the manuscript, providing concrete technical specifications for each of the four architectural layers. For the Data Harmonization layer, this means specifying the exact data formats, identifier schemes, and metadata standards that would be employed. Rather than simply stating that "multi-omic datasets from sources such as HMP, MGnify, EBI, and NCBI are standardized," the blueprint should identify specific data access endpoints, transformation procedures, and quality control checks. For example: "Microbiome sequencing data would be retrieved from the MGnify API (https://www.ebi.ac.uk/metagenomics/api/v1), converted from JSON to RDF using a custom Python transformation script, and validated against the MIxS standard using the GSC validator."

The Semantic Modeling layer should include a minimal core schema defining the essential entity types and relationships that any SKGI-compliant knowledge graph must implement. This schema should be expressed in a machine-readable format such as OWL or SHACL and made available in the GitHub repository. The core schema should include classes for MicrobialTaxon (linked to NCBI Taxonomy), HostOrganism (linked to NCBI Taxonomy and UBERON), MicrobialFunction (linked to Gene Ontology), ChemicalCompound (linked to ChEBI), Disease (linked to MONDO or DOID), and AntimicrobialResistance (linked to CARD). Relationships should include hasTaxonomicClassification, hasFunctionalAnnotation, interactsWith, causesDisease, and confersResistanceTo. This minimal schema provides a starting point for implementation while allowing for domain-specific extensions.

The Modular Knowledge Graph Construction layer should specify recommended technology stacks and integration patterns. Rather than presenting a generic statement about "RDF triple stores and reasoning engines," the blueprint should recommend specific technologies based on the analysis of existing systems in the review. For example: "For small-to-medium scale deployments (up to 500K nodes), we recommend Apache Jena Fuseki as the triple store, with OWL reasoning enabled. For larger deployments requiring distributed processing, we recommend Amazon Neptune or Ontotext GraphDB. Property graph components requiring high-performance traversal should use Neo4j with the APOC plugin."

The Graph-Based Intelligence layer should include concrete benchmarking protocols that define how SKGI implementations would be evaluated. This is perhaps the most critical enhancement, as it transforms SKGI from a proposal into a measurable standard. The benchmarking protocol should specify at least four evaluation dimensions: link prediction accuracy, entity resolution performance, query response time, and explainability metrics. For link prediction, the protocol should define a standard dataset (such as the AMR gene-drug associations from CARD) and evaluation metrics (mean reciprocal rank, hits@10). For entity resolution, the protocol should specify alignment tasks between different taxonomic identifiers or ontology terms and measure precision and recall. For query performance, the protocol should define a set of competency queries representing common use cases and measure execution time across different scales. For explainability, the protocol should specify user studies or automated metrics assessing the interpretability of predictions.

---

## 4. Strengthening Methods Reporting to PRISMA-ScR Standards

While the manuscript broadly follows PRISMA-ScR guidelines, several reporting elements require strengthening to meet current expectations. The search date should be prominently stated in the abstract as well as the Methods section—specifically, "The search was conducted on March 31, 2026"—to provide temporal context for the findings. This is particularly important in a rapidly evolving field where new systems are published frequently.

The inclusion and exclusion criteria should be operationalized with greater specificity. Rather than stating that studies were included if they "involved microbiome, microbiota, or microbial communities," the manuscript should define what constitutes sufficient microbiome involvement. For example: "Studies were considered microbiome-related if they analyzed microbial communities using sequencing-based approaches (16S rRNA, metagenomics, metatranscriptomics), culture-based characterization of multiple microbial species, or computational modeling of microbial interactions." Similarly, the knowledge graph criterion should be defined: "Studies were considered to employ knowledge graph approaches if they used RDF or OWL for data representation, property graph databases for relationship storage, ontology-based semantic modeling, or graph neural networks for predictive analytics."

The statement that "quality assessment was not performed as it is optional for scoping reviews" should be expanded to explain why this choice was appropriate for the specific research questions. A brief paragraph should note that scoping reviews aim to map the breadth of literature rather than synthesize evidence on effectiveness, and that quality assessment is therefore not required. However, the manuscript should also note that basic quality checks were applied—such as excluding non-peer-reviewed content except for preprints on bioRxiv—to ensure that the review focused on scientifically valid contributions.

A limitations paragraph should be added to the Methods section, acknowledging the constraints of the review methodology. This should include acknowledgment of the limited database coverage (only three sources, excluding Scopus and Web of Science), the reliance on English-language publications, and the potential for publication bias favoring positive results. Including these limitations in the Methods rather than only in the Discussion demonstrates transparency and methodological awareness.

---

## 5. Elevating Results from Narrative to Structured Evidence

The current Results section provides a narrative synthesis of the 54 included studies organized by the six classification categories. While this approach is appropriate for a scoping review, the manuscript would benefit from additional structured reporting that enables readers to extract quantitative insights more efficiently.

A supplementary table should be created that summarizes all 54 included studies with the following columns: first author and year, classification category, knowledge graph type (RDF/OWL, property graph, hybrid, GNN-based), ontologies used (from a controlled list), approximate scale (node count category: <5K, 5K-50K, 50K-150K, 150K-500K, >500K), primary analytics methods, FAIR compliance level (low, moderate, high), and availability status (open access, restricted, unavailable). This table would enable readers to identify studies matching their specific interests and to understand the distribution of approaches across the field.

The manuscript should include a quantitative analysis of trends across the included studies. This could include: the proportion of RDF-based versus property graph versus GNN-based systems; the frequency of ontology usage (e.g., 78% of studies use Gene Ontology, 45% use NCBI Taxonomy); the temporal trend in publication volume (e.g., 60% of included studies were published in 2022 or later); and the distribution of application domains (e.g., 35% focus on human health, 25% on antimicrobial resistance, 20% on environmental microbiomes). These quantitative insights transform the Results section from a descriptive catalog into an analytical synthesis that identifies patterns and trends.

The PRISMA-ScR flow diagram should be refined to include more granular information about the screening process. The current diagram correctly shows the identification, deduplication, screening, and inclusion stages, but could be enhanced by adding information about the full-text assessment stage. Specifically, the diagram should indicate how many studies passed title/abstract screening but were excluded at full-text review, and the reasons for these exclusions. This additional detail provides a more complete picture of the selection process and addresses PRISMA-ScR reporting requirements more fully.

---

## 6. Ensuring Citation Integrity and Resource Attribution

A final but critical enhancement involves ensuring that every named resource in the manuscript has a corresponding citation. The current manuscript mentions several major microbiome and biomedical resources—Earth Microbiome Project, MGnify, Human Microbiome Project (HMP) and Integrative Human Microbiome Project (iHMP), Comprehensive Antibiotic Resistance Database (CARD), DrugBank—without always providing citations. Reviewers will flag these omissions as they prevent readers from accessing the original sources and verifying the claims made about these resources.

Each of these resources should be accompanied by a primary citation: Thompson et al. (2017) for the Earth Microbiome Project; Mitchell et al. (2020) for MGnify; Integrative HMP Research Network Consortium (2019) for iHMP; Alcock et al. (2020) for CARD; and Wishart et al. (2018) for DrugBank. These citations should be integrated into the text at first mention and included in the reference list with complete bibliographic information.

A related concern involves the system names used in Table 1 and throughout the manuscript. Several systems are referred to with names that appear to be invented for this review—"MicrobiomeKG (2026)," "KG-Microbe (2025)," "AMR-BRIDGE (2024)"—rather than the actual names used in the original publications. This practice, while intended to create a consistent typology, may confuse readers and will certainly be flagged by reviewers. The manuscript should either: (a) use the actual system names from the publications and add a footnote explaining the category assignment, or (b) clearly label these as "representative archetypes" that synthesize characteristics from multiple systems rather than referring to specific implementations. If option (b) is chosen, the manuscript should explicitly state that these are conceptual categories developed for analytical purposes and not actual system names.

---

## Implementation Roadmap and Priority Matrix

Implementing these enhancements requires approximately 3-4 weeks of focused effort. The highest priority items—those that will have the greatest impact on acceptance probability—are: (1) publishing the complete search strings and reproducibility package; (2) conducting the inter-rater reliability assessment; and (3) transforming SKGI into an actionable blueprint with concrete specifications. These three enhancements address the most common and serious reviewer objections and should be completed first.

Medium priority items include: strengthening the Methods reporting with operationalized criteria and limitations; creating the supplementary table of all 54 studies; and adding quantitative trend analyses. These enhancements improve the manuscript's rigor and value but are less likely to be rejection triggers if omitted.

Lower priority but still valuable items include: ensuring complete citation coverage for all named resources; refining the PRISMA flow diagram; and polishing the writing for clarity and concision. These final touches contribute to the overall professionalism of the manuscript and should be completed before submission.

---

## Conclusion

The current scoping review manuscript represents a valuable contribution to the microbiome knowledge graph literature, synthesizing 54 studies across multiple domains and proposing an innovative infrastructure framework. However, to achieve a plausible acceptance probability of approximately 60% in a competitive journal such as Briefings in Bioinformatics, the manuscript must address fundamental concerns about reproducibility, classification validity, and implementation feasibility. The enhancements outlined in this proposal directly target these concerns, transforming the manuscript from a descriptive review into a rigorously documented, reproducible, and actionable contribution. By implementing these changes, the authors demonstrate not only the breadth of their literature synthesis but also their commitment to the highest standards of methodological transparency and scientific rigor.

---

*Document prepared for enhancement of scoping review manuscript targeting Briefings in Bioinformatics*
