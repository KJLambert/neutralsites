process find_candidates {
    publishDir "results/"
    input:
        path gbk
    output:
        path "${gbk.baseName}_candidate_sites.tsv"
    script: 
    """
    uv run find_intergenic_regions.py \
        -g ${gbk} \
        -o .
    mv candidate_sites.tsv ${gbk.baseName}_candidate_sites.tsv
    """
}