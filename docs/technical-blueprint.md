# Privatedec Technical Blueprint

## 1. Purpose

Privatedec is a Django-based web application that lets authenticated users upload CSV datasets, configure anonymization parameters, run privacy-preserving transformations asynchronously, and download anonymized results. The product is intended to demonstrate a credible, evidence-backed privacy tool suitable for NIW petition support.

This blueprint defines the initial production architecture, application boundaries, data model, request flows, infrastructure integrations, testing strategy, and implementation order.

## 2. Current State

The current repository is a minimal Django scaffold with:

- `manage.py`
- `project/settings.py`
- `project/urls.py`
- `project/asgi.py`
- `project/wsgi.py`
- `db.sqlite3`

There are no custom apps, no dependency manifest, no deployment files, no environment configuration, and no production-grade settings split.

## 3. Product Goals

### 3.1 Primary Goals

- Allow user registration, login, verification, and profile management.
- Accept CSV uploads up to 50 MB.
- Detect schema and preview uploaded data safely.
- Let users choose quasi-identifiers and sensitive attributes.
- Run k-anonymity, l-diversity, and t-closeness processing asynchronously.
- Store original and anonymized files in Cloudflare R2.
- Present job status, metrics, and secure result downloads.
- Produce supporting operational evidence, analytics, screenshots, and documentation.

### 3.2 Non-Goals for Initial MVP

- Real-time websocket infrastructure.
- Multi-tenant organization accounts.
- API-first headless architecture.
- Fine-grained RBAC beyond guest/authenticated/admin separation.
- Complex collaborative workflows.

## 4. Guiding Principles

- Prefer server-rendered Django pages for speed of delivery and maintainability.
- Keep privacy processing out of request/response threads.
- Use database state as the source of truth for UI status.
- Encapsulate infrastructure dependencies behind service modules.
- Design the anonymization engine as a replaceable adapter layer.
- Build for production deployment from the start, even if some features are deferred.

## 5. Chosen Stack

### 5.1 Application Stack

- Python 3.11+
- Django 5.2.x
- Bootstrap 5
- Bootstrap Icons
- PostgreSQL
- Celery
- Redis
- pandas
- django-storages
- boto3
- Whitenoise
- Gunicorn
- Docker / Docker Compose

### 5.2 Recommended Python Dependencies

- `Django==5.2.*`
- `psycopg[binary]`
- `django-environ`
- `celery`
- `redis`
- `pandas`
- `django-storages`
- `boto3`
- `gunicorn`
- `whitenoise`
- `python-dateutil`
- `openpyxl` only if spreadsheet export becomes necessary later

### 5.3 Optional Dependencies

- `django-allauth` if email verification/auth flows need accelerated delivery
- `pytest`, `pytest-django`, `factory-boy` for test ergonomics
- `sentry-sdk` for production error reporting

## 6. High-Level Architecture

Privatedec will use a modular monolith design:

- Django handles views, forms, templates, auth, admin, and ORM.
- PostgreSQL stores users, upload sessions, schema metadata, anonymization runs, and evidence metrics.
- Cloudflare R2 stores original and anonymized CSV files.
- Celery workers process anonymization jobs asynchronously.
- Redis serves as the Celery broker.
- Bootstrap templates render the UI.
- Lightweight polling updates job status on processing/history/detail pages.

### 6.1 Logical Layers

- Presentation layer: Django templates, forms, views, messages, polling endpoints.
- Domain layer: models, services, validation, anonymization orchestration.
- Infrastructure layer: storage adapters, email delivery, analytics hooks, Celery integration.
- Operations layer: Docker, Railway deployment, health checks, logging, metrics.

## 7. Proposed Project Structure

```text
privatedec/
  manage.py
  requirements/
    base.txt
    dev.txt
    prod.txt
  docs/
    technical-blueprint.md
    implementation-checklist.md
  .env.example
  .gitignore
  Dockerfile
  docker-compose.yml
  project/
    __init__.py
    asgi.py
    celery.py
    urls.py
    wsgi.py
    settings/
      __init__.py
      base.py
      local.py
      production.py
  apps/
    accounts/
    core/
    uploads/
    anonymization/
    results/
    evidence/
```

