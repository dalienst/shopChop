from django import forms

from store.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "title", "description", "price", "image", "status")
        widgets = {
            "category": forms.Select(attrs={"class": "w-full p-2 border border-gray-200"}),
            "title": forms.TextInput(attrs={"class": "w-full p-2 border border-gray-200"}),
            "description": forms.Textarea(attrs={"class": "w-full p-2 border border-gray-200"}),
            "price": forms.NumberInput(attrs={"class": "w-full p-2 border border-gray-200"}),
            "image": forms.FileInput(attrs={"class": "w-full p-2 border border-gray-200"}),
            "status": forms.Select(attrs={"class": "w-full p-2 border border-gray-200"}),
        }
