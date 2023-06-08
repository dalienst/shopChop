import stripe
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

from store.models import Product, Category, Order, OrderItem
from store.cart import Cart
from store.forms import OrderForm


@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    messages.success(request, "Product Added to cart")

    return redirect("core:frontpage")


@login_required
def cart_view(request):
    cart = Cart(request)

    return render(request, "store/cart_view.html", {"cart": cart})


@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    messages.success(request, "Product removed from cart")

    return redirect("store:cart_view")


@login_required
def change_quantity(request, product_id):
    action = request.GET.get("action", "")
    if action:
        quantity = 1

        if action == "decrease":
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    messages.success(request, "Item quantity increased")

    return redirect("store:cart_view")


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        data = json.loads(request.body)
        form = OrderForm(request.POST)

        total_price = 0
        items = []

        for item in cart:
            product = item["product"]
            total_price += product.price * int(item["quantity"])

            items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product.title,
                        },
                        "unit_amount": product.price,
                    },
                    "quantity": item["quantity"],
                }
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            success_url=f"{settings.WEBSITE_URL}store/cart/success/",
            cancel_url=f"{settings.WEBSITE_URL}store/cart/",
        )

        payment_intent = stripe.PaymentIntent.create(
            payment_method_types=["card"],
            amount=total_price,
            currency="usd",
        )

        order = Order.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["address"],
            zipcode=data["zipcode"],
            city=data["city"],
            created_by=request.user,
            is_paid=True,
            payment_intent=payment_intent,
            paid_amount=total_price,
        )

        for item in cart:
            product = item["product"]
            quantity = int(item["quantity"])
            price = product.price * quantity

            item = OrderItem.objects.create(
                order=order, product=product, price=price, quantity=quantity
            )

        cart.clear()

        return JsonResponse({"session": session, "order": payment_intent})
    else:
        form = OrderForm()

    return render(
        request,
        "store/check_out.html",
        {
            "cart": cart,
            "form": form,
            "pub_key": settings.STRIPE_PUB_KEY,
        },
    )


def success(request):
    return render(request, "store/success.html")


def search(request):
    query = request.GET.get("query", "")
    products = Product.objects.filter(status=Product.ACTIVE).filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    return render(request, "store/search.html", {"query": query, "products": products})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(
        request,
        "store/category_detail.html",
        {"category": category, "products": products},
    )


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    return render(request, "store/product_detail.html", {"product": product})
