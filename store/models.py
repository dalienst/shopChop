from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    DRAFT = "draft"
    WAITING_APPROVAL = "waitingapproval"
    ACTIVE = "active"
    DELETED = "deleted"

    STATUS_CHOICES = (
        (DRAFT, "Draft"),
        (WAITING_APPROVAL, "Waiting Approval"),
        (ACTIVE, "Active"),
        (DELETED, "Deleted"),
    )

    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(
        upload_to="uploads/product_images/", blank=True, null=True
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title

    def get_display_price(self):
        return self.price / 100
