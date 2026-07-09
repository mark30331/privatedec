# NIW Case Study 1: Privacy-Preserving Preparation For Healthcare Research Sharing

Date: 2026-06-22  
Prepared by: Mark Kportufe  
Project: Privatedec

## 1. Scenario

This case study demonstrates how `Privatedec` can be used to prepare a small synthetic patient-style dataset for lower-risk use in healthcare research collaboration. The objective is to show a repeatable workflow for reducing re-identification risk before a dataset is shared with a research collaborator, student research team, or analytics group. The example uses synthetic data and is intended as a product evidence exhibit, not as a claim of legal compliance in any specific regulatory context.

## 2. Why It Matters

Healthcare research often depends on structured datasets containing demographic fields, geographic indicators, and diagnosis-related information. Even when a dataset appears simple, combinations of fields such as age and ZIP code can make individuals easier to identify, especially in smaller cohorts. As a result, many institutions either delay data sharing, rely on inconsistent manual redaction, or avoid collaborative use altogether.

`Privatedec` addresses this challenge by giving the user a structured workflow to:

- identify quasi-identifiers and sensitive attributes
- apply privacy-preserving processing before sharing
- retain reproducible evidence of what parameters were used
- limit downstream access through signed delivery and retention controls

This matters for the public interest because safer research data preparation can support more efficient collaboration while reducing privacy risk.

## 3. Input Dataset Summary

This example uses the synthetic sample dataset currently included in the project:

- source file: `docs/sample-upload.csv`
- dataset type: synthetic patient-style tabular CSV
- rows: 5
- columns: 4
- sample fields: `name`, `age`, `zipcode`, `diagnosis`
- direct identifiers present in source: `name`
- quasi-identifiers selected: `age`, `zipcode`
- sensitive attributes selected: `diagnosis`

For research sharing, the central concern is that a record could be linked through a combination of quasi-identifiers even if a direct identifier is not preserved in the final result.

## 4. Privatedec Workflow

The workflow documented in this case study is:

1. Upload the CSV dataset to `Privatedec`.
2. Review the automatically detected columns and preview rows.
3. Mark `age` and `zipcode` as quasi-identifiers.
4. Mark `diagnosis` as the sensitive attribute.
5. Choose privacy parameters appropriate for a small demonstrative dataset.
6. Launch asynchronous processing.
7. Review the generated processing report and result preview.
8. Download the processed CSV through the controlled result workflow.
9. Apply retention and deletion controls as part of data minimization.

This workflow is valuable because it moves privacy protection from an ad hoc spreadsheet process into a repeatable application flow with system-generated evidence.

## 5. Output And Controls

For this demonstrative case, the dataset can be processed using a successful parameter set appropriate for a very small sample. A practical example is:

- k value: `2`
- l value: `2`
- t value: `0.5`
- result status: completed successfully
- rows processed: 5
- privacy score: captured in the generated processing report
- processing time: captured in the generated processing report
- retention settings: original upload subject to short retention, result subject to separate retention, metadata retained longer for audit purposes
- secure delivery method: authenticated access and signed result download when object storage signing is enabled

The application also produces a printable report page documenting the selected parameters, result status, retention information, and result preview.

## 6. Before / After Summary

Before processing, the source data contains a direct identifier (`name`) and linkable quasi-identifiers (`age` and `zipcode`) that could create re-identification risk in a small dataset.

After processing:

- quasi-identifiers are generalized to reduce linkability
- sensitive information is preserved in a more controlled form suitable for group-level analysis
- the workflow is documented through a system-generated report
- result access is mediated through authenticated views and controlled download behavior
- retention rules support later deletion of original and result objects

Analytically useful information remains because the dataset still preserves the presence of diagnosis categories and demographic structure at a less identifying level of granularity.

## 7. Why This Supports National Importance

This case study supports a strong NIW narrative because it shows that `Privatedec` is not merely an abstract software concept. It demonstrates an operational process for lower-risk healthcare data preparation that can support collaborative research. Institutions across the United States regularly face the problem of wanting to analyze or share data without exposing patients or creating unmanaged privacy risk. A tool that introduces repeatable anonymization controls, report generation, and retention-aware handling directly contributes to safer research infrastructure.

This example also shows broader public value beyond a single employer. The workflow can be relevant to hospitals, university labs, public-interest analytics teams, biomedical researchers, and privacy-conscious data programs. By making privacy-preserving preparation more practical and reproducible, the endeavor contributes to healthcare research capacity and data governance in a way that has broader U.S. significance.

## 8. Exhibits To Attach

- screenshot of the upload page
- screenshot of the session detail page showing quasi-identifier and sensitive attribute selection
- screenshot of the processing page
- screenshot of the result page
- screenshot of the printable report page
- printed PDF of the generated report
- optional architecture diagram from the project documentation

## 9. Suggested Caption For Petition Use

This exhibit demonstrates a working example of `Privatedec` being used to transform a synthetic patient-style CSV into a lower-risk research dataset through a reproducible workflow involving quasi-identifier selection, anonymization controls, secure result delivery, and retention-aware handling.

