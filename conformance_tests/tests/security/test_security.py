import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)
from conformance_tests.src.ngl_security import NGLSecurity


def test_signature_verification():
    sec = NGLSecurity()
    result = sec.verify_signature(b"message", b"sig")
    assert result.valid