### 7.1 App Responsibilities

#### `apps.core`

- Home page
- Dashboard shell
- Shared template helpers
- Health endpoint
- Shared constants and utility helpers

#### `apps.accounts`

- Custom user model
- Registration
- Login/logout integration
- Email verification
- Password reset views/templates
- Profile management

#### `apps.uploads`

- UploadSession lifecycle
- File validation
- CSV preview and schema inference
- Parameter collection UI
- Original file persistence to R2

#### `apps.anonymization`

- Anonymization service interface
- Job orchestration
- Celery tasks
- Progress updates
- Metrics capture
- Error handling and retry policy

#### `apps.results`

- History list
- Session detail page
- Secure signed download
- Delete session and file cleanup
- Result preview

#### `apps.evidence`

- Usage metrics
- Testimonials
- Analytics integration hooks
- Evidence report helpers

## 8. Settings Architecture

Replace the single `project/settings.py` with a settings package:

- `project/settings/base.py`
- `project/settings/local.py`
- `project/settings/production.py`

### 8.1 Base Settings

- Shared installed apps and middleware
- Template configuration
- Auth settings
- Static/media defaults
- Celery namespace
- Logging configuration
- App-level constants

### 8.2 Local Settings

- `DEBUG = True`
- Local PostgreSQL or SQLite fallback only for early bootstrapping
- Console email backend
- Local static serving

### 8.3 Production Settings

- `DEBUG = False`
- Whitenoise
- secure cookies
- HTTPS redirects
- trusted origins
- R2 storage backend
- PostgreSQL from environment
- SMTP provider config

### 8.4 Environment Variables

At minimum:

- `DJANGO_SETTINGS_MODULE`
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `DEFAULT_FROM_EMAIL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`
- `R2_ENDPOINT_URL`
- `R2_PUBLIC_BASE_URL`
- `GOOGLE_ANALYTICS_ID`

## 9. Authentication Design

### 9.1 User Model

Use a custom user model at project start:

- `email` as unique identifier
- `affiliation` as optional or required based on product policy
- `first_name`
- `last_name`
- `is_email_verified`
- `is_staff`
- `is_active`
- `date_joined`
- `updated_at`

Set:

- `AUTH_USER_MODEL = "accounts.User"`

### 9.2 Auth Flows

- Registration creates an inactive or unverified account.
- Verification email includes a signed token link.
- Login is allowed only after verification if enforcement is enabled.
- Password reset uses Django built-in token flow.
- Profile page lets users update personal information and password.

### 9.3 Access Control

- Guests can see marketing pages and auth pages.
- Authenticated users can upload files and access only their own sessions/results.
- Admin users can access the Django admin for all operational records.

## 10. Data Model

### 10.1 `accounts.User`

- `id`
- `email`
- `affiliation`
- `first_name`
- `last_name`
- `is_email_verified`
- `is_staff`
- `is_active`
- `date_joined`
- `updated_at`

### 10.2 `uploads.UploadSession`

Represents one uploaded source dataset and the job lifecycle around it.

Fields:

- `id`
- `user` -> `accounts.User`
- `original_filename`
- `stored_original_key`
- `content_type`
- `file_size_bytes`
- `encoding`
- `delimiter`
- `row_count`
- `column_count`
- `status`
- `progress_percent`
- `error_code`
- `error_message`
- `created_at`
- `updated_at`
- `processing_started_at`
- `processing_completed_at`

Status enum:

- `PENDING`
- `VALIDATING`
- `READY`
- `PROCESSING`
- `COMPLETED`
- `FAILED`
- `DELETED`

### 10.3 `uploads.UploadSchema`

Stores inferred schema and user selections for a session.

Fields:

