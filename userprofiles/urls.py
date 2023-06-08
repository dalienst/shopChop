from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from userprofiles import views

app_name = "userprofiles"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(template_name="userprofile/login.html"),
        name="login",
    ),
    path("myaccount/", views.myaccount, name="myaccount"),
    path("my-store/", views.mystore, name="mystore"),
    path("my-store/order-detail/<int:pk>/", views.my_store_order_detail, name="mystore_orderdetail"),
    path("my-store/add-product/", views.add_product, name="add_product"),
    path("my-store/edit-product/<int:pk>/", views.edit_product, name="edit_product"),
    path("my-store/delete-product/<int:pk>/", views.delete_product, name="delete_product"),
    path("vendors/<int:pk>/", views.vendor_detail, name="vendor_detail"),
]
