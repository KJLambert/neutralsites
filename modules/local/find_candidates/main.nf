process find_candidates {
    publishDir "results/"
    input:
        path gbk
    output:
        path 'candidate_sites.tsv'
    script: 
    """
    uv run find_intergenic_regions.py \
        -g ${gbk} \
        -o .
    """
}