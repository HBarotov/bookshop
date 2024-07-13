from coupons.forms import CouponApplyForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shops.models import Product
from shops.recommender import Recommender

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd["quantity"], override_quantity=cd["override"]
        )
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    cart_product_form = CartAddProductForm()
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )

    r = Recommender()
    cart_products = [item["product"] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, 4)
    else:
        recommended_products = []

    context = {
        "cart": cart,
        "coupon_apply_form": coupon_apply_form,
        "recommended_products": recommended_products,
        "cart_product_form": cart_product_form,
    }
    return render(request, "cart/detail.html", context)
