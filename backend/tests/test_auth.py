from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

# This creates a "fake browser" that can talk to your FastAPI app internally
client = TestClient(app)

def test_admin_route_security():
    """
    Ensure that an unauthenticated user cannot access the admin users list.
    """
    response = client.get(f"{settings.API_V1_STR}/auth/users")
    
    # We expect the server to reject this request with a 401 Unauthorized
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}