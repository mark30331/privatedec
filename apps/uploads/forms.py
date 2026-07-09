from decimal import Decimal

from django import forms
from django.conf import settings


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(
        label="CSV file",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv"}),
    )
    k_value = forms.IntegerField(
        min_value=2,
        initial=2,
        label="k-anonymity",
        help_text="Minimum group size. Higher values increase privacy but may reduce utility.",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "2", "step": "1"}),
    )
    l_value = forms.IntegerField(
        min_value=2,
        initial=2,
        label="l-diversity",
        help_text="Minimum distinct sensitive values per group. Small datasets often require lower l.",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "2", "step": "1"}),
    )
    t_value = forms.DecimalField(
        min_value=Decimal("0"),
        max_value=Decimal("1"),
        decimal_places=3,
        initial=Decimal("0.200"),
        label="t-closeness",
        help_text="Distance threshold between each group and the overall distribution (0–1). If processing fails on a small dataset, try 0.4–0.7.",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": "0", "max": "1", "step": "0.05"}
        ),
    )

    def clean_csv_file(self):
        uploaded_file = self.cleaned_data["csv_file"]
        filename = uploaded_file.name.lower()
        if not filename.endswith(".csv"):
            raise forms.ValidationError("Upload a CSV file with a .csv extension.")
        if uploaded_file.size > settings.CSV_MAX_UPLOAD_BYTES:
            raise forms.ValidationError(
                f"CSV files must be {settings.CSV_MAX_UPLOAD_MB} MB or smaller."
            )
        return uploaded_file


class ColumnSelectionForm(forms.Form):
    quasi_identifier_columns = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Quasi-identifiers",
    )
    sensitive_columns = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Sensitive attributes",
    )

    def __init__(self, *args, columns=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(column, column) for column in (columns or [])]
        self.fields["quasi_identifier_columns"].choices = choices
        self.fields["sensitive_columns"].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        quasi_identifiers = set(cleaned_data.get("quasi_identifier_columns", []))
        sensitive_columns = set(cleaned_data.get("sensitive_columns", []))
        overlap = sorted(quasi_identifiers & sensitive_columns)
        if overlap:
            raise forms.ValidationError(
                "Columns cannot be both quasi-identifiers and sensitive attributes: "
                + ", ".join(overlap)
            )
        return cleaned_data
