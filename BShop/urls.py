"""BShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop.views import (
    ProductViewSet,
    OrderViewSet,
    CartViewSet,
    register_user,
    login_user,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("create/", register_user),
    path("login/", login_user),
    path("cart/", CartViewSet.as_view({"get": "get", "patch": "partial_update"})),
]
urlpatterns += router.urls
