# Privatedec Implementation Checklist

## 1. Foundation

- [x] Add `.gitignore`
- [ ] Stop tracking local `venv/`
- [x] Add `requirements/base.txt`
- [x] Add `requirements/dev.txt`
- [x] Add `requirements/prod.txt`
- [x] Add `.env.example`
- [x] Split settings into `base.py`, `local.py`, `production.py`
- [x] Add PostgreSQL config via environment variables
- [x] Add Celery config
- [x] Add Redis config
- [x] Add Cloudflare R2 config
- [x] Add Dockerfile
- [x] Add `docker-compose.yml`
- [x] Add Whitenoise config
- [x] Add `project/celery.py`

## 2. App Scaffolding

- [x] Create `apps/` package
- [x] Create `apps/core`
- [x] Create `apps/accounts`
- [x] Create `apps/uploads`
- [x] Create `apps/anonymization`
- [x] Create `apps/results`
- [x] Create `apps/evidence`
- [x] Register apps in Django settings

## 3. Authentication

- [x] Implement custom `User` model
- [x] Set `AUTH_USER_MODEL`
- [x] Create user manager
- [x] Add registration form/view/template
- [x] Add email verification token flow
- [x] Add login/logout pages
- [x] Add password reset pages
- [x] Add profile page
- [x] Add dashboard page
- [x] Restrict dashboard and upload pages to authenticated users

## 4. Base UI

- [x] Add Bootstrap 5 base template
- [x] Add navbar with auth-aware links
- [x] Add toast/message partial
- [x] Add home page
- [x] Add responsive layout conventions
- [x] Add Bootstrap Icons

## 5. Upload Flow

- [x] Create `UploadSession` model
- [x] Create `UploadSchema` model
- [x] Add upload form
- [x] Validate file extension and file size
- [x] Validate CSV readability
- [x] Detect encoding policy
- [x] Parse first rows with pandas
- [x] Infer columns and likely types
- [x] Save preview rows
- [x] Add quasi-identifier selection UI
- [x] Add sensitive attribute selection UI
- [x] Add `k`, `l`, `t` parameter validation
- [ ] Store original CSV in R2
- [x] Save upload session metadata

## 6. Anonymization Engine

- [ ] Define engine service interface
- [x] Add input validation service
- [ ] Implement CSV download from R2
- [x] Load DataFrame for processing
- [x] Implement k-anonymity step
- [x] Implement l-diversity step
- [x] Implement t-closeness step
- [ ] Add suppression/generalization behavior
- [x] Compute privacy score
- [x] Save anonymized CSV
- [ ] Upload result to R2
- [x] Create `AnonymizationRun` model
- [x] Save metrics and failure reasons

## 7. Async Processing

- [x] Add Celery app wiring
- [x] Create `anonymize_upload_session` task
- [x] Update session status transitions
- [x] Update progress checkpoints
- [ ] Add retry policy for transient failures
- [ ] Add worker startup command docs

## 8. Results Management

- [x] Add session history page
- [x] Add session detail page
- [x] Add processing page
- [x] Add status polling endpoint
- [x] Add result download endpoint
- [ ] Generate signed R2 URL
- [ ] Add delete session flow
- [ ] Delete R2 objects on session delete
- [x] Add status badges
- [x] Add result preview

## 9. Django Admin

- [x] Register `User` admin
- [x] Register `UploadSession` admin
- [x] Register `UploadSchema` admin
- [x] Register `AnonymizationRun` admin
- [x] Register `Testimonial` admin
- [x] Add useful admin filters/search

## 10. Evidence and Analytics

- [x] Create `UsageEvent` model
- [x] Record core product events
- [ ] Add Google Analytics template hook
- [ ] Add testimonial submission form
- [ ] Add testimonial moderation admin flow
- [ ] Add evidence report data aggregation helpers

## 11. Deployment

- [x] Add `/health/` endpoint
- [x] Add production security settings
- [x] Add Gunicorn command
- [ ] Add Railway deployment notes
- [ ] Add migration-on-deploy instructions
- [ ] Add static asset collection flow

## 12. Testing

- [ ] Add auth tests
- [ ] Add upload validation tests
- [ ] Add session ownership tests
- [ ] Add anonymization service tests
- [ ] Add download permission tests
- [ ] Add integration test for upload to completion flow
- [ ] Add malformed CSV test cases
- [ ] Add large-file sanity check

## 13. Suggested Execution Order

1. Foundation
2. App scaffolding
3. Authentication
4. Base UI
5. Upload flow
6. Anonymization engine
7. Async processing
8. Results management
9. Admin
10. Deployment
11. Evidence and analytics
12. Testing and polish
