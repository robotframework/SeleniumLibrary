"""Test helper for Secret type acceptance tests."""

try:
    from robot.api import types as _robot_api_types

    _SECRET_AVAILABLE = hasattr(_robot_api_types, "Secret")
except ImportError:  # RF < 7.4
    _SECRET_AVAILABLE = False


def skip_if_no_secret():
    """Skip the current test if ``robot.api.types.Secret`` is unavailable (RF < 7.4)."""
    if not _SECRET_AVAILABLE:
        from robot.libraries.BuiltIn import BuiltIn

        BuiltIn().skip("RF Secret type requires Robot Framework 7.4+")
