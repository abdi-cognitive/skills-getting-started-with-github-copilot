import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# take a snapshot of the initial in-memory state
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """TestClient for exercising the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Restore the `activities` dict to its original contents before every test.

    The fixture is `autouse` so it runs for every test without
    needing to be requested explicitly.
    """
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # cleanup (not strictly necessary since we reset before the next test,
    # but keeps state predictable if somebody inspects after a failure).
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
