# NIW Case Study 2: Privacy-Preserving Dataset Preparation For Healthcare AI Training

Date: 2026-06-22  
Prepared by: Mark Kportufe  
Project: Privatedec

## 1. Scenario

This case study demonstrates how `Privatedec` can support preparation of a structured healthcare-style dataset before downstream analytics or AI model development. The central issue in this context is not only whether data is useful for training, but whether the preparation process itself includes appropriate privacy controls, governance steps, and reproducible documentation. The example below uses a synthetic dataset and is presented as an evidence exhibit for product capability and national-interest relevance.

## 2. Why It Matters

Healthcare AI systems depend on data. However, many organizations lack a practical workflow for preparing structured datasets in a way that both preserves analytical value and reduces privacy risk. In many real-world settings, data preparation still happens through informal scripts, spreadsheets, or one-off manual review. Those approaches create inconsistency, weak documentation, and unnecessary governance risk.

`Privatedec` helps address this by creating a controlled preparation layer before model training or analytics. In this context, the system contributes value by:

- identifying fields that increase re-identification risk
- applying privacy parameters in a repeatable workflow
- generating evidence that documents what processing occurred
- supporting controlled download and retention behavior after the dataset is produced

This is significant because responsible AI development in healthcare begins with responsible data handling.

## 3. Input Dataset Summary

For the purposes of this exhibit, the AI preparation workflow uses the same synthetic patient-style dataset included in the repository:

- source file: `docs/sample-upload.csv`
- dataset type: synthetic structured healthcare-style CSV
- rows: 5
- columns: 4
- fields: `name`, `age`, `zipcode`, `diagnosis`
- direct identifier requiring removal or transformation: `name`
- quasi-identifiers selected: `age`, `zipcode`
- sensitive attribute selected: `diagnosis`

In an AI preparation context, the goal is to preserve medically or analytically meaningful patterns while lowering the risk that a training dataset contains readily linkable records.

## 4. Privatedec Workflow

The workflow for this exhibit is as follows:

1. Upload the structured CSV into `Privatedec`.
2. Review the schema, detected columns, and preview rows.
3. Select `age` and `zipcode` as quasi-identifiers because they can contribute to linkage risk.
4. Select `diagnosis` as the sensitive field because it carries health-related content.
5. Configure privacy parameters suited to a small demonstrative dataset.
6. Execute anonymization as a background process.
7. Review the system-generated report, including status, parameters, and preview.
8. Download the processed result through the controlled result-delivery path.
9. Maintain governance by using retention and deletion policies after processing.

This case study is useful because it demonstrates that AI training readiness is not just about making a dataset available. It is about preparing a lower-risk dataset through a governed, reproducible workflow.

## 5. Output And Controls

For a small synthetic dataset such as this one, a practical successful run can use:

- k value: `2`
- l value: `2`
- t value: `0.5`
- result status: completed successfully
- rows processed: 5
- privacy score: recorded in the generated processing report
- processing time: recorded in the generated processing report
- retention settings: separate retention windows for original upload, anonymized result, and session metadata
- secure delivery method: authenticated result access with signed file delivery when supported by configured storage

In an AI-governance context, the report is especially important because it documents how the training candidate dataset was prepared rather than relying on undocumented preprocessing.

## 6. Before / After Summary

Before processing, the dataset contains a direct identifier and linkable demographic-style attributes. Even in a small illustrative sample, those fields show why raw structured data should not be passed directly into downstream analytics or model development without review.

After processing:

- direct identifying exposure is reduced as the workflow shifts focus away from raw identifiers
- quasi-identifiers are generalized to reduce record-level linkability
- diagnostic content remains available in a form better suited for cohort-level or classification-style analysis
- the system records the selected parameters and outcome in a report that can be attached to governance documentation
- retention and controlled download features help reduce unnecessary long-term storage and uncontrolled redistribution

This matters because healthcare AI programs need not only data utility, but also a documented preparation process that shows diligence, repeatability, and governance awareness.

## 7. Why This Supports National Importance

This case study strengthens the NIW argument because it ties `Privatedec` directly to responsible AI development in healthcare, an area of growing national importance. The United States increasingly depends on data-driven healthcare tools, but those tools require careful upstream data preparation to reduce privacy risk and support trustworthy use. A system that helps organizations create lower-risk structured datasets while documenting the preparation process can contribute to safer and more scalable innovation.

The case study also demonstrates that Mark Kportufe's endeavor is broader than a narrow business application. It addresses a national challenge at the intersection of healthcare data governance, analytics, and AI readiness. By building practical infrastructure for privacy-preserving dataset preparation, the endeavor can support research institutions, healthcare organizations, and innovation teams across the country.

## 8. Exhibits To Attach

- screenshot of upload and schema review
- screenshot of session detail with selected quasi-identifiers and sensitive attributes
- screenshot of processing status
- screenshot of result detail
- screenshot of printable report
- printed PDF report showing parameters and retention details
- optional screenshot of legal, security, and retention pages to show governance-oriented design

## 9. Suggested Caption For Petition Use

This exhibit demonstrates how `Privatedec` can be used as a privacy-preserving preparation layer before healthcare analytics or AI training by combining structured anonymization, reproducible reporting, controlled result delivery, and retention-aware governance.

