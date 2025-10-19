import pytest
import time
import cProfile
import pstats
from io import StringIO
from timeit import timeit

class TestPerformance:
    """Performance tests to identify slow code and bottlenecks"""
    
    def test_cart_total_calculation_performance(self, client, reset_cart):
        """
        Test cart total calculation speed
        FINDS PERFORMANCE BUG: Inefficient nested loop in get_total_price()
        """
        # Add multiple books with high quantities
        books = ['The Great Gatsby', '1984', 'I Ching', 'Moby Dick']
        
        for book_title in books:
            client.post('/add-to-cart', data={
                'title': book_title,
                'quantity': '50'  # High quantity to expose performance issue
            })
        
        # Measure cart page load time
        start_time = time.time()
        response = client.get('/cart')
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        print(f"\n📊 Cart page loaded in: {duration_ms:.2f}ms")
        
        # Performance threshold
        if duration_ms > 100:
            print(f"⚠️  WARNING: Slow performance detected! (Expected < 100ms)")
        else:
            print(f"✓ Performance is acceptable")
    
    
    def test_cart_calculation_with_timeit(self, client, reset_cart):
        """
        Use timeit module to measure cart total calculation
        Required by assignment specifications
        """
        # Setup: Add items to cart
        client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': '10'})
        client.post('/add-to-cart', data={'title': '1984', 'quantity': '20'})
        
        # Measure execution time using timeit
        def cart_operation():
            client.get('/cart')
        
        # Run 100 times and get average
        total_time = timeit(cart_operation, number=100)
        avg_time_ms = (total_time / 100) * 1000
        
        print(f"\n⏱️  Average cart calculation time (100 runs): {avg_time_ms:.2f}ms")
        
        # Log the result
        assert avg_time_ms < 500, f"Cart calculation too slow: {avg_time_ms}ms"
    
    
    def test_profile_cart_total_calculation(self, client, reset_cart):
        """
        Use cProfile to identify bottlenecks in cart calculation
        Required by assignment specifications
        """
        # Add items to cart
        client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': '25'})
        client.post('/add-to-cart', data={'title': '1984', 'quantity': '30'})
        
        # Create profiler
        profiler = cProfile.Profile()
        
        print("\n\n" + "="*70)
        print("📊 PROFILING CART TOTAL CALCULATION")
        print("="*70)
        
        # Profile the cart page load
        profiler.enable()
        for _ in range(50):  # Run multiple times to get better data
            client.get('/cart')
        profiler.disable()
        
        # Get statistics
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Show top 20 functions
        
        profile_output = stream.getvalue()
        print(profile_output)
        
        # Check if inefficient function is in the profile
        if 'get_total_price' in profile_output:
            print("\n⚠️  PERFORMANCE ISSUE DETECTED:")
            print("   The get_total_price() function appears in profiling results")
            print("   This suggests it may be inefficient (nested loop)")
        
        print("="*70 + "\n")
    
    
    def test_add_to_cart_performance(self, client, reset_cart):
        """Test the speed of adding items to cart"""
        start_time = time.time()
        
        # Add 10 different books
        for i in range(10):
            client.post('/add-to-cart', data={
                'title': 'The Great Gatsby',
                'quantity': str(i + 1)
            })
        
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        
        print(f"\n⚡ Time to add 10 items: {duration_ms:.2f}ms")
        assert duration_ms < 1000, "Adding items is too slow"
    
    
    def test_checkout_page_performance(self, client, reset_cart):
        """Test checkout page load time with items in cart"""
        # Add items
        client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': '5'})
        client.post('/add-to-cart', data={'title': '1984', 'quantity': '3'})
        
        # Measure checkout page load
        start_time = time.time()
        response = client.get('/checkout')
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        
        print(f"\n🛒 Checkout page loaded in: {duration_ms:.2f}ms")
        assert response.status_code == 200
        assert duration_ms < 200, "Checkout page is too slow"