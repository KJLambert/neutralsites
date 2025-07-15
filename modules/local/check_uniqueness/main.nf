process check_uniqueness {
    tag "${sample_id}"
    label 'process_low' /* this might be tied to AWS configuration */
    publishDir "results/"
    input:
        tuple val(sample_id), path(candidate_sites), path(genome)
    output:
        tuple val(sample_id), path("${sample_id}_unique_sites.tsv")
    script: 
    """
    # Create a temporary FASTA file with candidate sequences
    awk -F'\t' 'NR>1 {print ">" \$1 "\\n" \$4}' ${candidate_sites} > candidate_sequences.fasta
    
    # convert the gbff to fasta with seqkit 
    uv run gbff2fasta.py \
        --gbff ${genome} \
        --output genome.fna

    # Create BLAST database from the genome
    makeblastdb -in genome.fna -dbtype nucl -out genome_db
    
    # Run BLAST to check uniqueness
    blastn -query candidate_sequences.fasta -db genome_db -out blast_results.txt -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"
    
    # Process BLAST results using the dedicated Python script TODO - update the 
    uv run check_uniqueness.py \
        --candidate-sites ${candidate_sites} \
        --blast-results blast_results.txt \
        --output ${sample_id}_unique_sites.tsv \
        --identity-threshold 97
    """
} 