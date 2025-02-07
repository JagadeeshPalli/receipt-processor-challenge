from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Sample receipt for testing
receipt_data = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "Knorr Chicken", "price": "1.26"}
    ],
    "total": "23.35"
}

def test_process_receipt():
    """Test POST /receipts/process"""
    response = client.post("/receipts/process", json=receipt_data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_points():
    """Test GET /receipts/{id}/points"""
    # Step 1: Send receipt and get ID
    response = client.post("/receipts/process", json=receipt_data)
    receipt_id = response.json()["id"]

    # Step 2: Fetch points using the receipt ID
    response = client.get(f"/receipts/{receipt_id}/points")

    assert response.status_code == 200
    points = response.json().get("points", 0)

    # Step 3: Update Expected Points Calculation
    expected_points = 6  # Retailer name (Target) has 6 alphanumeric chars
    expected_points += 10  # Two pairs of items (4 items = 2 pairs x 5 points)
    expected_points += 3   # "Emils Cheese Pizza" has 18 characters (multiple of 3)
    expected_points += 6   # Purchase day is odd

    assert points == expected_points, f"Expected {expected_points}, got {points}"

