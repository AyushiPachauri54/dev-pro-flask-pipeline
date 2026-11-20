from app import app

def test_home_route_returns_success():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Flask application is running successfully"
    }
