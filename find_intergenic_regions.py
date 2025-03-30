#!/usr/bin/env python3
"""
Find all neutral sites in a genome, return a table with
region_name | convergent | length | uniqueness | sequence | sequence flanking 2000 | notes

Scan intergenic regions, only report regions with forward - reverse having length 200 - 500bp
Add in blast for uniqueness later!
Report sequence and 1000bp flanking regions.
"""

from Bio import SeqIO
import sys
import click
#import requests # add option to pull gbk with the API
#import yaml
from pathlib import Path


def find_intergenic_regions(gbk_file, out_path):
    """Parse genbank file and find intergenic regions between convergent genes.
    
    Args:
        gbk_file (str): Path to genbank file
        out_path (Path): Output directory path
    """
    # Read genbank file
    records = SeqIO.parse(gbk_file, "genbank")
    
    # Get all CDS features and their strands
    intergenic_regions = [] # initiate a list of 'region' dictionaries
    for rec in records:
        feats = []
        for feature in rec.features: 
            if feature.type == "CDS": # ideally regions would account for RNA features and avoid them
                try:
                    feats.append({
                        'start': int(feature.location.start),
                        'end': int(feature.location.end),
                        'strand': int(feature.location.strand),
                        'type': feature.type,
                        'short_tag': feature.qualifiers.get('locus_tag', ['Unknown'])[0].split('_')[2],
                        'locus_tag': feature.qualifiers.get('locus_tag', ['Unknown'])[0],
                        'gene': feature.qualifiers.get('gene', ['Unknown'])[0],
                        'product': feature.qualifiers.get('product', ['Unknown'])[0]
                    })
                except:
                    print(f"unconverted locus tag, usually on small contigs, avoid anyway: {feature.qualifiers.get('locus_tag', ['Unknown'])[0]}")
    
        # Sort genes by start position
        feats.sort(key=lambda x: x['start'])
        
        # Find intergenic regions between convergent genes
        for i in range(len(feats)-1):
            current_feat = feats[i]
            next_feat = feats[i+1]
            
            # Check if genes are convergent (-> <-)
            if current_feat['strand'] == 1 and next_feat['strand'] == -1:
                intergenic_length = next_feat['start'] - current_feat['end']
                
                # Only keep regions between 200-500bp
                if 200 <= intergenic_length <= 500:
                    region = {
                        'upstream_gene': current_feat['locus_tag'],
                        'downstream_gene': next_feat['locus_tag'],
                        'upstream_gene_annotation': "gene: "+current_feat['gene']+" product: "+current_feat['product'],
                        'downstream_gene_annotation': "gene: "+next_feat['gene']+" product: "+next_feat['product'],
                        'region_name':current_feat['short_tag']+"_"+next_feat['short_tag'],
                        'convergent':'yes',
                        'start': current_feat['end'],
                        'end': next_feat['start'],
                        'length': intergenic_length,
                        'sequence': rec.seq[current_feat['end']:next_feat['start']],
                        'flanking_sequence': rec.seq[max(0, current_feat['end']-1000):min(len(rec.seq), next_feat['start']+1000)]
                    }
                    intergenic_regions.append(region)
    
    # Write results to file
    with open(out_path / "neutral_sites.tsv", 'w') as f:
        f.write("region_name\tconvergent\tlength\tneutral_sequence\tflanking_Sequences\tNotes\n")
        for i, region in enumerate(intergenic_regions):
            #name = f"neutral_site_{i+1}"
            f.write(f"{region['region_name']}\t"
                    f"{region['convergent']}\t"
                    f"{region['length']}\t"
                    f"{region['sequence']}\t"
                    f"{region['flanking_sequence']}\t"
                    f"Between {region['upstream_gene_annotation']} and {region['downstream_gene_annotation']}\n")




@click.command(
    help=(
        "Find all neutral sites in a genome. Note that this script does not look at uniqueness yet."
    )
)
@click.option(
    "--gbk",
    "-g",
    help=(
        "File path to a genbank file"
    ),
)
@click.option(
    "--output-directory",
    "-o",
    help="Path to save outputs",
)


def main(gbk, output_directory):
    out_path = Path(output_directory)
    out_path.mkdir(parents=True, exist_ok=True)
    find_intergenic_regions(gbk,out_path)

if __name__ == "__main__":
    main()