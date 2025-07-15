# KJLambert/neutralsites

Meant to be run in a local environment.
[![Nextflow](https://img.shields.io/badge/nextflow%20DSL2-%E2%89%A522.10.1-23aa62.svg)](https://www.nextflow.io/)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)
[![Launch on Nextflow Tower](https://img.shields.io/badge/Launch%20%F0%9F%9A%80-Nextflow%20Tower-%234256e7)](https://tower.nf/launch?pipeline=https://github.com/KJLambert/neutralsites)

## Introduction

**neutralsites** is A nextflow workflow for finding neutral sites in a genome. This applies to a specific situation where you need to find regions in a genome that are safe for genome editing. Safe from the perspective that these sites should not disrupt the functional genome. This is usually useful for non-model organisms since edit sites are often known for model organisms.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It uses Docker/Singularity containers making installation trivial and results highly reproducible. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies. Where possible, these processes have been submitted to and installed from [nf-core/modules](https://github.com/nf-core/modules) in order to make them available to all nf-core pipelines, and to everyone within the Nextflow community!

<!-- TODO: Add full-sized test dataset and amend the paragraph below if applicable -->

## Pipeline summary
* The pipeline is set up to run a script (find_intergenic_regions). This will return a file with a list of genome regions that are potentially good edit sites.

### Enhanced Workflow
The pipeline now includes three processing steps:

1. **Find Candidate Sites**: Identifies intergenic regions between convergent genes (200-500bp)
2. **Check Uniqueness** (Optional): Uses BLAST to verify sites are unique within the genome
3. **Quality Assessment** (Optional): Evaluates sites based on GC content, repeat content, sequence complexity, and length

For detailed information about the enhanced workflow, see [ENHANCED_WORKFLOW.md](ENHANCED_WORKFLOW.md).

### Planned
* Possibly add a step that deals with obtaining inputs from various sources (s3, custome API or NCBI datasets), currently the user provides a gbff or gbk file.
* run a blast job to look for unique sites
* update the output table with sites that are unique in the genome.

## Quick start

* install nextflow and uv
* requires a genbank file (this is tested with gbff's from ncbi, which are usually annotated by prokka or bakta)
* run `nextflow run main.nf --gbk assets/GCA_006094495.1/genomic.gbff`

## Full documentation

### input
The pipeline supports two input methods:

#### Single GenBank File
Provide a genbank file example for testing at `assets/GCA_006094495.1/genomic.gbff`. (specifically genes should be labeled via locus tag and the second part of the locus tag should be a relative number eg. GHJGK_12345)

```bash
nextflow run main.nf --gbk assets/GCA_006094495.1/genomic.gbff
```

#### Multiple GenBank Files (CSV Input)
For processing multiple files, create a CSV file with a header row and one column containing the paths to your GenBank files:

```csv
file_path
/path/to/genome1.gbk
/path/to/genome2.gbk
/path/to/genome3.gbk
```

Then run the pipeline with:
```bash
nextflow run main.nf --csv genomes.csv
```

**Notes:**
- The CSV must have a header row
- The column name can be anything (e.g., `file_path`, `genbank_file`, etc.)
- All file paths must be valid and accessible
- The pipeline will process each file in parallel
- Only one input method can be used at a time (either `--gbk` or `--csv`, not both)

### output
candidate_sites.tsv

`region_name | convergent | length | sequence | sequence flanking 2000 | note | match_count | uniqueness`

## Contributions and support

<!-- TODO: Add CONTRIBUTING.MD that is specific to Kyle Lambert -->

## Citations

<!-- TODO: Add bibliography of tools and data used in your pipeline -->

This cookiecutter template is based off of the `nf-core` template. You can cite the `nf-core` publication as follows:

> **The nf-core framework for community-curated bioinformatics pipelines.**
>
> Philip Ewels, Alexander Peltzer, Sven Fillinger, Harshil Patel, Johannes Alneberg, Andreas Wilm, Maxime Ulysse Garcia, Paolo Di Tommaso & Sven Nahnsen.
>
> _Nat Biotechnol._ 2020 Feb 13. doi: [10.1038/s41587-020-0439-x](https://dx.doi.org/10.1038/s41587-020-0439-x).

An extensive list of references for the tools used by the pipeline can be found in the [`CITATIONS.md`](CITATIONS.md) file.
