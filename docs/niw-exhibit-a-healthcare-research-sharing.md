# Exhibit A

## Demonstrative Use Of `Privatedec` For Privacy-Preserving Healthcare Research Data Sharing

Prepared for NIW evidence assembly  
Prepared by: Mark Kportufe  
Date: 2026-06-22

Note: This exhibit uses a synthetic dataset for demonstrative purposes. It is submitted to illustrate the functionality and public-facing value of the proposed endeavor. It is not presented as a legal opinion or as a claim that any particular dataset satisfies a regulatory standard in all contexts.

## I. Purpose Of This Exhibit

This exhibit demonstrates a practical use case for `Privatedec`, a privacy-preserving software platform developed by Mark Kportufe to support lower-risk preparation of structured datasets for healthcare research and related analytical use. The exhibit is offered to show that the proposed endeavor is concrete, technically implemented, and relevant to a nationally significant problem: enabling safer and more reproducible use of sensitive healthcare data.

More specifically, this exhibit shows how `Privatedec` can be used to transform a synthetic patient-style CSV dataset into a lower-risk research asset through a structured workflow involving column review, privacy parameter selection, asynchronous anonymization, controlled result delivery, and retention-aware governance.

## II. Scenario Presented

In healthcare research settings, institutions often need to share or analyze data containing demographic and diagnosis-related fields. Even when a dataset does not appear highly complex, combinations of fields such as age and ZIP code may increase re-identification risk, particularly in small cohorts. This risk frequently leads to delay, inconsistent manual redaction, or avoidance of broader data use.

The scenario presented in this exhibit is therefore a representative one: a research team seeks to prepare a structured dataset for lower-risk collaboration without relying on informal spreadsheet edits or undocumented preprocessing steps.

## III. Demonstrative Dataset

This exhibit uses the synthetic sample dataset currently included in the project repository.

- Source file: `docs/sample-upload.csv`
- Dataset type: synthetic patient-style tabular CSV
- Number of rows: 5
- Number of columns: 4
- Included fields: `name`, `age`, `zipcode`, `diagnosis`
- Direct identifier present in source data: `name`
- Quasi-identifiers selected in the workflow: `age`, `zipcode`
- Sensitive attribute selected in the workflow: `diagnosis`

The purpose of the example is to demonstrate the workflow and the governance-oriented design of the system, rather than to maximize statistical complexity.

## IV. Workflow Demonstrated By `Privatedec`

This exhibit reflects the following application workflow:

1. A user uploads a structured CSV dataset into `Privatedec`.
2. The application analyzes the file and presents a preview and detected columns.
3. The user designates `age` and `zipcode` as quasi-identifiers and `diagnosis` as the sensitive attribute.
4. The user configures privacy parameters suited to a small demonstrative dataset.
5. The system launches background processing through an asynchronous task workflow.
6. The application produces a result page and a printable report documenting the processing outcome.
7. The processed result is delivered through an authenticated workflow, with signed delivery where supported by the configured object storage.
8. The application applies retention-aware handling and supports later deletion of stored artifacts.

This workflow is significant because it replaces ad hoc manual handling with a repeatable software process that preserves an evidentiary record of how the dataset was prepared.

## V. Demonstrative Processing Outcome

For a small synthetic dataset of this type, a successful demonstrative run may use the following parameters:

- k-anonymity value: `2`
- l-diversity value: `2`
- t-closeness value: `0.5`
- Result status: completed successfully
- Rows processed: 5

Additional run-specific values, including privacy score and processing time, are captured in the application-generated report associated with the session.

## VI. Privacy And Governance Features Illustrated

This exhibit demonstrates that the proposed platform is not limited to a narrow anonymization step. Instead, it combines multiple operational safeguards that are relevant to responsible use of sensitive data:

- structured identification of quasi-identifiers and sensitive attributes
- repeatable processing through an application workflow rather than undocumented scripts
- report generation documenting parameters and results
- controlled result delivery through authenticated access and signed downloads where supported
- retention-aware handling of original files, result files, and metadata
- deletion support consistent with data minimization principles

These features are important because privacy-preserving infrastructure in healthcare settings depends not only on technical transformation, but also on the existence of reproducible controls and documented handling practices.

## VII. Public Value And National Importance

This exhibit supports the national-importance aspect of the proposed endeavor because it shows a practical method for reducing barriers to healthcare research collaboration. Institutions across the United States increasingly depend on data for clinical analytics, operational study, public-interest research, and innovation. At the same time, privacy risk and governance burdens often limit safe reuse and exchange of structured datasets.

By providing a repeatable workflow for lower-risk data preparation, `Privatedec` contributes to safer research infrastructure. The value of such a system extends beyond any single employer or organization. A platform of this kind can be relevant to hospitals, universities, research groups, public-interest analytics teams, and other entities that need to prepare sensitive structured data in a more controlled and reproducible manner.

## VIII. Relevance To Mr. Kportufe's Proposed Endeavor

This exhibit is relevant because it shows that Mark Kportufe's proposed endeavor is already being advanced through an implemented software system with healthcare-relevant functionality. It demonstrates more than a general idea. It shows a functioning platform that combines technical privacy controls with secure handling, retention-aware governance, and evidence-style reporting.

Accordingly, this exhibit supports the position that Mr. Kportufe's endeavor has substantial merit, practical implementation, and broader public-facing value.

## IX. Suggested Supporting Materials

The following materials may be attached or cross-referenced with this exhibit:

- screenshot of the upload page
- screenshot of the session detail page showing selected quasi-identifiers and sensitive attributes
- screenshot of the processing page
- screenshot of the result page
- screenshot of the printable report page
- printed PDF copy of the generated report
- relevant project architecture documentation

## X. Suggested Exhibit Caption

Exhibit A demonstrates a working example of `Privatedec` being used to prepare a synthetic patient-style dataset for lower-risk healthcare research sharing through a repeatable workflow involving privacy parameter selection, controlled result delivery, and retention-aware governance.

