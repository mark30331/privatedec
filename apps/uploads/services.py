import csv
import io
import os

import pandas as pd
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def analyze_csv_upload(uploaded_file):
    raw_bytes = uploaded_file.read()
    if not raw_bytes:
        raise ValidationError("The uploaded CSV file is empty.")

    encoding = _detect_encoding(raw_bytes)
    decoded_text = raw_bytes.decode(encoding)
    sample = decoded_text[:4096]
    delimiter = _detect_delimiter(sample)

    try:
        data_frame = pd.read_csv(io.StringIO(decoded_text), sep=delimiter)
    except Exception as exc:
        raise ValidationError(f"Unable to read the uploaded CSV file: {exc}") from exc

    if data_frame.empty:
        raise ValidationError("The uploaded CSV has no data rows.")
    if len(data_frame.columns) == 0:
        raise ValidationError("The uploaded CSV does not contain any columns.")

    data_frame = data_frame.where(pd.notnull(data_frame), None)
    preview_frame = data_frame.head(5)

    return {
        "raw_bytes": raw_bytes,
        "encoding": encoding,
        "delimiter": delimiter,
        "row_count": int(len(data_frame.index)),
        "column_count": int(len(data_frame.columns)),
        "columns": [str(column) for column in data_frame.columns.tolist()],
        "types": {str(column): str(dtype) for column, dtype in data_frame.dtypes.items()},
        "preview_rows": _serialize_rows(preview_frame),
        "column_stats": _calculate_column_stats(data_frame),
    }


def build_original_storage_key(user_id, session_id, filename):
    safe_name = os.path.basename(filename)
    return f"uploads/{user_id}/{session_id}/original/{safe_name}"


def persist_original_upload(storage_key, raw_bytes):
    return default_storage.save(storage_key, ContentFile(raw_bytes))


def _detect_encoding(raw_bytes):
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            raw_bytes.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    raise ValidationError("The CSV file must be UTF-8 encoded.")


def _detect_delimiter(sample):
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        return ","


def _serialize_rows(data_frame):
    rows = []
    for row in data_frame.to_dict(orient="records"):
        rows.append(
            {
                str(key): "" if value is None else str(value)
                for key, value in row.items()
            }
        )
    return rows


def _calculate_column_stats(data_frame):
    stats = {}
    for column in data_frame.columns:
        series = data_frame[column]
        non_null = series.dropna()
        column_stats = {
            "unique_count": int(non_null.nunique()),
            "non_null_count": int(non_null.shape[0]),
        }
        if not non_null.empty:
            if pd.api.types.is_numeric_dtype(series):
                column_stats["min"] = _serialize_scalar(non_null.min())
                column_stats["max"] = _serialize_scalar(non_null.max())
            else:
                column_stats["sample_values"] = [
                    _serialize_scalar(value) for value in non_null.astype(str).unique()[:5]
                ]
        stats[str(column)] = column_stats
    return stats


def _serialize_scalar(value):
    if value is None:
        return ""
    if hasattr(value, "item"):
        value = value.item()
    return str(value)
