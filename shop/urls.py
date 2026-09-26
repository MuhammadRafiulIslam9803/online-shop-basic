from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.ProductView.as_view(), name="home"),
    path("product/<int:id>/", views.ProductDetailsView.as_view(), name="productDetails"),
    path("category/<str:category>/", views.categoryView.as_view(), name="categoryProducts"),
    path("registration/", views.CustomerRegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
