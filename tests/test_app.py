from fastapi.testclient import TestClient

from src.app import app, activities  # import to inspect/alter state if needed


def test_root_redirect(client: TestClient):
    # Arrange: client fixture provides TestClient
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client: TestClient):
    # Arrange: the activities dict is already seeded
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    new_email = "newstudent@mergington.edu"
    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": new_email}
    )
    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_email} for {activity}"
    }
    # verify state changed
    assert new_email in activities[activity]["participants"]


def test_signup_duplicate(client: TestClient):
    # Arrange
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]
    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": existing}
    )
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client: TestClient):
    # Arrange
    bogus = "Nonexistent Club"
    # Act
    response = client.post(
        f"/activities/{bogus}/signup", params={"email": "foo@bar.com"}
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client: TestClient):
    # Arrange
    activity = "Programming Class"
    participant = activities[activity]["participants"][0]
    # Act
    response = client.delete(
        f"/activities/{activity}/signup", params={"email": participant}
    )
    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {participant} from {activity}"
    }
    assert participant not in activities[activity]["participants"]


def test_remove_nonexistent_participant(client: TestClient):
    # Arrange
    activity = "Programming Class"
    fake = "noone@mergington.edu"
    # Act
    response = client.delete(
        f"/activities/{activity}/signup", params={"email": fake}
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_nonexistent_activity(client: TestClient):
    # Arrange
    bogus = "Imaginary Activity"
    # Act
    response = client.delete(
        f"/activities/{bogus}/signup", params={"email": "someone@school.edu"}
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
