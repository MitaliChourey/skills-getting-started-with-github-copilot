from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Ensure src directory is importable
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "src"))

from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_remove_participant():
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Ensure participant exists before removal
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email in resp.json()[activity]["participants"]

    # Remove the participant
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Removed {email} from {activity}"

    # Confirm participant no longer present
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_remove_nonexistent_participant():
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"

    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert resp.status_code == 404
