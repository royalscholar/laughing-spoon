import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def reset_runtime_state() -> None:
    from app.services.log_service import reset_logs_for_tests
    from app.services.state import reset_state_for_tests

    reset_state_for_tests()
    reset_logs_for_tests()
