"""Test helper for building Secret objects in acceptance tests.

Robot Framework's Secret type is only available in RF 7.4+. This helper
exposes ``Make Secret`` plus a ``SECRET_AVAILABLE`` boolean so tests can
skip cleanly on older versions.
"""

try:
    from robot.api.types import Secret

    SECRET_AVAILABLE = True
except ImportError:  # RF < 7.4
    Secret = None  # type: ignore[assignment,misc]
    SECRET_AVAILABLE = False


def make_secret(value: str):
    """Wrap *value* in a Robot Framework Secret object."""
    if Secret is None:
        raise RuntimeError("Secret type requires Robot Framework 7.4+")
    return Secret(value)