- `id`
- `session` -> `uploads.UploadSession` one-to-one
- `detected_columns_json`
- `detected_types_json`
- `quasi_identifier_columns_json`
- `sensitive_columns_json`
- `preview_rows_json`
- `column_stats_json`
- `created_at`
- `updated_at`

### 10.4 `anonymization.AnonymizationRun`

Stores the anonymization parameters and execution results.

Fields:

- `id`
- `session` -> `uploads.UploadSession`
- `engine_name`
- `engine_version`
- `k_value`
- `l_value`
- `t_value`
- `suppression_placeholder`
- `privacy_score`
- `rows_processed`
- `suppressed_rows`
- `suppressed_cells`
- `processing_time_ms`
- `result_filename`
- `stored_result_key`
- `result_row_count`
- `task_id`
- `failure_reason`
- `created_at`
- `updated_at`

### 10.5 `evidence.Testimonial`

- `id`
- `user` -> `accounts.User`
- `rating`
- `title`
- `body`
- `is_approved`
- `created_at`
- `updated_at`

### 10.6 `evidence.UsageEvent`

Tracks evidence and operational metrics.

Fields:

- `id`
- `user` nullable
- `event_type`
- `session` nullable
- `metadata_json`
- `created_at`

Event examples:

- `USER_REGISTERED`
- `EMAIL_VERIFIED`
- `UPLOAD_CREATED`
- `UPLOAD_VALIDATED`
- `JOB_STARTED`
- `JOB_COMPLETED`
- `JOB_FAILED`
- `RESULT_DOWNLOADED`

## 11. File Storage Design

### 11.1 Storage Rules

- Original uploads are stored in R2 immediately after validation.
- Anonymized outputs are stored in a separate namespace/prefix.
- Local disk is used only for temporary processing if needed.

### 11.2 Proposed Object Key Layout

```text
uploads/{user_id}/{session_id}/original/{filename}
uploads/{user_id}/{session_id}/result/{filename}
uploads/{user_id}/{session_id}/artifacts/{artifact_name}
```

### 11.3 Signed Downloads

- Downloads must use short-lived signed URLs.
- The app must verify the requesting user owns the session before generating the URL.
- Deleted sessions must revoke logical access even if the object still exists temporarily.

## 12. Upload and Validation Flow

### 12.1 User Flow

1. User opens upload page.
2. User drags or selects a CSV file.
3. Form validates file type, size, and anonymization parameters.
4. Server inspects encoding and basic CSV readability.
5. pandas reads a sample for preview and column inference.
6. User confirms quasi-identifiers and sensitive attributes.
7. System creates `UploadSession` and `UploadSchema`.
8. Original file is stored in R2.
9. User starts anonymization.
10. Celery task runs asynchronously.

### 12.2 Validation Rules

- File extension must be `.csv`.
- MIME type is advisory only; content parsing is authoritative.
- Max file size: `50 MB`.
- Encoding must decode as UTF-8 or a controlled fallback policy must be defined.
- Header row must exist.
- `k >= 2`
- `l >= 2`
- `0 <= t <= 1`
- `k <= row_count`
- quasi-identifier and sensitive column selections must exist in detected columns.
- quasi-identifier and sensitive columns should not overlap unless explicitly permitted by policy.

### 12.3 Preview Rules

- Show first 5 rows only.
- Truncate very long cell values in UI.
- Never render raw HTML from CSV content.

## 13. Anonymization Engine Design

### 13.1 Engine Abstraction

Create an internal service contract:

```python
class AnonymizationEngine:
    def validate_inputs(...)
    def anonymize(...)
    def calculate_privacy_score(...)
```

This allows the first implementation to use a selected library or custom pandas logic while preserving future replaceability.

### 13.2 Processing Pipeline

1. Download original file from R2.
2. Load CSV into pandas DataFrame.
3. Validate columns and parameters again.
4. Apply k-anonymity transformation.
5. Apply l-diversity checks.
6. Apply t-closeness checks.
7. Suppress or generalize violating records where necessary.
8. Compute privacy score and operational metrics.
9. Save anonymized CSV locally/temp.
10. Upload result to R2.
11. Persist `AnonymizationRun`.
12. Update `UploadSession.status` and progress.

