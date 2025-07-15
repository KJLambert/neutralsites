/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    VALIDATE INPUTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

def summary_params = NfcoreSchema.paramsSummaryMap(workflow, params)

// TODO: Add all file path parameters for the pipeline to the list below
// Check input path parameters to see if they exist
def checkPathParamList = []
if (params.gbk) { 
    checkPathParamList.add(params.gbk) 
}
if (params.csv) { 
    checkPathParamList.add(params.csv) 
}

// Validate that at least one input method is provided
if (!params.gbk && !params.csv) {
    log.error "No input provided. Please specify either --gbk for a single file or --csv for multiple files."
    System.exit(1)
}

// Validate that only one input method is provided
if (params.gbk && params.csv) {
    log.error "Both --gbk and --csv parameters provided. Please use only one input method."
    System.exit(1)
}

for (param in checkPathParamList) { 
    if (param) { 
        file(param, checkIfExists: true) 
    } 
}


/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CONFIG FILES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT LOCAL MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { find_candidates        } from '../modules/local/find_candidates/main'
include { check_uniqueness       } from '../modules/local/check_uniqueness/main'
include { quality_assessment     } from '../modules/local/quality_assessment/main'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT NF-CORE MODULES/SUBWORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

//
// MODULE: Installed directly from nf-core/modules
//


/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

workflow NEUTRALSITES {
    // Create input channel based on parameter provided
    ch_gbk = Channel.empty()
    
    if (params.gbk) {
        // Single file input
        ch_gbk = Channel.fromPath(params.gbk).map { file -> 
            [file.baseName, file] 
        }
    } else if (params.csv) {
        // CSV input with multiple files
        ch_gbk = Channel
            .fromPath(params.csv)
            .splitCsv(header: true)
            .map { row -> 
                // Assuming CSV has a column with file paths
                // You can adjust the column name as needed
                def filePath = row.values().find { it }
                if (!filePath) {
                    log.error "No valid file path found in CSV row: ${row}"
                    System.exit(1)
                }
                def file = file(filePath, checkIfExists: true)
                // Use filename as sample ID, or extract from CSV if available
                [file.baseName, file]
            }
    }

    // Step 1: Find candidate sites
    candidates = find_candidates(ch_gbk)
    
    // Step 2: Check uniqueness using BLAST (optional)
    unique_sites = params.skip_uniqueness_check ? candidates : check_uniqueness(candidates)
    
    // Step 3: Quality assessment (optional)
    quality_assessed = params.skip_quality_assessment ? unique_sites : quality_assessment(unique_sites)
}
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    COMPLETION EMAIL AND SUMMARY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

workflow.onComplete {
    if (params.email || params.email_on_fail) {
        NfcoreTemplate.email(workflow, params, summary_params, projectDir, log, multiqc_report)
    }
    NfcoreTemplate.summary(workflow, params, log)
}

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
