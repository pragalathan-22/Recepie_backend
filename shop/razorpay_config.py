import razorpay
from django.conf import settings

# Initialize Razorpay client
client = razorpay.Client(auth=("rzp_test_TgoyRB6TISQvTe", "4j71MwXwEcplPWrqD7DLvNoQ"))

def create_order(amount, currency="INR"):
    """
    Create a Razorpay order
    amount: Amount in paise (multiply by 100)
    currency: Currency code (default: INR)
    """
    try:
        # Convert amount to paise
        amount_in_paise = int(amount * 100)
        
        # Create order
        order_data = {
            'amount': amount_in_paise,
            'currency': currency,
            'payment_capture': 1  # Auto-capture payment
        }
        
        order = client.order.create(data=order_data)
        return order
    except Exception as e:
        print(f"Error creating Razorpay order: {str(e)}")
        return None

def verify_payment(payment_id, order_id, signature):
    """
    Verify Razorpay payment
    """
    try:
        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        return True
    except Exception as e:
        print(f"Error verifying payment: {str(e)}")
        return False 