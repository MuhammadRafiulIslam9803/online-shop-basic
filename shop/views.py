from django.shortcuts import render

# Create your views here.


def home(request):
    available_products = [
        {"name": "Product 1", "price": 10.99},
        {"name": "Product 2", "price": 19.99},
        {"name": "Product 3", "price": 5.99},
        {"name": "Product 4", "price": 15.99},
        {"name": "Product 5", "price": 25.99},
    ]
    return render(request, "shop/home.html", {"available_products": available_products})
