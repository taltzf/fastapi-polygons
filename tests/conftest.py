import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """
    Session-scoped event loop to suppress pytest-asyncio deprecation warning.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
