import io
import os
import time
from decimal import Decimal

import pandas as pd
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils import timezone

from apps.evidence.models import UsageEvent
from apps.uploads.models import SessionStatus, UploadSession


def process_upload_session(session_id, task_id=""):
    session = (
        UploadSession.objects.select_related("schema", "anonymization_run", "user")
        .get(pk=session_id)
    )
    run = session.anonymization_run
    schema = session.schema

    _validate_processing_inputs(session)

    with transaction.atomic():
        session.status = SessionStatus.PROCESSING
        session.progress_percent = 5
        session.error_code = ""
        session.error_message = ""
        session.processing_started_at = timezone.now()
        session.processing_completed_at = None
        session.save(
            update_fields=[
                "status",
                "progress_percent",
                "error_code",
                "error_message",
                "processing_started_at",
                "processing_completed_at",
                "updated_at",
            ]
        )
        run.task_id = task_id or run.task_id
        run.failure_reason = ""
        run.save(update_fields=["task_id", "failure_reason", "updated_at"])

    UsageEvent.objects.create(user=session.user, session=session, event_type="JOB_STARTED")
    started_at = time.perf_counter()

    raw_bytes = _read_storage_bytes(session.stored_original_key)
    _update_progress(session, 15)

    data_frame = pd.read_csv(
        io.StringIO(raw_bytes.decode(session.encoding or "utf-8-sig")),
        sep=session.delimiter or ",",
    )
    _update_progress(session, 30)

    generalized_frame, group_ranges = _apply_group_generalization(
        data_frame,
        schema.quasi_identifier_columns_json,
        run.k_value,
    )
    _update_progress(session, 55)

    l_ok, l_metric = _evaluate_l_diversity(
        generalized_frame,
        group_ranges,
        schema.sensitive_columns_json,
        run.l_value,
    )
    t_ok, max_distance = _evaluate_t_closeness(
        generalized_frame,
        group_ranges,
        schema.sensitive_columns_json,
        float(run.t_value),
    )

    if not l_ok:
        raise ValidationError(
            f"l-diversity could not be satisfied. Minimum distinct sensitive values per group: {l_metric}."
        )
    if not t_ok:
        raise ValidationError(
            f"t-closeness could not be satisfied. Maximum group distance was {max_distance:.3f}."
        )

    _update_progress(session, 75)

    result_filename = _build_result_filename(session.original_filename)
    result_key = build_result_storage_key(session.user_id, session.pk, result_filename)
    csv_bytes = generalized_frame.to_csv(index=False).encode("utf-8")
    stored_result_key = default_storage.save(result_key, ContentFile(csv_bytes))
    _update_progress(session, 90)

    privacy_score = _calculate_privacy_score(
        minimum_group_size=min(len(group) for group in group_ranges),
        k_value=run.k_value,
        min_l_value=l_metric,
        target_l_value=run.l_value,
        max_distance=max_distance,
        target_t_value=float(run.t_value),
    )
    processing_time_ms = int((time.perf_counter() - started_at) * 1000)

    with transaction.atomic():
        session.status = SessionStatus.COMPLETED
        session.progress_percent = 100
        session.processing_completed_at = timezone.now()
        session.save(
            update_fields=[
                "status",
                "progress_percent",
                "processing_completed_at",
                "updated_at",
            ]
        )
        run.engine_name = "baseline-generalization"
        run.engine_version = "0.1"
        run.privacy_score = privacy_score
        run.rows_processed = int(len(generalized_frame.index))
        run.processing_time_ms = processing_time_ms
        run.result_filename = result_filename
        run.stored_result_key = stored_result_key
        run.result_row_count = int(len(generalized_frame.index))
        run.failure_reason = ""
        run.save()

    UsageEvent.objects.create(
        user=session.user,
        session=session,
        event_type="JOB_COMPLETED",
        metadata_json={"result_key": stored_result_key, "privacy_score": str(privacy_score)},
    )
    return session


def mark_processing_failure(session_id, reason):
    session = UploadSession.objects.select_related("anonymization_run", "user").get(pk=session_id)
    normalized_reason = _normalize_failure_reason(reason)
    session.status = SessionStatus.FAILED
    session.progress_percent = 100
    session.error_code = "PROCESSING_FAILED"
    session.error_message = normalized_reason
    session.processing_completed_at = timezone.now()
    session.save(
        update_fields=[
            "status",
            "progress_percent",
            "error_code",
            "error_message",
            "processing_completed_at",
            "updated_at",
        ]
    )
    session.anonymization_run.failure_reason = normalized_reason
    session.anonymization_run.save(update_fields=["failure_reason", "updated_at"])
    UsageEvent.objects.create(
        user=session.user,
        session=session,
        event_type="JOB_FAILED",
        metadata_json={"reason": normalized_reason},
    )


def build_result_storage_key(user_id, session_id, filename):
    safe_name = os.path.basename(filename)
    return f"uploads/{user_id}/{session_id}/result/{safe_name}"


