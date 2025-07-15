process quality_assessment {
    tag "${sample_id}"
    label 'process_low'
    publishDir "results/"
    input:
        tuple val(sample_id), path(unique_sites), path(genome)
    output:
        tuple val(sample_id), path("${sample_id}_quality_assessed_sites.tsv")
    script: 
    """
    # Run quality assessment using the dedicated Python script
    uv run quality_assessment.py \
        --sites ${unique_sites} \
        --output ${sample_id}_quality_assessed_sites.tsv \
        --quality-threshold ${params.quality_score_threshold}
    """
} 