### 13.3 Privacy Score

Initial privacy score can be a bounded heuristic from 0 to 1 based on:

- success of selected constraints
- amount of suppression
- distribution retention
- percentage of rows preserved

The exact scoring formula should be documented in code comments and surfaced in the detail page.

### 13.4 Error Handling

Expected failures:

- unreadable CSV
- invalid encoding
- missing columns
- parameter mismatch
- engine failure
- R2 download/upload failure
- worker timeout

User-facing errors should be concise; detailed traces should go to logs.

## 14. Async Processing Design

### 14.1 Celery Task

Primary task:

- `anonymization.tasks.anonymize_upload_session(session_id: str)`

### 14.2 Task Behavior

- Load session and lock processing state.
- Set status to `PROCESSING`.
- Update progress milestones at deterministic checkpoints.
- Retry transient storage/network failures.
- Mark session `COMPLETED` or `FAILED`.

### 14.3 Retry Policy

- Retry only transient failures.
- Use exponential backoff.
- Do not retry validation failures.

### 14.4 Progress Model

Suggested checkpoints:

- `5`: task accepted
- `15`: file downloaded
- `30`: CSV loaded
- `50`: anonymization running
- `70`: privacy metrics computed
- `85`: result uploaded
- `100`: database finalized

## 15. UI and Page Map

### 15.1 Public Pages

- `/` home page
- `/accounts/login/`
- `/accounts/register/`
- `/accounts/password-reset/`

### 15.2 Authenticated Pages

- `/dashboard/`
- `/upload/`
- `/sessions/`
- `/sessions/<uuid>/`
- `/sessions/<uuid>/processing/`
- `/profile/`

### 15.3 AJAX / Lightweight Endpoints

- `/sessions/<uuid>/status/`
- `/sessions/<uuid>/download/`
- `/sessions/<uuid>/delete/`

### 15.4 UI Design Rules

- Bootstrap 5 layout with responsive grid.
- Toast notifications via Django messages plus small JS helper.
- Processing page auto-polls until terminal state.
- Status badges use consistent color mapping.
- All forms display inline validation errors.

## 16. Django Admin Design

### 16.1 Admin Modules

- User admin with email verification visibility
- UploadSession admin with filters by status and user
- AnonymizationRun admin with metrics visibility
- Testimonial admin with approval actions

### 16.2 Useful Filters

- session status
- creation date
- completion date
- user email
- rating
- approval state

## 17. Logging and Monitoring

### 17.1 Logging Targets

- console logging in development
- structured stdout logging in production
- optional external error aggregation later

### 17.2 Log Events

- registration/verification events
- upload start/validation success/failure
- task start/progress/completion/failure
- R2 failures
- download generation
- delete operations

### 17.3 Health Check

Endpoint:

- `/health/`

Checks:

- Django process alive
- database reachable
- Redis reachable if enabled

## 18. Security Requirements

- Use `SECRET_KEY` from environment only.
- Enforce CSRF protection on all forms.
- Use Django auth/session middleware.
- Restrict result access to owner/admin only.
- Sanitize template rendering for preview data.
- Use signed download URLs with short expiration.
- Enable secure cookie flags in production.
- Use HTTPS-only deployment.
- Validate uploaded file size and content before persistence.

## 19. Deployment Architecture

### 19.1 Local Development

Docker Compose services:

- `web`
- `db`
- `redis`

Optional:

- `worker`

### 19.2 Production on Railway

Recommended services:

- Django web service
- Celery worker service
- PostgreSQL service
- Redis service

Cloudflare R2 remains external.

### 19.3 Production Process Model

- Web: `gunicorn project.wsgi`
- Worker: `celery -A project worker -l info`
- Release command: `python manage.py migrate`

## 20. Testing Strategy

### 20.1 Unit Tests

- user model and manager
- upload validation
- schema detection
- anonymization service validation
- storage service helpers

