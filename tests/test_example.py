"""
Example test module demonstrating TDD patterns for data engineering.

This file shows fixtures, parametrization, mocking, and pytest marks using
pipeline naming and configuration utilities from `src.pipeline`.

**Pattern:** Red → Green → Refactor
"""

from __future__ import annotations

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.pipeline import (
    ModelLayer,
    PipelineConfig,
    build_table_fqn,
    normalize_column_name,
    validate_model_name,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_order_row() -> Dict[str, Any]:
    """Sample raw order record as it might arrive from a source system."""
    return {
        "Order ID": "ORD-1001",
        "Customer Name": "Ada Lovelace",
        "Order Date": "2026-06-07",
        "Amount USD": 42.50,
    }


@pytest.fixture
def mock_spark_session() -> Mock:
    """Mock Spark session for unit tests without a Databricks cluster."""
    session = Mock()
    session.table.return_value.count.return_value = 0
    return session


@pytest.fixture
def pipeline_config() -> PipelineConfig:
    """Default pipeline configuration for staging loads."""
    return PipelineConfig(catalog="main", schema="analytics", batch_date="2026-06-07")


# ============================================================================
# MODEL NAMING
# ============================================================================


class TestModelNaming:
    """Tests for dbt-style model name validation."""

    def test_valid_staging_model_accepted(self) -> None:
        assert validate_model_name("stg_raw__orders") is True

    def test_invalid_model_without_layer_prefix_rejected(self) -> None:
        assert validate_model_name("orders") is False

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("stg_raw__orders", True),
            ("int_orders_enriched", True),
            ("fct_orders", True),
            ("dim_customers", True),
            ("rpt_daily_orders", True),
            ("Orders", False),
            ("stg-orders", False),
            ("raw_orders", False),
        ],
    )
    def test_model_name_parametrized(self, name: str, expected: bool) -> None:
        assert validate_model_name(name) is expected

    def test_model_layer_prefixes(self) -> None:
        assert ModelLayer.STAGING.prefix == "stg_"


# ============================================================================
# COLUMN NORMALIZATION
# ============================================================================


class TestColumnNormalization:
    """Tests for source-to-warehouse column renaming."""

    def test_normalize_source_column_to_snake_case(self, sample_order_row: Dict[str, Any]) -> None:
        raw_key = "Order ID"
        assert normalize_column_name(raw_key) == "order_id"
        assert raw_key in sample_order_row

    def test_normalize_rejects_empty_label(self) -> None:
        with pytest.raises(ValueError, match="Invalid column name"):
            normalize_column_name("   ")

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("Customer Name", "customer_name"),
            ("Amount USD", "amount_usd"),
            ("order_date", "order_date"),
        ],
    )
    def test_normalize_parametrized(self, raw: str, expected: str) -> None:
        assert normalize_column_name(raw) == expected


# ============================================================================
# PIPELINE CONFIG & TABLE FQN
# ============================================================================


class TestPipelineConfig:
    """Tests for batch pipeline configuration."""

    def test_staging_table_fqn(self, pipeline_config: PipelineConfig) -> None:
        assert pipeline_config.staging_table == "main.analytics.stg_raw__orders"

    def test_rejects_catalog_with_dot(self) -> None:
        with pytest.raises(ValueError, match="must not contain"):
            PipelineConfig(catalog="main.prod", schema="analytics", batch_date="2026-06-07")

    def test_build_table_fqn_validates_parts(self) -> None:
        with pytest.raises(ValueError, match="must not contain"):
            build_table_fqn("main", "analytics.stg", "orders")


class TestSparkBatchLoad:
    """Example of mocking Spark for a staging load."""

    def test_read_source_table(
        self, mock_spark_session: Mock, pipeline_config: PipelineConfig
    ) -> None:
        mock_spark_session.table(pipeline_config.staging_table).count()

        mock_spark_session.table.assert_called_once_with("main.analytics.stg_raw__orders")
        mock_spark_session.table.return_value.count.assert_called_once()


# ============================================================================
# FIXTURES WITH SETUP/TEARDOWN
# ============================================================================


@pytest.fixture
def catalog_client():
    """Set up and tear down a mocked Unity Catalog client."""
    client = Mock()
    client.list_schemas.return_value = ["analytics", "raw"]
    yield client
    client.close()


@pytest.fixture(params=["dev", "prod"])
def environment(request: pytest.FixtureRequest) -> str:
    return str(request.param)


def test_catalog_client_lists_schemas_in_each_environment(
    catalog_client: Mock, environment: str
) -> None:
    assert environment in ["dev", "prod"]
    assert "analytics" in catalog_client.list_schemas()


# ============================================================================
# MARKS & EDGE CASES
# ============================================================================


@pytest.mark.unit
def test_is_unit_test() -> None:
    assert validate_model_name("stg_raw__smoke") is True


@pytest.mark.integration
def test_is_integration_test() -> None:
    assert (
        build_table_fqn("main", "analytics", "stg_raw__orders") == "main.analytics.stg_raw__orders"
    )


@pytest.mark.slow
def test_process_large_batch_of_rows() -> None:
    rows = [{"order_id": i, "amount_usd": float(i)} for i in range(10_000)]
    assert len(rows) == 10_000
    assert all("order_id" in row for row in rows)


@pytest.mark.skip(reason="Not implemented yet")
def test_skipped_incremental_merge() -> None:
    assert False


@pytest.mark.xfail(reason="Known limitation in example scaffold")
def test_expected_failure() -> None:
    assert validate_model_name("orders") is True


def test_with_patch_decorator() -> None:
    with patch("builtins.print") as mock_print:
        print("dbt run --select stg_raw__orders")
        mock_print.assert_called_once_with("dbt run --select stg_raw__orders")
