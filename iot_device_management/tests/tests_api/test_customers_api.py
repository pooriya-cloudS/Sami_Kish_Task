import pytest

pytestmark = pytest.mark.django_db


def test_list_customers(authenticated_api_client):
    """
    Feature: Customers
    Scenario: List all customers
    """
    response = authenticated_api_client.get("/api/users/")

    assert response.status_code == 200
    results = response.data.get("results", response.data)
    assert isinstance(results, list)


def test_create_customer_success(api_client, customer_payload):
    """
    Feature: Customers
    Scenario: Create a new customer
    """
    response = api_client.post(
        "/api/users/",
        customer_payload,
        format="json"
    )
    print(response.data)

    assert response.status_code == 201

    data = response.data
    assert "id" in data
    assert data["email"] == customer_payload["email"]
    assert data["name"] == customer_payload["name"]


def test_create_customer_invalid_email(api_client, customer_payload):
    """
    Feature: Customers
    Scenario: Reject invalid email format
    """
    customer_payload["email"] = "not-an-email"

    response = api_client.post(
        "/api/users/",
        customer_payload,
        format="json"
    )

    assert response.status_code == 400
    assert "email" in response.data
