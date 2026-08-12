"""Typed command failures for stable CLI exit semantics."""

from __future__ import annotations


class ProductQuantError(Exception):
    """Expected, sanitized command failure."""

    exit_code = 1
    error_code = "internal_error"


class NetworkError(ProductQuantError):
    exit_code = 3
    error_code = "network_error"


class IntegrityError(ProductQuantError):
    exit_code = 4
    error_code = "integrity_error"


class StateError(ProductQuantError):
    exit_code = 5
    error_code = "state_error"
