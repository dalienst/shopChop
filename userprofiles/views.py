from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify


from userprofiles.models import Userprofile
from store.forms import ProductForm
from store.models import Product


def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(
        request, "userprofile/vendor_detail.html", {"user": user, "products": products}
    )


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            messages.success(request, "Account created")
            return redirect("core:frontpage")
    else:
        form = UserCreationForm()
    return render(request, "userprofile/signup.html", {"form": form})


@login_required
def myaccount(request):
    return render(request, "userprofile/myaccount.html")


@login_required
def mystore(request):
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request, "userprofile/mystore.html", {"products": products})


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get("title")
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, "Product has been created successfully")

            return redirect("userprofiles:mystore")
    else:
        form = ProductForm()
    return render(
        request,
        "userprofile/add_product.html",
        {"form": form, "title": "Add Product"},
    )


@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, "Product has been updated successfully")

            return redirect("userprofiles:mystore")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "userprofile/edit_product.html",
        {
            "title": "Edit Product",
            "form": form,
            "product": product,
        },
    )


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, "Product has been deleted")

    return redirect("userprofiles:mystore")
