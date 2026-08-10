import random
import string
from datetime import datetime


def format_currency(amount):
    return f"Le {amount:,.2f}"


def generate_order_number():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    rand = ''.join(random.choices(string.digits, k=4))
    return f"ORD-{timestamp}-{rand}"
