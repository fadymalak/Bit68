from rest_framework.serializers import ModelSerializer
from shop.models import Product, Cart, Order, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
