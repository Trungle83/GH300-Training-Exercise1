from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"
    original_participants = app_module.activities[activity_name]["participants"][:]

    try:
        app_module.activities[activity_name]["participants"] = []

        first_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )
        second_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert first_response.status_code == 200
        assert second_response.status_code == 409
        assert second_response.json()["detail"] == "Student already signed up for this activity"
    finally:
        app_module.activities[activity_name]["participants"] = original_participants