def build_result_preview(session, limit=5):
    run = session.anonymization_run
    if not run.stored_result_key:
        return []

    raw_bytes = _read_storage_bytes(run.stored_result_key)
    data_frame = pd.read_csv(
        io.StringIO(raw_bytes.decode(session.encoding or "utf-8")),
        sep=session.delimiter or ",",
    )
    preview = data_frame.head(limit).where(pd.notnull(data_frame.head(limit)), "")
    return preview.to_dict(orient="records")


def _validate_processing_inputs(session):
    schema = session.schema
    run = session.anonymization_run
    if session.row_count < run.k_value:
        raise ValidationError("k-anonymity cannot exceed the number of rows in the uploaded CSV.")
    if not schema.quasi_identifier_columns_json:
        raise ValidationError("Select at least one quasi-identifier before processing.")
    if not schema.sensitive_columns_json:
        raise ValidationError("Select at least one sensitive attribute before processing.")


def _update_progress(session, value):
    UploadSession.objects.filter(pk=session.pk).update(progress_percent=value, updated_at=timezone.now())


def _read_storage_bytes(storage_key):
    with default_storage.open(storage_key, "rb") as stored_file:
        return stored_file.read()


def _apply_group_generalization(data_frame, quasi_columns, k_value):
    working = data_frame.copy().reset_index(drop=True)
    working = working.sort_values(by=quasi_columns, kind="mergesort").reset_index(drop=True)

    groups = []
    index = 0
    total_rows = len(working.index)
    while index < total_rows:
        remaining = total_rows - index
        if remaining < k_value and groups:
            groups[-1].extend(range(index, total_rows))
            break
        group_end = min(index + k_value, total_rows)
        groups.append(list(range(index, group_end)))
        index = group_end

    for group in groups:
        subset = working.iloc[group]
        for column in quasi_columns:
            replacement = _generalize_series(subset[column])
            working.loc[group, column] = replacement
    return working, groups


def _generalize_series(series):
    non_null = series.dropna()
    if non_null.empty:
        return "*"
    if pd.api.types.is_numeric_dtype(series):
        min_value = non_null.min()
        max_value = non_null.max()
        return str(min_value) if min_value == max_value else f"{min_value}-{max_value}"

    values = sorted(str(value) for value in non_null.astype(str).unique())
    if len(values) == 1:
        return values[0]
    return f"{values[0]}..{values[-1]}"


def _evaluate_l_diversity(data_frame, groups, sensitive_columns, l_value):
    minimum_distinct = None
    for group in groups:
        subset = data_frame.iloc[group]
        for column in sensitive_columns:
            distinct_count = int(subset[column].dropna().nunique())
            minimum_distinct = (
                distinct_count
                if minimum_distinct is None
                else min(minimum_distinct, distinct_count)
            )
    minimum_distinct = minimum_distinct or 0
    return minimum_distinct >= l_value, minimum_distinct


def _evaluate_t_closeness(data_frame, groups, sensitive_columns, t_value):
    if not sensitive_columns:
        return True, 0.0

    max_distance = 0.0
    for column in sensitive_columns:
        overall_distribution = _normalized_distribution(data_frame[column])
        for group in groups:
            group_distribution = _normalized_distribution(data_frame.iloc[group][column])
            categories = set(overall_distribution) | set(group_distribution)
            distance = sum(
                abs(group_distribution.get(category, 0.0) - overall_distribution.get(category, 0.0))
                for category in categories
            ) / 2
            max_distance = max(max_distance, distance)
    return max_distance <= t_value, max_distance


def _normalized_distribution(series):
    counts = series.astype(str).value_counts(normalize=True)
    return {str(key): float(value) for key, value in counts.items()}


def _calculate_privacy_score(
    minimum_group_size,
    k_value,
    min_l_value,
    target_l_value,
    max_distance,
    target_t_value,
):
    k_factor = min(1.0, minimum_group_size / max(k_value, 1))
    l_factor = min(1.0, min_l_value / max(target_l_value, 1))
    if target_t_value <= 0:
        t_factor = 1.0 if max_distance == 0 else 0.0
    else:
        t_factor = max(0.0, 1.0 - (max_distance / max(target_t_value, 0.001)) + 1.0)
        t_factor = min(1.0, t_factor)
    return Decimal(f"{((k_factor + l_factor + t_factor) / 3):.4f}")


def _build_result_filename(original_filename):
    name, ext = os.path.splitext(original_filename)
    return f"{name}-anonymized{ext or '.csv'}"


def _normalize_failure_reason(reason):
    if isinstance(reason, ValidationError):
        messages = reason.messages
    elif isinstance(reason, (list, tuple)):
        messages = [str(item) for item in reason]
    else:
        messages = [str(reason)]

    cleaned = " ".join(message.strip() for message in messages if str(message).strip())
    if not cleaned:
        return "Processing failed due to an unexpected error."

    lowered = cleaned.lower()
    if "t-closeness could not be satisfied" in lowered:
        return (
            f"{cleaned} Try increasing the t-closeness value, reducing the number of "
            "quasi-identifiers, or using a larger dataset."
        )
    if "l-diversity could not be satisfied" in lowered:
        return (
            f"{cleaned} Try lowering the l-diversity requirement, reducing the number of "
            "quasi-identifiers, or using a larger dataset."
        )

    return cleaned
