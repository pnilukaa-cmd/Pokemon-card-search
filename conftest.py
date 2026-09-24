"""Make pytest honest about test_ability_engine.py.

Its check() records a failure in FAILURES and carries on, so under pytest
every test "passed" whatever it checked -- only `python
test_ability_engine.py` reported the truth. Fail any test that added to
FAILURES.
"""
import pytest


@pytest.fixture(autouse=True)
def _checks_must_pass(request):
    mod = request.module
    failures = getattr(mod, "FAILURES", None)
    if failures is None:
        yield
        return
    before = len(failures)
    yield
    new = failures[before:]
    if new:
        pytest.fail("check() failed: " + "; ".join(new), pytrace=False)
