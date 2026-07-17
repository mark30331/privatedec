# Privatedec

Privatedec is a privacy-preserving data preparation platform for healthcare research, analytics, and responsible AI workflows. It helps teams transform sensitive structured datasets into lower-risk research assets through anonymization controls, controlled delivery, and retention-aware governance.

## Problem

Healthcare researchers and AI teams often need access to useful data, but privacy risk, governance requirements, and fear of re-identification make sensitive datasets difficult to share or reuse safely. Privatedec helps address this gap by providing a practical workflow for preparing lower-risk datasets for research, analytics, and responsible AI development.

## What Privatedec Does

- Securely uploads and validates structured CSV datasets for privacy-aware processing.
- Applies configurable anonymization controls such as k-anonymity, l-diversity, and t-closeness.
- Produces review-friendly outputs and evidence-style processing reports.
- Restricts access through authenticated sessions and signed result delivery.
- Reinforces trust with retention, security, privacy, and responsible AI policy pages.

## Live Demo

Privatedec is live at [app.privatedec.com](https://app.privatedec.com/), where it demonstrates a deployed privacy-preserving workflow for preparing sensitive structured datasets for healthcare research, analytics, and responsible AI data preparation.

## Security, Privacy, and Retention

Privatedec includes public-facing governance pages that explain how the platform approaches secure data handling, privacy transparency, and retention-aware deletion workflows.

- [Security](https://app.privatedec.com/security/)
- [Privacy](https://app.privatedec.com/privacy/)
- [Retention](https://app.privatedec.com/retention/)

## Intended Use

Privatedec is designed for privacy-aware data preparation workflows involving structured datasets. For demonstrations and testing, synthetic or appropriately de-identified data should be used instead of real patient information.

## Status

This project is an actively developed deployed MVP focused on privacy-preserving dataset preparation, governance visibility, and evidence-friendly reporting.

## Tech Stack

- Django
- PostgreSQL
- Redis
- Celery
- Cloudflare R2
- Bootstrap 5
- Render

## Screenshots

### Homepage
<img width="1920" height="926" alt="Screenshot (108)" src="https://github.com/user-attachments/assets/7e0172ac-2796-4b04-addd-58d5c7bc0d17" />

### Upload Workflow
<img width="1920" height="1021" alt="Screenshot (109)" src="https://github.com/user-attachments/assets/1bc6c5b2-3ce2-4d9a-b981-091c2ca30d54" />

<img width="1920" height="850" alt="Screenshot (112)" src="https://github.com/user-attachments/assets/8b398317-1992-4c5c-90e1-33f578a4e3e6" />

### Results and Reporting
<img width="1920" height="866" alt="Screenshot (111)" src="https://github.com/user-attachments/assets/7c7fc5dd-2eb8-4882-b240-9b7c089688aa" />

