import pytest
from app import app, cart, users, orders

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def reset_cart():
    """Reset cart before each test"""
    cart.clear()
    yield
    cart.clear()

@pytest.fixture
def reset_data():
    """Reset users and orders before tests"""
    users.clear()
    orders.clear()
    # Recreate demo user
    from models import User
    demo_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Demo Street")
    users["demo@bookstore.com"] = demo_user
    yield