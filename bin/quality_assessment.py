#!/usr/bin/env python3
"""
Quality assessment of candidate neutral sites.

This script evaluates candidate sites based on multiple quality metrics including
GC content, repeat content, sequence complexity, and length.
"""

import pandas as pd
import numpy as np
from Bio import SeqIO
from Bio.SeqUtils import GC
from collections import Counter
import click
from pathlib import Path


def calculate_gc_content(sequence):
    """Calculate GC content percentage."""
    return GC(sequence)


def calculate_repeat_content(sequence, min_repeat_length=10):
    """
    Calculate repeat content in a sequence.
    
    Args:
        sequence (str): DNA sequence
        min_repeat_length (int): Minimum length of repeats to consider
    
    Returns:
        float: Proportion of sequence that is repetitive
    """
    if len(sequence) < min_repeat_length:
        return 0.0
    
    repeat_content = 0
    for i in range(len(sequence) - min_repeat_length + 1):
        repeat = sequence[i:i+min_repeat_length]
        if sequence.count(repeat) > 1:
            repeat_content += 1
    
    return repeat_content / len(sequence) if len(sequence) > 0 else 0.0


def calculate_sequence_entropy(sequence):
    """
    Calculate sequence complexity using Shannon entropy.
    
    Args:
        sequence (str): DNA sequence
    
    Returns:
        float: Entropy value (0-2 for DNA)
    """
    if not sequence:
        return 0.0
    
    base_counts = Counter(sequence)
    total_bases = len(sequence)
    
    entropy = 0.0
    for count in base_counts.values():
        if count > 0:
            p = count / total_bases
            entropy -= p * np.log2(p)
    
    return entropy


def calculate_length_score(length, optimal_min=300, optimal_max=400, acceptable_min=250, acceptable_max=450):
    """
    Calculate length score based on optimal and acceptable ranges.
    
    Args:
        length (int): Length of the sequence
        optimal_min (int): Lower bound of optimal length
        optimal_max (int): Upper bound of optimal length
        acceptable_min (int): Lower bound of acceptable length
        acceptable_max (int): Upper bound of acceptable length
    
    Returns:
        float: Length score (0-1)
    """
    if optimal_min <= length <= optimal_max:
        return 1.0
    elif acceptable_min <= length <= acceptable_max:
        return 0.8
    else:
        return 0.5


def assess_quality(sites_file, output_file, quality_threshold=0.5):
    """
    Assess quality of candidate neutral sites.
    
    Args:
        sites_file (str): Path to sites TSV file
        output_file (str): Path to output file
        quality_threshold (float): Minimum quality score for recommendations
    """
    # Read sites
    sites = pd.read_csv(sites_file, sep='\t')
    
    # Calculate quality metrics for each site
    quality_metrics = []
    
    for idx, site in sites.iterrows():
        sequence = site['neutral_sequence']
        length = site['length']
        
        # Calculate individual metrics
        gc_content = calculate_gc_content(sequence)
        repeat_content = calculate_repeat_content(sequence)
        entropy = calculate_sequence_entropy(sequence)
        length_score = calculate_length_score(length)
        
        # Calculate overall quality score
        quality_score = (
            (1 - abs(gc_content - 50) / 50) * 0.3 +  # GC content preference
            (1 - repeat_content) * 0.3 +              # Low repeat content
            (entropy / 2) * 0.2 +                     # High complexity
            length_score * 0.2                        # Optimal length
        )
        
        # Determine recommendation
        if quality_score > 0.7:
            recommendation = 'high'
        elif quality_score > 0.5:
            recommendation = 'medium'
        else:
            recommendation = 'low'
        
        quality_metrics.append({
            'region_name': site['region_name'],
            'gc_content': gc_content,
            'repeat_content': repeat_content,
            'sequence_entropy': entropy,
            'length_score': length_score,
            'quality_score': quality_score,
            'recommendation': recommendation
        })
    
    # Create quality dataframe
    quality_df = pd.DataFrame(quality_metrics)
    
    # Merge with original sites
    final_sites = sites.merge(quality_df, on='region_name', how='left')
    
    # Sort by quality score
    final_sites = final_sites.sort_values('quality_score', ascending=False)
    
    # Save quality-assessed sites
    final_sites.to_csv(output_file, sep='\t', index=False)
    
    # Print summary statistics
    total_sites = len(final_sites)
    high_quality = len(final_sites[final_sites['quality_score'] > 0.7])
    medium_quality = len(final_sites[(final_sites['quality_score'] > 0.5) & (final_sites['quality_score'] <= 0.7)])
    low_quality = len(final_sites[final_sites['quality_score'] <= 0.5])
    
    print(f'Quality Assessment Summary:')
    print(f'  Total sites analyzed: {total_sites}')
    print(f'  High quality sites (score > 0.7): {high_quality}')
    print(f'  Medium quality sites (0.5-0.7): {medium_quality}')
    print(f'  Low quality sites (score <= 0.5): {low_quality}')
    print(f'  Average quality score: {final_sites["quality_score"].mean():.3f}')


@click.command(help="Assess quality of candidate neutral sites")
@click.option(
    "--sites",
    "-s",
    required=True,
    help="Path to sites TSV file"
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="Path to output file"
)
@click.option(
    "--quality-threshold",
    "-q",
    default=0.5,
    help="Minimum quality score for recommendations (default: 0.5)"
)
def main(sites, output, quality_threshold):
    """Assess quality of candidate neutral sites."""
    assess_quality(sites, output, quality_threshold)


if __name__ == "__main__":
    main() 