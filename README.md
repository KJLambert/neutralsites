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
* The pipeline is set up to run a script (find_intergenic_regions). This will return a file with candidate_sites.

### Planned
* Possibly add a step that deals with obtaining inputs from various places, currently the user provides a gbff or gbk file.
* run a blast job to look for unique sites
* update the output table with sites that are unique in the genome.

## Quick start

* install nextflow and uv
* requires a genbank file (this is tested with gbff's from ncbi, which are usually annotated by prokka or bakta)
* run `nextflow run main.nf --gbk assets/GCA_006094495.1/genomic.gbff`

## Full documentation

<!-- TODO: Fill in this section with how to fully use the pipeline, what the inputs are and what the outputs look like. If this section ends up being super long, feel free to create a new docs/ directory and add details there. -->

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
