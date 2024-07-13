from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_completed(request):
    return render(request, "payments/completed.html")


def payment_cancelled(request):
    return render(request, "payments/cancelled.html")


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payments:completed"))
        cancel_url = request.build_absolute_uri(reverse("payments:cancelled"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }

        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                },
            )

        # add shipping cost to the Stripe checkout session
        session_data["line_items"].append(
            {
                "price_data": {
                    "unit_amount": int(order.get_shipping_cost() * Decimal("100")),
                    "currency": "usd",
                    "product_data": {
                        "name": "Shipping Cost",
                    },
                },
                "quantity": 1,
            }
        )

        # Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code, percent_off=order.discount, duration="once"
            )
            session_data["discounts"] = [{"coupon": stripe_coupon.id}]

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, "payments/process.html", locals())
