from django.shortcuts import render
from django.views import View

from .models import Product

# Create your views here.


class ProductView(View):
    def get(self, request):
        gentsPant = Product.objects.filter(category="pant")
        shirts = Product.objects.filter(category="shirt")
        borka = Product.objects.filter(category="borka")
        shoes = Product.objects.filter(category="shoes")
        return render(
            request,
            "shop/home.html",
            {"gentsPant": gentsPant, "shirts": shirts, "borka": borka, "shoes": shoes},
        )

class ProductDetailsView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, "shop/productDetails.html", {"product": product})