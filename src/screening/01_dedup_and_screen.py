#!/usr/bin/env python3
"""
================================================================================
SCOPING REVIEW - PHASE 1: DEDUPLICATION & TITLE/ABSTRACT SCREENING
================================================================================
Simplified workflow for scoping review with single-reviewer screening.

Usage:
    python 01_dedup_and_screen.py --pubmed pubmed_results.csv --ieee ieee.csv

Output:
    - deduplicated.csv: Unique records
    - screening_template.csv: Ready for screening
    - auto_screened.csv: Pre-screened with suggestions
================================================================================
"""

import pandas as pd
import numpy as np
import argparse
import re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher


def normalize_text(text):
    """Normalize text for matching"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def similarity(a, b):
    """Calculate string similarity"""
    return SequenceMatcher(None, a, b).ratio()


def load_pubmed(file):
    import pandas as pd
    
    df = pd.read_csv(file)
    
    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # Column mapping
    col_map = {
        'title': ['title'],
        'authors': ['authors', 'author'],
        'journal': ['journal', 'source', 'journal title', 'journal_title'],
        'year': ['year', 'pubyear', 'publication year'],
        'doi': ['doi'],
        'abstract': ['abstract', 'abstracttext', 'summary']
    }

    def find_col(possible_names):
        for name in possible_names:
            if name in df.columns:
                return name
        return None

    def safe_get(column_key):
        col = find_col(col_map[column_key])
        if col is not None:
            return df[col]
        else:
            return [''] * len(df)   # ✅ prevent crash

    # Build clean dataframe safely
    clean_df = pd.DataFrame()

    clean_df['title'] = safe_get('title')
    clean_df['authors'] = safe_get('authors')
    clean_df['journal'] = safe_get('journal')   # ✅ FIXED
    clean_df['year'] = safe_get('year')
    clean_df['doi'] = safe_get('doi')
    clean_df['abstract'] = safe_get('abstract')

    clean_df['source'] = 'pubmed'
    clean_df['id'] = range(len(clean_df))

    return clean_df


def load_ieee(filepath):
    """Load IEEE Xplore data"""
    print(f"\n📥 Loading IEEE Xplore: {filepath}")
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    df = df.rename(columns={
        'Document Title': 'title',
        'Authors': 'authors',
        'Publication Title': 'journal',
        'Publication Year': 'year',
        'DOI': 'doi',
        'Abstract': 'abstract'
    })
    df['source'] = 'IEEE Xplore'
    df['id'] = df.index.map(lambda x: f"IEEE_{x}")
    print(f"   ✓ {len(df)} records")
    return df[['id', 'title', 'authors', 'journal', 'year', 'doi', 'abstract', 'source']]


def load_scholar(filepath):
    """Load Google Scholar data"""
    print(f"\n📥 Loading Google Scholar: {filepath}")
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filepath, encoding='latin-1')
    
    # Auto-detect columns
    col_map = {}
    for col in df.columns:
        c = col.lower()
        if 'title' in c:
            col_map[col] = 'title'
        elif 'author' in c:
            col_map[col] = 'authors'
        elif 'journal' in c or 'source' in c:
            col_map[col] = 'journal'
        elif 'year' in c:
            col_map[col] = 'year'
        elif 'doi' in c:
            col_map[col] = 'doi'
        elif 'abstract' in c:
            col_map[col] = 'abstract'
    
    df = df.rename(columns=col_map)
    df['source'] = 'Google Scholar'
    df['id'] = df.index.map(lambda x: f"SCHOLAR_{x}")
    print(f"   ✓ {len(df)} records")
    return df[['id', 'title', 'authors', 'journal', 'year', 'doi', 'abstract', 'source']]


def load_biorxiv(filepath):
    """Load bioRxiv data"""
    print(f"\n📥 Loading bioRxiv: {filepath}")
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    
    # Standardize columns
    if 'DOI' in df.columns and 'doi' not in df.columns:
        df = df.rename(columns={'DOI': 'doi'})
    if 'Title' in df.columns and 'title' not in df.columns:
        df = df.rename(columns={'Title': 'title'})
    
    df['source'] = 'bioRxiv'
    df['id'] = df.index.map(lambda x: f"BIORXIV_{x}")
    print(f"   ✓ {len(df)} records")
    return df[['id', 'title', 'authors', 'journal', 'year', 'doi', 'abstract', 'source']]


def deduplicate(dfs):
    """Remove duplicates across all sources"""
    print("\n" + "="*60)
    print("DEDUPLICATION")
    print("="*60)
    
    combined = pd.concat(dfs, ignore_index=True)
    total_before = len(combined)
    print(f"\nTotal before dedup: {total_before}")
    
    # Normalize for matching
    combined['title_norm'] = combined['title'].apply(normalize_text)

    # =========================
    # DOI DEDUPLICATION (ROBUST)
    # =========================
    combined['doi'] = combined['doi'].astype(str).str.strip()

    with_doi = combined[combined['doi'] != '']
    without_doi = combined[combined['doi'] == '']

    with_doi = with_doi.drop_duplicates(subset='doi', keep='first')

    combined = pd.concat([with_doi, without_doi], ignore_index=True)

    # Secondary deduplication by normalized title
    combined = combined.drop_duplicates(subset='title_norm', keep='first')

    # =========================
    # SIMILARITY DEDUPLICATION
    # =========================
    to_drop = []
    for year in combined['year'].dropna().unique():
        year_df = combined[combined['year'] == year]
        titles = year_df['title_norm'].tolist()
        indices = year_df.index.tolist()
        
        for i, (idx1, t1) in enumerate(zip(indices, titles)):
            if idx1 in to_drop:
                continue
            for idx2, t2 in zip(indices[i+1:], titles[i+1:]):
                if idx2 in to_drop:
                    continue
                if similarity(t1, t2) > 0.85:
                    to_drop.append(idx2)

    combined = combined.drop(index=to_drop)

    # Cleanup
    combined = combined.drop(columns=['title_norm'])

    # Correct duplicate count
    duplicates_removed = total_before - len(combined)

    print(f"After dedup: {len(combined)}")
    print(f"Duplicates removed: {duplicates_removed}")
    
    return combined

def auto_screen(df):
    print("\n" + "="*60)
    print("AUTO-SCREENING (SCORING MODE)")
    print("="*60)
    
    microbiome_terms = ['microbiome', 'microbiota', 'microbial', 'gut']
    kg_terms = ['knowledge graph', 'ontology', 'rdf', 'owl', 'graph']
    
    scores = []
    decisions = []
    
    for _, row in df.iterrows():
        text = (str(row.get('title','')) + ' ' + str(row.get('abstract',''))).lower()
        
        score = 0
        
        score += sum(2 for t in microbiome_terms if t in text)
        score += sum(2 for t in kg_terms if t in text)
        
        if 'gnn' in text or 'embedding' in text:
            score += 1
        
        scores.append(score)
        
        if score >= 6:
            decisions.append('Include')
        elif score <= 2:
            decisions.append('Exclude')
        else:
            decisions.append('Review')
    
    df['score'] = scores
    df['auto_decision'] = decisions
    
    print(f"\nInclude: {decisions.count('Include')}")
    print(f"Exclude: {decisions.count('Exclude')}")
    print(f"Review: {decisions.count('Review')}")
    
    return df
def create_template(df, output_dir):
    """Create screening template"""
    print("\n" + "="*60)
    print("CREATING SCREENING TEMPLATE")
    print("="*60)
    
    # Add screening columns
    df['screening_decision'] = df['auto_decision']
    df['screening_reason'] = df['auto_reason']
    df['reviewer_notes'] = ''
    df['screening_date'] = ''
    
    # Reorder columns
    cols = ['id', 'title', 'authors', 'year', 'journal', 'doi', 'source',
            'auto_decision', 'auto_reason', 'screening_decision', 
            'screening_reason', 'reviewer_notes', 'screening_date', 'abstract']
    df = df[[c for c in cols if c in df.columns]]
    
    # Save template
    template_path = Path(output_dir) / 'screening_template.csv'
    df.to_csv(template_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ Template saved: {template_path}")
    
    return template_path


def main():
    parser = argparse.ArgumentParser(description='Scoping Review - Deduplication & Screening')
    parser.add_argument('--pubmed', type=str, help='PubMed CSV file')
    parser.add_argument('--ieee', type=str, help='IEEE Xplore CSV file')
    parser.add_argument('--scholar', type=str, help='Google Scholar CSV file')
    parser.add_argument('--biorxiv', type=str, help='bioRxiv CSV file')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')
    
    args = parser.parse_args()
    
    print("="*60)
    print("SCOPING REVIEW - PHASE 1: DEDUPLICATION & SCREENING")
    print("="*60)
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load all sources
    sources = []
    if args.pubmed:
        sources.append(load_pubmed(args.pubmed))
    if args.ieee:
        sources.append(load_ieee(args.ieee))
    if args.scholar:
        sources.append(load_scholar(args.scholar))
    if args.biorxiv:
        sources.append(load_biorxiv(args.biorxiv))
    
    if not sources:
        print("❌ No input files provided!")
        return
    
    # Deduplicate
    df = deduplicate(sources)
    
    # Save deduplicated
    dedup_path = output_dir / '01_deduplicated.csv'
    df.to_csv(dedup_path, index=False, encoding='utf-8-sig')
    print(f"✅ Deduplicated: {dedup_path}")
    
    # Auto-screen
    df = auto_screen(df)
    
    # Create template
    template_path = create_template(df, output_dir)
    
    # Prepare source counts
    source_counts = df['source'].value_counts().to_string().replace('\n', '\n   ')

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"""
📊 RESULTS:
   Total unique records: {len(df)}
   
   By source:
{source_counts}
   
   Auto-screening:
   ✓ Include: {(df['auto_decision'] == 'Include').sum()}
   ✗ Exclude: {(df['auto_decision'] == 'Exclude').sum()}
   ⏳ Review: {(df['auto_decision'] == 'Review').sum()}

📁 FILES:
   - {dedup_path}
   - {template_path}

📝 NEXT STEPS:
   1. Open: {template_path}
   2. Review auto-screened records
   3. Change decisions as needed
   4. Save as: screening_completed.csv
   5. Run: python 02_fulltext_and_synthesis.py --input screening_completed.csv
""")



if __name__ == '__main__':
    main()
