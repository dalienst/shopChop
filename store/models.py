from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image


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
    thumbnail = models.ImageField(
        upload_to="uploads/product_images/thumbnail/", blank=True, null=True
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

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return "https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHNob3B8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)
        name = image.name.replace('uploads/product_images/', '')

        thumbnail = File(thumb_io, name=name)

        return thumbnail
