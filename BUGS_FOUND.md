# 🐛 Bugs Found Through Testing

---

## Bug #1: Application Crashes with Non-Numeric Quantity Input

### Severity: HIGH 🔴
**Status:** ✅ FIXED 
**Date Found:** October 19, 2025
**Date Fixed:** October 19, 2025

### Description
When a user enters non-numeric text (e.g., "abc") in the quantity field, the application crashes with a ValueError instead of handling the error gracefully.

### Location
- **File:** `app.py`
- **Function:** `add_to_cart()`
- **Line:** 60

### Steps to Reproduce
1. Navigate to the home page
2. Find any book
3. Enter "abc" in the quantity field
4. Click "Add to Cart"
5. Application crashes

### Expected Behavior
- Should display error message: "Please enter a valid quantity"
- Should redirect user back to home page
- Should NOT crash

### Actual Behavior
```
ValueError: invalid literal for int() with base 10: 'abc'
```
Application crashes completely.

### Test Case
`tests/test_cart.py::TestCart::test_add_book_invalid_quantity`

### Root Cause
No error handling around the `int()` conversion:
```python
quantity = int(request.form.get('quantity', 1))  # Line 60 - No try/except!
```

### Proposed Fix
Add try-except block to handle ValueError:
```python
try:
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        flash('Quantity must be at least 1', 'error')
        return redirect(url_for('index'))
except ValueError:
    flash('Please enter a valid quantity', 'error')
    return redirect(url_for('index'))
```

---

## Bug #2: Negative Quantities Accepted in Cart

### Severity: MEDIUM 🟡
**Status:** ✅ FIXED  
**Date Found:** October 19, 2025
**Date Fixed:** October 19, 2025

### Description
The application accepts negative quantities (e.g., -5) when adding books to cart. This creates illogical cart states where "Total Items: -5" is displayed.

### Location
- **File:** `app.py`
- **Function:** `add_to_cart()`
- **Line:** 60

### Steps to Reproduce
1. Navigate to home page
2. Find any book
3. Enter "-5" in the quantity field
4. Click "Add to Cart"
5. View cart - shows "-5" items

### Expected Behavior
- Should reject negative quantities
- Should display error: "Quantity must be a positive number"
- Cart should remain empty

### Actual Behavior
- Negative quantity is accepted
- Cart displays: "Total Items: -5"
- Total Price shows: "$0.00"

### Test Case
`tests/test_cart.py::TestCart::test_add_book_negative_quantity`

### Root Cause
No validation to check if quantity is positive:
```python
quantity = int(request.form.get('quantity', 1))  # Accepts any integer, including negatives
```

### Proposed Fix
Add validation after converting to int:
```python
quantity = int(request.form.get('quantity', 1))
if quantity < 1:
    flash('Quantity must be at least 1', 'error')
    return redirect(url_for('index'))
```

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Tests Run | 4 |
| Tests Passed | 2 |
| Tests Failed (Bugs Found) | 2 |
| Critical Bugs | 1 |
| Medium Bugs | 1 |

---

## Impact Assessment

**Bug #1 Impact:**
- User experience: SEVERE (app crashes)
- Data integrity: MEDIUM (no data saved when crashes)
- Security: LOW

**Bug #2 Impact:**
- User experience: MEDIUM (confusing display)
- Data integrity: MEDIUM (incorrect cart calculations)
- Security: LOW

---

## Next Steps
1. ✅ Bugs documented
2. ✅ Fixes implemented
3. ✅ Tests re-run - all passing!
4. ⏳ Add additional edge case tests
5. ⏳ Performance testing
6. ⏳ Security testing
7. ⏳ CI/CD pipeline setup