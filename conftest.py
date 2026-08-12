"""Repository-wide pytest entry-point options and collection policy."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--data-root",
        action="store",
        default="./data",
        help="ProductQuant data root used by explicit full-data acceptance tests",
    )


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Keep the costly acceptance gate explicit without reporting a skip/pass."""
    if config.option.markexpr:
        return
    full_data = [item for item in items if item.get_closest_marker("full_data")]
    if not full_data:
        return
    items[:] = [item for item in items if item not in full_data]
    config.hook.pytest_deselected(items=full_data)
