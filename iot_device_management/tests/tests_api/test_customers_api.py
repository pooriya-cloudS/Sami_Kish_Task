import pytest

pytestmark = pytest.mark.django_db


def test_list_customers(api_client):
    """
    Feature: Customers
    Scenario: List all customers
    Given the API is running
    When client requests list of customers
    Then response should be 200
    And response should be a list
    """
    response = api_client.get("/api/customers/")

    assert response.status_code == 200
    assert isinstance(response.data, list)


def test_create_customer_success(api_client):
    """
    Feature: Customers
    Scenario: Create a new customer
    Given valid customer data
    When client creates a customer
    Then customer should be created successfully
    """
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
    }

    response = api_client.post(
        "/api/customers/",
        payload,
        format="json"
    )

    assert response.status_code == 201

    data = response.data
    assert "id" in data
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]


def test_create_customer_invalid_email(api_client):
    """
    Feature: Customers
    Scenario: Reject invalid email format
    Given customer data with invalid email
    When client creates a customer
    Then validation error should be returned
    """
    payload = {
        "name": "Invalid User",
        "email": "not-an-email",
    }

    response = api_client.post(
        "/api/customers/",
        payload,
        format="json"
    )

    assert response.status_code == 400
    assert "email" in response.data
