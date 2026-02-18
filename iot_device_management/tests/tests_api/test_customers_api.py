import pytest

pytestmark = pytest.mark.django_db


def test_list_customers(api_client):
    """
    Feature: Customers
    Scenario: List all customers
    """
    response = api_client.get("/api/customers/")

    assert response.status_code == 200
    assert isinstance(response.data, list)


def test_create_customer_success(api_client, customer_payload):
    """
    Feature: Customers
    Scenario: Create a new customer
    """
    response = api_client.post(
        "/api/customers/",
        customer_payload,
        format="json"
    )

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
        "/api/customers/",
        customer_payload,
        format="json"
    )

    assert response.status_code == 400
    assert "email" in response.data
