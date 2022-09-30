from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from shop.serializers import (
    ProductSerializer,
    OrderSerializer,
    CartSerializer,
    UserSerializer,
)
from rest_framework import status
from django.contrib.auth import authenticate, login

# Create your views here.
from django_filters import rest_framework as filter
from shop.models import Product, Cart, Order


class ProductFilter(filter.FilterSet):
    name = filter.CharFilter(field_name="name", lookup_expr="contains")
    sorting = filter.OrderingFilter(fields=(("price", "price")))

    class Meta:
        model = Product
        exclude = [
            "price",
        ]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action == "create":
            return [
                IsAdminUser(),
            ]
        return [
            IsAuthenticated(),
        ]


class CartViewSet(ViewSet):
    def get(self, request, pk=None):
        """get User cart"""
        user = request.user
        instance = Cart.objects.get(user=user)
        serializer = CartSerializer(instance)
        return Response(serializer.data)

    def partial_update(self, request):

        user = request.user
        data = request.data
        print(data)
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        obj = ProductSerializer(data=data)
        obj.is_valid(raise_exception=True)
        product = Product.objects.get(id=data.get("id"))
        cart.products.add(product)
        return Response(obj.data, status=status.HTTP_201_CREATED)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        user = request.user
        cart = Cart.objects.prefetch_related("products").get(user=user)
        order = Order.objects.create(user=user)
        order.products.set(cart.products.all())
        cart.products.clear()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user).all()
        serializer = OrderSerializer(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
def register_user(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_user(request):
    data = request.data
    username = data.get("username", None)
    password = data.get("password", None)
    if username is None or password is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
