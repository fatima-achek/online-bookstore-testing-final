import pytest

class TestCart:
    """Tests for shopping cart functionality"""
    
    def test_add_book_to_cart_success(self, client, reset_cart):
        """Test successfully adding a book to cart"""
        # Add a book with quantity 2
        response = client.post('/add-to-cart', data={
            'title': 'The Great Gatsby',
            'quantity': '2'
        })
        
        # Should redirect (status code 302)
        assert response.status_code == 302
        
        # Now check the cart page
        cart_response = client.get('/cart')
        assert cart_response.status_code == 200
        assert b'The Great Gatsby' in cart_response.data
        print("\n✓ Test passed: Book added to cart successfully!")
    
    
    def test_add_book_invalid_quantity(self, client, reset_cart):
        """Test adding book with invalid (non-numeric) quantity - FINDS BUG!"""
        # Try to add with text instead of number
        response = client.post('/add-to-cart', data={
            'title': 'The Great Gatsby',
            'quantity': 'abc'  # This is invalid!
        })
        
        # Should handle gracefully, not crash
        # Currently this WILL crash - that's the bug!
        assert response.status_code in [200, 302, 400]
        print("\n✓ Test passed: Invalid quantity handled correctly!")
    
    
    def test_add_book_negative_quantity(self, client, reset_cart):
        """Test adding book with negative quantity - FINDS BUG!"""
        # Try negative number
        response = client.post('/add-to-cart', data={
            'title': '1984',
            'quantity': '-5'
        })
        
        # Should reject negative quantities
        assert response.status_code in [200, 302]
        
        # Cart should be empty
        cart_response = client.get('/cart')
        assert b'Your cart is empty' in cart_response.data
        print("\n✓ Test passed: Negative quantity rejected!")
    
    
    def test_view_empty_cart(self, client, reset_cart):
        """Test viewing an empty cart"""
        response = client.get('/cart')
        
        assert response.status_code == 200
        assert b'Your cart is empty' in response.data
        print("\n✓ Test passed: Empty cart displays correctly!")