### 20.2 View Tests

- auth flows
- upload flow
- session ownership restrictions
- download permission checks

### 20.3 Integration Tests

- register -> verify -> login
- upload -> preview -> queue -> completed
- result download
- delete session cleanup

### 20.4 Operational Checks

- CSV near 50 MB
- malformed CSV
- unicode edge cases
- failed worker path
- R2 unavailable path

## 21. Evidence Collection Plan

### 21.1 Built-In Evidence

- usage event table
- testimonial submissions
- analytics pageview hooks
- result completion counts

### 21.2 Manual Evidence Artifacts

- screenshots of major pages
- short demo video
- README and setup guide
- implementation blog post
- evidence report assembled from metrics

## 22. Phase-to-Implementation Mapping

### Phase 1: Foundation

- repo hygiene
- settings split
- dependency manifests
- PostgreSQL
- Docker / Compose
- Celery / Redis setup
- R2 config

### Phase 2: Authentication

- custom user model
- registration
- verification
- login/logout
- password reset
- profile
- dashboard shell

### Phase 3: Upload System

- upload form
- drag-and-drop UI
- validation
- preview
- schema detection
- parameter forms
- R2 original file storage

### Phase 4: Anonymization Engine

- service contract
- concrete engine implementation
- metrics
- suppression behavior
- error mapping

### Phase 5: Async Processing

- Celery task
- status transitions
- progress polling
- retry policy

### Phase 6: Results Management

- history page
- detail page
- signed download
- delete flow
- status badges

### Phase 7: User Interface

- base layout
- home page
- upload page
- processing page
- result page
- history page
- profile and auth pages

### Phase 8: Admin

- model admin registration
- search, filters, actions

### Phase 9: Evidence

- analytics
- testimonials
- evidence reporting

### Phase 10: Deployment

- Dockerfile
- Compose
- production settings
- Whitenoise
- Gunicorn
- Railway deploy

### Phase 11: Testing

- unit, view, integration, performance, security checks

## 23. MVP Boundary

The initial implementation should include:

- all Phase 1 must-haves
- all Phase 2 must-haves
- Phase 3 must-haves except optional progress percentage polish
- core Phase 4 anonymization pipeline
- essential Phase 5 async processing
- essential Phase 6 results/history/download
- essential Phase 7 UI pages
- core Phase 8 admin
- core Phase 10 deployment
- core Phase 11 security/logging/tests

Deferred until after MVP if time is constrained:

- testimonial moderation workflow
- PDF export report
- before/after comparison view
- dark mode
- advanced search/filter history
- demo/evidence extras beyond basic metrics

## 24. Implementation Sequencing

### Iteration 1

- repo cleanup
- settings package
- dependency files
- Docker baseline
- custom user model

### Iteration 2

- auth views/templates
- dashboard
- base UI

### Iteration 3

- upload model/form/view
- CSV validation and preview
- schema detection
- R2 original file storage

### Iteration 4

- anonymization service layer
- Celery + Redis
- processing page and status polling

### Iteration 5

- results pages
- signed download
- delete flow
- admin

### Iteration 6

- docs
- analytics hooks
- tests
- deployment hardening

## 25. Immediate Next Implementation Tasks

1. Add dependency manifests and `.gitignore`.
2. Convert settings to package-based config.
3. Create `apps` package and scaffold `core`, `accounts`, `uploads`, `anonymization`, `results`, and `evidence`.
4. Add custom user model and initial migrations.
5. Configure PostgreSQL, Celery, Redis, Whitenoise, and R2 placeholders.
6. Add base templates and URL routing skeleton.

## 26. Open Decisions Locked for Implementation

Unless revised during review, implementation will proceed with these choices:

- Django 5.2.x instead of downgrading to 5.0
- custom user model with email login
- server-rendered Bootstrap UI
- PostgreSQL as the default database target
- Cloudflare R2 via `django-storages`
- Celery + Redis for background processing
- modular monolith structure under `apps/`
- database-driven polling instead of websockets
