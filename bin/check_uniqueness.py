#!/usr/bin/env python3
"""
Check uniqueness of candidate neutral sites using BLAST results.

This script processes BLAST output to identify unique sites within a genome.
"""

import pandas as pd
import sys
import click
from pathlib import Path


def check_uniqueness(candidate_sites_file, blast_results_file, output_file, identity_threshold=95.0):
    """
    Check uniqueness of candidate sites using BLAST results.
    
    Args:
        candidate_sites_file (str): Path to candidate sites TSV file
        blast_results_file (str): Path to BLAST results file
        output_file (str): Path to output file
        identity_threshold (float): Minimum identity percentage for matches
    """
    # Read candidate sites
    candidates = pd.read_csv(candidate_sites_file, sep='\t')
    
    # Read BLAST results
    blast_cols = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 
                  'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    
    try:
        blast_results = pd.read_csv(blast_results_file, sep='\t', names=blast_cols, header=None)
    except pd.errors.EmptyDataError:
        # If BLAST found no matches, all sites are unique
        print("No BLAST matches found - we expect 1 match per candidate.. something went wrong in blast step")
        candidates['match_count'] = 0
        candidates['uniqueness'] = 'Unchecked'
        candidates.to_csv(output_file, sep='\t', index=False) # check whether re-write is OK
        return
    
    # Filter for high-quality matches (identity > threshold and length > 90% of query)
    length_thresh = candidates.rename(columns={'region_name': 'qseqid'}).set_index('qseqid')['length'] * 0.9
    blast_results['length_threshold'] = blast_results['qseqid'].map(length_thresh)
    high_quality_matches = blast_results[
        (blast_results['pident'] > identity_threshold) & 
        (blast_results['length'] > blast_results['length_threshold'] ) ]
    
    # Count matches per candidate site
    match_counts = high_quality_matches.groupby('qseqid').size().reset_index(name='match_count')
    
    # Merge with candidates and filter for unique sites (only 1 match = self-match)
    unique_sites = candidates.merge(match_counts, left_on='region_name', right_on='qseqid', how='left')
    unique_sites['match_count'] = unique_sites['match_count'].fillna(0)
    #unique_sites = unique_sites[unique_sites['match_count'] <= 1]
    
    # Update uniqueness
    # uniqueness = True if < 1 match, otherwise uniqueness = False
    unique_sites['uniqueness'] = unique_sites['match_count'].apply(lambda x: True if x <= 1 else False)
    
    # Remove the redundant qseqid column
    if 'qseqid' in unique_sites.columns:
        unique_sites = unique_sites.drop('qseqid', axis=1)
    
    # Save unique sites
    unique_sites.to_csv(output_file, sep='\t', index=False)
    
    # Print summary
    total_sites = len(candidates)
    unique_count = len(unique_sites)
    print(f"Uniqueness check summary:")
    print(f"  Total candidate sites: {total_sites}")
    print(f"  Unique sites: {unique_count}")
    print(f"  Filtered out: {total_sites - unique_count}")


@click.command(help="Check uniqueness of candidate neutral sites using BLAST results")
@click.option(
    "--candidate-sites",
    "-c",
    required=True,
    help="Path to candidate sites TSV file"
)
@click.option(
    "--blast-results",
    "-b",
    required=True,
    help="Path to BLAST results file"
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="Path to output file"
)
@click.option(
    "--identity-threshold",
    "-i",
    default=95.0,
    help="Minimum identity percentage for BLAST matches (default: 95.0)"
)
def main(candidate_sites, blast_results, output, identity_threshold):
    """Check uniqueness of candidate neutral sites."""
    check_uniqueness(candidate_sites, blast_results, output, identity_threshold)


if __name__ == "__main__":
    main() 