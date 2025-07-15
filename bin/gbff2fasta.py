#!/usr/bin/env python3
"""
Convert gbff to fasta
"""

from Bio import SeqIO
import sys
import click

def gbffTofna(gbff, output):
    """convert genbank file.

    Args:
        gbff_file (str): Path to genbank file
        out_file (str): Output fasta file name
    """
    # Read genbank file
    #records = SeqIO.parse(gbk_file, "genbank")
    SeqIO.convert(gbff, "genbank", output, "fasta")

@click.command(help=("Find all neutral sites in a genome. Note that this script does not look at uniqueness yet."))
@click.option(
    "--gbff",
    "-g",
    help=("File path to a genbank file"),
)
@click.option(
    "--output",
    "-o",
    help="Output fasta file name",
)
def main(gbff, output):
    gbffTofna(gbff, output)


if __name__ == "__main__":
    main()
