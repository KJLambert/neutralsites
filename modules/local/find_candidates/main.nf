process find_candidates {
    tag "${sample_id}"
    label 'process_low'
    publishDir "results/"
    input:
        tuple val(sample_id), path(gbk)
    output:
        tuple val(sample_id), path("${sample_id}_candidate_sites.tsv"), path(gbk)
    script: 
    """
    uv run find_intergenic_regions.py \
        -g ${gbk} \
        -o .
    
    mv candidate_sites.tsv ${sample_id}_candidate_sites.tsv
    """
}