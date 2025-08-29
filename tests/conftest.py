import pytest
from fastapi.testclient import TestClient
from music_system.main import app
from music_system.database import Base, engine

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)
