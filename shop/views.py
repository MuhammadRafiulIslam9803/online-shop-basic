from django.contrib import messages
from django.shortcuts import render
from django.views import View

from root_app.shop.forms import CustomerRegistrationForm

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

class categoryView(View):
    def get(self, request, category):
        products = Product.objects.filter(category=category)
        return render(request, "shop/category.html", {"products": products})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "shop/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! You have registered successfully.")
        return render(request, "shop/customerregistration.html", {"form": form})