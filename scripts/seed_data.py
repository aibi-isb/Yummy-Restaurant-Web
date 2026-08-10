#!/usr/bin/env python
"""Seed the database with initial data."""

import os
import sys
import shutil
import django
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.customers.models import CustomerProfile
from apps.menu.models import Food
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment
from apps.notifications.models import Notification
from apps.core.choices import OrderStatus, PaymentStatus, PaymentMethod, NotificationType
from apps.core.helpers import generate_order_number


CUSTOMERS = [
    {'username': 'Ousi', 'email': 'ousi@yummy.com', 'password': 'password123',
     'full_name': 'Ousi', 'address': '12 Independence Ave, Accra', 'phone': '024-100-0001'},
]


def seed_customers():
    for data in CUSTOMERS:
        if User.objects.filter(username=data['username']).exists():
            print(f"Customer '{data['username']}' already exists")
            continue
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )
        CustomerProfile.objects.create(
            user=user,
            full_name=data['full_name'],
            address=data['address'],
            phone_number=data['phone'],
        )
        print(f"Created customer '{data['username']}' ({data['full_name']}) / {data['password']}")


ORDER_DATA = {
    'Ousi': [
        {'items': [(1, 2), (5, 1)], 'status': 'delivered', 'payment': 'approved', 'method': 'mobile_money', 'days_ago': 14},
        {'items': [(3, 1), (4, 2)], 'status': 'delivered', 'payment': 'approved', 'method': 'card', 'days_ago': 7},
        {'items': [(7, 1), (2, 1)], 'status': 'preparing', 'payment': 'approved', 'method': 'mobile_money', 'days_ago': 1},
        {'items': [(6, 2), (8, 1), (5, 2)], 'status': 'pending', 'payment': 'pending', 'method': 'mobile_money', 'days_ago': 0},
        {'items': [(6, 2), (8, 1)], 'status': 'delivered', 'payment': 'approved', 'method': 'mobile_money', 'days_ago': 10},
        {'items': [(1, 1), (3, 2), (5, 2)], 'status': 'payment_received', 'payment': 'pending', 'method': 'card', 'days_ago': 0},
        {'items': [(4, 3)], 'status': 'delivered', 'payment': 'approved', 'method': 'card', 'days_ago': 21},
        {'items': [(2, 1), (7, 1)], 'status': 'ready', 'payment': 'approved', 'method': 'mobile_money', 'days_ago': 3},
        {'items': [(1, 1)], 'status': 'pending', 'payment': 'rejected', 'method': 'card', 'days_ago': 3},
    ],
}

NOTIFICATION_MAP = {
    ('pending', 'pending'): None,
    ('payment_received', 'approved'): ('order_confirmed', 'Order Confirmed', 'Your order has been confirmed and payment received.'),
    ('preparing', 'approved'): ('order_preparing', 'Order Being Prepared', 'Your meal is now being prepared in the kitchen.'),
    ('ready', 'approved'): ('order_ready', 'Order Ready', 'Your order is ready for pickup/delivery.'),
    ('delivered', 'approved'): ('order_delivered', 'Order Delivered', 'Your order has been delivered. Enjoy your meal!'),
    ('pending', 'rejected'): ('payment_rejected', 'Payment Rejected', 'Your payment was rejected. Please try again.'),
}


def seed_mock_data():
    foods = {f.id: f for f in Food.objects.all()}
    profiles = {p.user.username: p for p in CustomerProfile.objects.select_related('user').all()}

    for username, orders in ORDER_DATA.items():
        profile = profiles.get(username)
        if not profile:
            print(f"  Skipping '{username}' — no profile found")
            continue

        for odata in orders:
            items = []
            for food_id, qty in odata['items']:
                food = foods.get(food_id)
                if food:
                    items.append({'food_id': food_id, 'quantity': qty, 'price': food.price})

            if not items:
                continue

            total = sum(Decimal(str(it['quantity'])) * it['price'] for it in items)
            created_at = timezone.now() - timedelta(days=odata['days_ago'])

            order = Order.objects.create(
                customer=profile,
                order_number=generate_order_number(),
                delivery_address=profile.address,
                total_amount=total,
                status=odata['status'],
                created_at=created_at,
                updated_at=created_at + timedelta(hours=2),
            )

            for it in items:
                OrderItem.objects.create(
                    order=order,
                    food_id=it['food_id'],
                    quantity=it['quantity'],
                    unit_price=it['price'],
                    subtotal=Decimal(str(it['quantity'])) * it['price'],
                )

            method = odata['method']
            pay_fields = {
                'order': order,
                'customer': profile,
                'method': method,
                'amount': total,
                'status': odata['payment'],
                'created_at': created_at,
            }
            if method == 'mobile_money':
                pay_fields['mobile_number'] = profile.phone_number
                pay_fields['network'] = 'MTN'
            else:
                pay_fields['card_holder'] = profile.full_name
                pay_fields['card_number'] = '1234'
            Payment.objects.create(**pay_fields)

            notif_key = (odata['status'], odata['payment'])
            notif_info = NOTIFICATION_MAP.get(notif_key)
            if notif_info:
                ntype, title, message = notif_info
                Notification.objects.create(
                    customer=profile,
                    title=title,
                    message=message,
                    notification_type=ntype,
                    is_read=False if odata['days_ago'] < 2 else True,
                    created_at=created_at + timedelta(hours=2, minutes=10),
                )

            print(f"  Order {order.order_number} ({odata['status']}/{odata['payment']}) for {username} — Le {total}")


def seed(with_mock=False):
    call_command('loaddata', 'fixtures/food_categories.json', verbosity=1)

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@yummy.com', 'admin123')
        print('Created admin user (admin/admin123)')
    else:
        print('Admin user already exists')

    seed_customers()

    if with_mock:
        seed_mock_data()

    foods_dir = os.path.join(settings.MEDIA_ROOT, 'foods')
    os.makedirs(foods_dir, exist_ok=True)

    sample_images = sorted([
        f for f in os.listdir(os.path.join(settings.BASE_DIR, 'static/public/img/menu'))
        if f.endswith(('.png', '.jpg', '.jpeg'))
    ])

    for i, food in enumerate(Food.objects.all()):
        if not food.image and i < len(sample_images):
            src = os.path.join(settings.BASE_DIR, 'static/public/img/menu', sample_images[i])
            dst_name = f'food_{food.id}_{sample_images[i]}'
            dst = os.path.join(foods_dir, dst_name)
            shutil.copy2(src, dst)
            food.image.name = os.path.join('foods', dst_name)
            food.save(update_fields=['image'])
            print(f'  Assigned {sample_images[i]} to {food.name}')

    print('Seeding complete!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed the database')
    parser.add_argument('--with-mock', action='store_true', help='Include mock orders/payments/notifications')
    args = parser.parse_args()
    seed(with_mock=args.with_mock)