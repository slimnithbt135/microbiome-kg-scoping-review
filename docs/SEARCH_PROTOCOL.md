# Search Protocol

## Scoping Review: Microbiome Knowledge Graph Systems

Search Date: March 31, 2026
Review Type: PRISMA-ScR (Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews)

---

## 1. Research Question

What is the current landscape of knowledge graph applications in microbiome research, and what are the key characteristics, technologies, and gaps in existing systems?



## 2. Search Strategy

### 2.1 Databases Searched

| Database | Platform | Records Retrieved |
|----------|----------|-------------------|
| PubMed | NCBI | 725 |
| IEEE Xplore | IEEE | 10 |
| bioRxiv | Crossref API | 34 |
| Total | | 769 |

### 2.2 Search Strings

PubMed (via NCBI E-utilities)
URL: https://pubmed.ncbi.nlm.nih.gov/
```
Search String:
((microbiome[Title/Abstract] OR microbiota[Title/Abstract] OR microbial[Title/Abstract] OR "gut bacteria"[Title/Abstract] OR "bacterial community"[Title/Abstract]) AND ("knowledge graph"[Title/Abstract] OR "semantic web"[Title/Abstract] OR "linked data"[Title/Abstract] OR ontology[Title/Abstract] OR RDF[Title/Abstract] OR "graph database"[Title/Abstract]))
```
Search Parameters:
- Search fields: Title/Abstract [Title/Abstract]
- Boolean operators: AND, OR
- Date restrictions: None
- Language restrictions: None
- Publication type filters: None

IEEE Xplore
URL: https://ieeexplore.ieee.org/

Search String:
```
(("microbiome" OR "microbiota" OR "microbial" OR "gut bacteria") AND ("knowledge graph" OR "semantic web" OR "ontology" OR "RDF" OR "graph database"))
```

Search Parameters:
- Search within: All Content
- Document types: All document types
- Publication years: All years
- Content type: All content types

bioRxiv (via Crossref API)
URL: https://api.crossref.org/

API Query:
```
import requests
url = "https://api.crossref.org/works"
params = {
    "query": "microbiome knowledge graph",
    "filter": "from-pub-date:2000-01-01,until-pub-date:2026-03-31,type:posted-content",
    "rows": 100,
    "sort": "published",
    "order": "desc"
}
response = requests.get(url, params=params)
data = response.json()
```
Search Parameters:
- Query terms: "microbiome knowledge graph"
- Publication date range: 2000-01-01 to 2026-03-31
- Content type: posted-content (preprints)
- Publisher filter: bioRxiv, medRxiv



## 3. Search Development

### 3.1 Search Term Selection

Microbiome Terms:
- microbiome: Primary term for microbial community studies
- microbiota: Alternative term commonly used
- microbial: Broader term capturing microbial focus
- gut bacteria: Specific to human gut microbiome
- bacterial community: Broader bacterial community focus

Knowledge Graph Terms:
- knowledge graph: Primary term for KG systems
- semantic web: W3C semantic web technologies
- linked data: Linked open data principles
- ontology: Ontology-based approaches
- RDF: Resource Description Framework
- graph database: Property graph databases

### 3.2 Alternative Strategies Considered (Not Executed)

Strategy A: Broader microbiome terms
(microbiome OR microbiota OR microbial OR metagenome OR metagenomic OR bacteriome)
Not used: Would increase recall but significantly decrease precision (estimated impact: +1,200 additional records).

Strategy B: Narrower KG terms
("knowledge graph" OR "knowledge graphs")
Not used: Would miss studies using related semantic web technologies (estimated impact: -300 relevant records).

Strategy C: Technology-specific terms only
(RDF OR OWL OR SPARQL OR Neo4j)
Partially included in final strategy; not used alone as it would miss conceptual papers (estimated impact: -150 relevant records).

Note: Impact estimates based on preliminary query exploration, not systematic benchmarking.



## 4. Deduplication Strategy

### 4.1 Process

Stage 1: DOI Matching
- Exact match on Digital Object Identifier
- Removes identical records across databases

Stage 2: Title Normalization
- Normalize titles (lowercase, remove punctuation)
- Identify exact textual duplicates

Stage 3: Similarity Matching
- Algorithm: SequenceMatcher from Python's difflib
- Threshold: 0.85 similarity score
- Applied within publication years

### 4.2 Results

| Stage | Duplicates Found | Records Remaining |
|-------|------------------|-------------------|
| Initial | - | 769 |
| DOI matching | 0 | 769 |
| Title normalization | 0 | 769 |
| Similarity matching | 0 | 769 |
| Final | 0 | 769 |

### 4.3 Database Overlap Analysis

| Database Pair | Overlap (DOI) | Overlap (Title) |
|---------------|---------------|-----------------|
| PubMed <-> IEEE Xplore | 0 | 0 |
| PubMed <-> bioRxiv | 0 | 0 |
| IEEE Xplore <-> bioRxiv | 0 | 0 |

The lack of overlap indicates that each database captured distinct literature.

---

## 5. Search Validation

### 5.1 Sensitivity Analysis

No formal sensitivity analysis was conducted. Alternative search strategies were considered during protocol development (Section 3.2) but not systematically benchmarked. The 7.0% inclusion rate (54/769) and exclusion breakdown (E1: 61.7%, E2: 38.3%) serve as post-hoc indicators of search specificity.

### 5.2 Precision Assessment

No formal precision assessment was conducted due to resource constraints. The final search strategy was deemed appropriate based on:
- High proportion of exclusions for clear irrelevance (E1: not microbiome-related)
- Manageable inclusion volume for scoping review scope
- Coverage of key databases in biomedical and computational domains

---

## 6. Search Limitations

1. Database coverage: Only three databases searched. Scopus, Web of Science, and Google Scholar not included.
2. Language bias: Only English-language publications captured.
3. Grey literature: Conference abstracts, technical reports, and unpublished studies not systematically searched.
4. Citation searching: Forward and backward citation searching not performed.
5. Author contact: Authors not contacted to identify additional unpublished studies.
6. Validation: No formal precision or sensitivity benchmarking performed.



## 7. Data Export

### 7.1 Export Fields

PubMed: PMID, Title, Authors, Journal, Publication Year, DOI, Abstract
IEEE Xplore: Document Title, Authors, Publication Title, Publication Year, DOI, Abstract
bioRxiv: Title, Authors, Published Date, DOI, Publisher, Abstract

### 7.2 File Locations
```
data/raw/
├── pubmed_results_20260331.csv
├── exportIEEEEexplorer.csv
└── biorxiv_crossref_50_results.csv

```

## 8. Search Documentation

### 8.1 Search Log

| Timestamp | Action | Database | Results |
|-----------|--------|----------|---------|
| 2026-03-31 14:23:07 | Initial search | PubMed | 725 |
| 2026-03-31 14:45:22 | Initial search | IEEE Xplore | 10 |
| 2026-03-31 15:12:45 | Initial search | bioRxiv | 34 |
| 2026-03-31 15:30:00 | Deduplication | All | 769 |

Note: Timestamps from screening_report.json metadata. Verify against actual execution logs.

### 8.2 Version Control

Search strings and parameters are version-controlled in this repository.

---

## 9. References

1. Tricco AC, et al. PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation. Ann Intern Med. 2018;169(7):467-473.
2. Levac D, et al. Scoping reviews: time for clarity in definition, methods, and reporting. J Clin Epidemiol. 2010;63(12):1291-1294.

---

Document version: 1.0
Last updated: April 12, 2026
Maintainer: [Thabet Slimani - thabet.slimani@gmail.com]
