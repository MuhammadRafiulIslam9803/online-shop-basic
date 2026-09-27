from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import (
    LoginForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm,
)

urlpatterns = [
    # Home URL
    path("", views.ProductView.as_view(), name="home"),
    
    # Product URL
    path(
        "product/<int:id>/", views.ProductDetailsView.as_view(), name="productDetails"
    ),
    
    # Category URL
    path(
        "category/<str:category>/",
        views.categoryView.as_view(),
        name="categoryProducts",
    ),
    
    # Registration URL
    path(
        "registration/", views.CustomerRegistrationView.as_view(), name="registration"
    ),
    
    # Login URL
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="shop/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    
    # Logout URL
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    
    # password change urls
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="shop/password_change.html",
            form_class=MyPasswordChangeForm,
            success_url="/password_change/done/",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="shop/password_change_done.html"
        ),
        name="password_change_done",
    ),
    
    # password reset urls
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="shop/password_reset.html",
            form_class=MyPasswordResetForm,
            email_template_name="shop/password_reset_email.html",
            subject_template_name="shop/password_reset_subject.txt",
            success_url="/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="shop/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="shop/password_reset_confirm.html",
            form_class=MySetPasswordForm,
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="shop/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
