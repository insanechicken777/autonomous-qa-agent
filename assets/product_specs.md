# Product Specifications & Business Rules

## Discount Codes
1. **SAVE15**: Grants a 15% discount on the total cart value.
2. **FREESHIP**: Sets shipping cost to $0 regardless of the method selected.
3. Any other code should display an error message: "Invalid Coupon".

## Shipping Rules
- **Standard Shipping**: Always Free ($0).
- **Express Shipping**: Flat rate of $10.
- **Exception**: If the Cart Total is greater than $200, Express Shipping becomes Free automatically.

## Cart Logic
- Minimum quantity for any item is 1.
- Maximum quantity for "Wireless Headphones" is 5 per customer.