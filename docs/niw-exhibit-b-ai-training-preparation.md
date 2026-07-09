# Exhibit B

## Demonstrative Use Of `Privatedec` For Privacy-Preserving Preparation Of Healthcare Data For AI And Advanced Analytics

Prepared for NIW evidence assembly  
Prepared by: Mark Kportufe  
Date: 2026-06-22

Note: This exhibit is based on a synthetic dataset and is intended to illustrate the implemented functionality and public significance of the proposed endeavor. It is not offered as a legal opinion or as a claim that any specific output satisfies all compliance requirements in every context.

## I. Purpose Of This Exhibit

This exhibit demonstrates how `Privatedec` can function as a privacy-preserving preparation layer before downstream healthcare analytics or AI-related use. It is offered to show that Mark Kportufe's proposed endeavor addresses a nationally important problem at the intersection of healthcare data governance, analytics, and responsible artificial intelligence.

In particular, this exhibit illustrates that `Privatedec` is designed not merely to transform data, but to create a governed workflow for preparing lower-risk datasets through structured privacy controls, reproducible reporting, controlled result delivery, and retention-aware handling.

## II. Scenario Presented

Healthcare AI and advanced analytics depend on access to structured data. However, raw datasets may contain direct identifiers or linkable combinations of demographic fields that make them unsuitable for downstream use without further preparation. In practice, many institutions still rely on inconsistent scripts, manual review, or undocumented preprocessing, which creates avoidable governance and privacy risk.

The scenario presented in this exhibit is a representative one: a healthcare-related dataset is being prepared for possible analytical or AI use, and the organization needs a documented process that reduces privacy risk while preserving meaningful utility for cohort-level or classification-oriented tasks.

## III. Demonstrative Dataset

This exhibit uses the same synthetic sample dataset included in the project repository.

- Source file: `docs/sample-upload.csv`
- Dataset type: synthetic structured healthcare-style CSV
- Number of rows: 5
- Number of columns: 4
- Included fields: `name`, `age`, `zipcode`, `diagnosis`
- Direct identifier requiring removal or transformation: `name`
- Quasi-identifiers selected in the workflow: `age`, `zipcode`
- Sensitive attribute selected in the workflow: `diagnosis`

The simplified nature of the dataset does not diminish the importance of the workflow shown here. The objective is to demonstrate the architecture and process by which sensitive structured data can be prepared in a more controlled manner before downstream analytical use.

## IV. Workflow Demonstrated By `Privatedec`

This exhibit reflects the following workflow:

1. A user uploads the structured CSV dataset into `Privatedec`.
2. The application analyzes the file and displays schema and preview information.
3. The user marks `age` and `zipcode` as quasi-identifiers because those fields may contribute to linkage risk.
4. The user marks `diagnosis` as the sensitive field.
5. The user configures privacy parameters suited to the size and nature of the demonstrative dataset.
6. The system performs anonymization through an asynchronous processing pipeline.
7. The application generates a result view and a printable report documenting the processing outcome.
8. The user accesses the processed file through an authenticated result workflow, with signed delivery where supported by the configured storage backend.
9. The application supports data minimization through retention-aware handling and deletion controls.

This workflow is relevant to responsible AI and analytics because it creates a documented preparation stage rather than allowing sensitive data to flow into downstream systems without traceable governance.

## V. Demonstrative Processing Outcome

For a small synthetic dataset of this kind, a successful demonstrative run may use:

- k-anonymity value: `2`
- l-diversity value: `2`
- t-closeness value: `0.5`
- Result status: completed successfully
- Rows processed: 5

Additional session-specific metrics, including privacy score and processing time, are recorded in the associated application report.

## VI. Privacy, Governance, And AI-Readiness Features Illustrated

This exhibit demonstrates several capabilities that are particularly relevant to responsible healthcare AI and analytics:

- identification of fields that increase re-identification risk
- application of privacy-preserving processing within a repeatable user workflow
- generation of reports documenting selected parameters and results
- controlled access to resulting files
- retention-aware treatment of original and processed data
- support for later deletion consistent with data minimization principles

These capabilities are important because AI readiness is not solely a matter of model architecture or downstream performance. It also depends on whether the source data was prepared through a disciplined process that reduces risk and creates a clear record of handling.

## VII. Public Value And National Importance

This exhibit supports the argument that the proposed endeavor has national importance because it addresses a growing need in the United States: enabling responsible use of healthcare data for advanced analytics and artificial intelligence without relying on unsafe or poorly documented handling practices. As healthcare innovation becomes more data dependent, systems that help organizations create lower-risk datasets in a reproducible way become more important to research capacity, operational analytics, and trustworthy technological development.

The public value of this endeavor is not confined to one employer or one commercial use. A platform like `Privatedec` may be relevant to hospitals, universities, research institutions, privacy-conscious analytics teams, and organizations exploring responsible AI applications involving sensitive structured data. By improving the process by which such data is prepared, the endeavor contributes to a broader national need.

## VIII. Relevance To Mr. Kportufe's Proposed Endeavor

This exhibit demonstrates that Mark Kportufe's proposed endeavor is already being advanced through an implemented platform with concrete privacy, governance, and reporting functionality. It reflects a technical effort that combines software engineering, cloud-based delivery, anonymization workflow design, and policy-aware controls in a manner directly relevant to healthcare data use and responsible AI preparation.

For that reason, this exhibit supports the conclusion that Mr. Kportufe's endeavor has practical substance, broader public value, and a direct connection to nationally important work involving healthcare data governance and innovation.

## IX. Suggested Supporting Materials

The following items may be attached or cross-referenced with this exhibit:

- screenshot of upload and schema review
- screenshot of session detail with selected quasi-identifiers and sensitive attributes
- screenshot of processing status
- screenshot of result detail
- screenshot of the printable report
- printed PDF copy of the generated report
- screenshots of the legal, security, and retention pages showing governance-oriented design

## X. Suggested Exhibit Caption

Exhibit B demonstrates a working example of `Privatedec` being used as a privacy-preserving preparation layer for healthcare analytics or AI-related use through structured anonymization, reproducible reporting, controlled result delivery, and retention-aware governance.

