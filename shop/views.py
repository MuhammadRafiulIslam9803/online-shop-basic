from django.contrib import messages
from django.http import request, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib.auth.views import LogoutView

from .models import Customer, Order, OrderItem, Product, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import transaction

# Create your views here.


# home page view
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


# product details view
class ProductDetailsView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, "shop/productDetails.html", {"product": product})


# category view
class categoryView(View):
    def get(self, request, category):
        products = Product.objects.filter(category=category)
        return render(request, "shop/category.html", {"products": products})


# customer registration view
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "shop/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congratulations! You have registered successfully."
            )
            return redirect("home")
        return render(request, "shop/customerregistration.html", {"form": form})


# customer logout view
class UserLogoutView(LogoutView):
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")

        return super().dispatch(request, *args, **kwargs)


# Customer profile view
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)

        form = CustomerProfileForm(instance=customer)

        return render(request, "shop/profile.html", {"form": form})

    def post(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)

        form = CustomerProfileForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()

            messages.success(request, "Profile updated successfully!")

            return redirect("address")

        return render(request, "shop/profile.html", {"form": form})


# show profile on address page
class AddressView(View):
    def get(self, request):
        customer = Customer.objects.filter(user=request.user).first()

        return render(request, "shop/address.html", {"customer": customer})


# add to cart view
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart.")

        return redirect("cart")


# cart view
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_items = cart.items.select_related("product")

        total = 0

        for item in cart_items:
            price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            item.subtotal = price * item.quantity
            total += item.subtotal

        return render(
            request,
            "shop/cart.html",
            {
                "cart_items": cart_items,
                "total": total,
            },
        )


# quantity remove add in cart view
class IncreaseCartView(LoginRequiredMixin, View):
    def post(self, request, id):
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)

        cart_item.quantity += 1
        cart_item.save()

        price = (
            cart_item.product.discounted_price
            if cart_item.product.discounted_price
            else cart_item.product.price
        )

        subtotal = price * cart_item.quantity

        cart = cart_item.cart

        total = 0

        for item in cart.items.select_related("product"):
            item_price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            total += item_price * item.quantity

        cart_count = sum(item.quantity for item in cart.items.all())

        return JsonResponse(
            {
                "success": True,
                "quantity": cart_item.quantity,
                "subtotal": str(subtotal),
                "total": str(total),
                "cart_count": cart_count,
            }
        )


class DecreaseCartView(LoginRequiredMixin, View):
    def post(self, request, id):
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

            cart = Cart.objects.get(user=request.user)

            total = 0

            for item in cart.items.select_related("product"):
                item_price = (
                    item.product.discounted_price
                    if item.product.discounted_price
                    else item.product.price
                )

                total += item_price * item.quantity

            cart_count = sum(item.quantity for item in cart.items.all())

            return JsonResponse(
                {
                    "success": True,
                    "deleted": True,
                    "total": str(total),
                    "cart_count": cart_count,
                }
            )

        price = (
            cart_item.product.discounted_price
            if cart_item.product.discounted_price
            else cart_item.product.price
        )

        subtotal = price * cart_item.quantity

        cart = cart_item.cart

        total = 0

        for item in cart.items.select_related("product"):
            item_price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            total += item_price * item.quantity

        cart_count = sum(item.quantity for item in cart.items.all())

        return JsonResponse(
            {
                "success": True,
                "quantity": cart_item.quantity,
                "subtotal": str(subtotal),
                "total": str(total),
                "cart_count": cart_count,
            }
        )


class RemoveCartView(LoginRequiredMixin, View):
    def post(self, request, id):

        cart_item = CartItem.objects.get(id=id, cart__user=request.user)

        cart_item.delete()

        cart = Cart.objects.get(user=request.user)

        total = 0

        for item in cart.items.select_related("product"):
            item_price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            total += item_price * item.quantity

        cart_count = sum(item.quantity for item in cart.items.all())

        return JsonResponse(
            {
                "success": True,
                "deleted": True,
                "total": str(total),
                "cart_count": cart_count,
            }
        )


# closed add to cart view


# checkout view
class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):

        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            messages.warning(request, "Your cart is empty.")
            return redirect("cart")

        cart_items = cart.items.select_related("product")

        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect("cart")

        customer = Customer.objects.filter(user=request.user).first()

        subtotal = 0

        for item in cart_items:
            price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            item.subtotal = price * item.quantity
            subtotal += item.subtotal

        # shipping charge
        # Later we will make it dynamic based on district.
        if customer and customer.district == "Dhaka":
            shipping_charge = 60
        else:
            shipping_charge = 120

        total_amount = subtotal + shipping_charge

        return render(
            request,
            "shop/checkout.html",
            {
                "cart_items": cart_items,
                "customer": customer,
                "subtotal": subtotal,
                "shipping_charge": shipping_charge,
                "total_amount": total_amount,
            },
        )


# place order view
class PlaceOrderView(LoginRequiredMixin, View):
    def post(self, request):

        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("cart")

        cart_items = list(cart.items.select_related("product"))

        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect("cart")

        customer = Customer.objects.filter(user=request.user).first()

        if not customer:
            messages.warning(
                request, "Please complete your delivery information first."
            )
            return redirect("profile")

        # Calculate subtotal
        subtotal = 0

        for item in cart_items:
            price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            subtotal += price * item.quantity

        # Shipping charge
        if customer.district == "Dhaka":
            shipping_charge = 60
        else:
            shipping_charge = 120

        total_amount = subtotal + shipping_charge

        # Create order + order items together
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                customer=customer,
                subtotal=subtotal,
                shipping_charge=shipping_charge,
                total_amount=total_amount,
                status="pending",
            )

            for item in cart_items:
                price = (
                    item.product.discounted_price
                    if item.product.discounted_price
                    else item.product.price
                )

                item_subtotal = price * item.quantity

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=price,
                    subtotal=item_subtotal,
                )

            # Empty cart after successful order
            cart.items.all().delete()

        messages.success(request, f"Order #{order.id} placed successfully!")

        return redirect("order_success", order_id=order.id)


# order success view
class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request, order_id):

        order = (
            Order.objects.filter(id=order_id, user=request.user)
            .prefetch_related("items__product")
            .first()
        )

        if not order:
            messages.error(request, "Order not found.")
            return redirect("home")

        return render(
            request,
            "shop/order_success.html",
            {
                "order": order,
            },
        )

# about 
def about(request):
    return render(request, "shop/about.html")
def contact(request):
    return render(request, "shop/contact.html")