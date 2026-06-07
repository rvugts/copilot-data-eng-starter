"""Small utilities for data pipeline configuration and naming conventions."""

from __future__ import annotations

import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ModelLayer(str, Enum):
    """Medallion-style dbt model layer prefixes."""

    STAGING = "stg"
    INTERMEDIATE = "int"
    FACT = "fct"
    DIMENSION = "dim"
    REPORT = "rpt"

    @property
    def prefix(self) -> str:
        return f"{self.value}_"


_LAYER_PREFIXES = tuple(layer.prefix for layer in ModelLayer)
_MODEL_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_COLUMN_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def validate_model_name(name: str) -> bool:
    """Return True if name matches dbt layer prefix and snake_case conventions."""
    if not _MODEL_NAME_PATTERN.match(name):
        return False
    return any(name.startswith(prefix) for prefix in _LAYER_PREFIXES)


def normalize_column_name(raw: str) -> str:
    """Convert a raw column label to snake_case (e.g. 'Order ID' -> 'order_id')."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", raw.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned or not _COLUMN_NAME_PATTERN.match(cleaned):
        raise ValueError(f"Invalid column name after normalization: {raw!r}")
    return cleaned


def build_table_fqn(catalog: str, schema: str, table: str) -> str:
    """Build a Unity Catalog three-part table name."""
    parts = (catalog.strip(), schema.strip(), table.strip())
    if not all(parts):
        raise ValueError("catalog, schema, and table must be non-empty")
    if any("." in part for part in parts):
        raise ValueError("catalog, schema, and table must not contain '.'")
    return ".".join(parts)


class PipelineConfig(BaseModel):
    """Runtime configuration for a batch pipeline job."""

    catalog: str = Field(min_length=1)
    schema_name: str = Field(min_length=1, alias="schema")
    batch_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")

    model_config = {"populate_by_name": True}

    @field_validator("catalog", "schema_name")
    @classmethod
    def _no_dots(cls, value: str) -> str:
        if "." in value:
            raise ValueError("must not contain '.'")
        return value

    @property
    def staging_table(self) -> str:
        return build_table_fqn(self.catalog, self.schema_name, "stg_orders")
