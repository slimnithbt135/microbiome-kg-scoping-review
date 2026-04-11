# Microbiome Knowledge Graph Scoping Review

[[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19441562.svg)](https://doi.org/10.5281/zenodo.19441562)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the complete data, code, and documentation for the scoping review:
**"Toward Semantic Knowledge Graph Infrastructure for Microbiome Intelligence: A PRISMA-ScR-Based Analysis and Framework"**

## Overview

This scoping review maps the landscape of microbiome knowledge graph systems following PRISMA-ScR guidelines. We searched PubMed, IEEE Xplore, and bioRxiv, identifying 769 records and including 54 studies in the final synthesis.

## Repository Structure

```
microbiome-kg-scoping-review/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CITATION.cff                       # Citation metadata
├── requirements.txt                   # Python dependencies
├── environment.yml                    # Conda environment specification
├── .gitignore                         # Git ignore patterns
│
├── data/                              # All data files
│   ├── raw/                           # Original search results (read-only)
│   │   ├── pubmed_results_20260331.csv
│   │   ├── exportIEEEEexplorer.csv
│   │   └── biorxiv_crossref_50_results.csv
│   │
│   ├── processed/                     # Deduplicated and processed data
│   │   ├── 01_deduplicated.csv
│   │   ├── screening_template.csv
│   │   ├── screening_completed.csv
│   │   ├── 02_final_included.csv
│   │   └── 02_excluded.csv
│   │
│   └── supplementary/                 # Supplementary datasets
│       ├── Supplementary_Table_1_All_Studies.csv
│       └── Table1_Real_Representatives.csv
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── screening/                     # Screening phase scripts
│   │   ├── __init__.py
│   │   ├── 01_dedup_and_screen.py
│   │   ├── 02_fulltext_and_synthesis.py
│   │   └── prisma_diagram.py
│   │
│   ├── analysis/                      # Analysis scripts
│   │   ├── __init__.py
│   │   ├── classification_analysis.py    # Statistical analysis
│   │   └── trend_visualization.py        # Figure generation
│   │
│   └── skgi/                          # SKGI implementation
│       ├── __init__.py
│       ├── core_schema.owl            # SKGI ontology (OWL)
│       ├── core_schema.shacl          # SHACL validation rules
│       └── example_implementation.py  # Reference implementation
│
├── docs/                              # Documentation
│   ├── SEARCH_PROTOCOL.md             # Complete search strategy
│   ├── SCREENING_GUIDE.md             # Screening decision guide
│   ├── CLASSIFICATION_FRAMEWORK.md    # Category definitions
│   ├── SKGI_BLUEPRINT.md              # Implementation specifications
│   └── BENCHMARK_PROTOCOL.md          # Evaluation protocols
│
├── outputs/                           # Generated outputs
│   ├── figures/                       # PRISMA and analysis figures
│   │   ├── Figure_1A_Temporal_Distribution.png
│   │   ├── Figure_1B_Category_Distribution.png
│   │   ├── Figure_1C_Technology_Distribution.png
│   │   ├── Figure_1D_FAIR_Compliance.png
│   │   ├── Figure_1E_Source_Distribution.png
│   │   ├── Figure_1F_Ontology_Usage.png
│   │   └── Figure_1_Combined_Analysis.png
│   │
│   └── reports/                       # Analysis reports
│       ├── classification_analysis_report.json
│       └── screening_report.json
│
├── supplementary_materials/           # Paper supplementary files
│   ├── Supplementary_Material_1_Search_Strings.pdf
│   ├── Supplementary_Material_2_PRISMA_Checklist.pdf
│   ├── Supplementary_Table_1_All_Studies.xlsx
│   └── Supplementary_Figure_1_Temporal_Trends.png
│
└── tests/                             # Unit tests
    ├── __init__.py
    ├── test_deduplication.py
    ├── test_screening.py
    └── test_classification.py
```

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/username/microbiome-kg-scoping-review.git
cd microbiome-kg-scoping-review

# Install dependencies
pip install -r requirements.txt
```

### Running Analysis

```bash
# Generate statistical analysis report
python src/analysis/classification_analysis.py \
    --input data/supplementary/Supplementary_Table_1_All_Studies.csv \
    --output outputs/reports/

# Generate all figures
python src/analysis/trend_visualization.py \
    --input data/supplementary/Supplementary_Table_1_All_Studies.csv \
    --output outputs/figures/

# Generate example SKGI knowledge graph
python src/skgi/example_implementation.py \
    --output outputs/example_kg.ttl
```

## Key Findings

From 54 included studies:

- **61.1%** of studies published between 2022-2026 (rapid recent growth)
- **92.6%** use RDF/OWL-based semantic web technologies
- **46.3%** are MDKG-type (Microbe-Disease Knowledge Graphs)
- **46.3%** achieve High FAIR compliance
- **88.9%** use NCBI Taxonomy for taxonomic classification

## Data Availability

All 769 records identified in the search are available in `data/processed/01_deduplicated.csv`.
The 54 included studies with classifications are in `data/supplementary/Supplementary_Table_1_All_Studies.csv`.

## Citation

If you use this code or data, please cite:

```
Slimani, T. (2026). Toward Semantic Knowledge Graph Infrastructure for 
Microbiome Intelligence: A PRISMA-ScR-Based Analysis and Framework. 
Briefings in Bioinformatics.
```

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contact

Thabet Slimani - t.slimani@tu.edu.sa
