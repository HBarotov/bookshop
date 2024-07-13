import weasyprint
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            # Asynchronous task
            order_created.delay(order.id)
            request.session["order_id"] = order.id
            return redirect("payments:process")
    else:
        form = OrderCreateForm()
    context = {"cart": cart, "form": form}
    return render(request, "orders/create.html", context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {"order": order}
    return render(request, "orders/admin/detail.html", context)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(finders.find("css/pdf.css"))]
    )
    return response
