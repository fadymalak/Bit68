from shop.models import Cart, Product

# Create your tests here.
import pytest


def create_products():
    return Product.objects.bulk_create(
        [
            Product(name="product1", price=11),
            Product(name="product2", price=12),
            Product(name="product3", price=13),
            Product(name="product4", price=14),
        ]
    )


@pytest.mark.django_db
def test_x():
    assert 1 == 1


@pytest.mark.django_db
def test_get_order_list_empty(API):
    req = API.get("/orders/", format="json")
    assert req.status_code == 200
    assert req.data == []


@pytest.mark.django_db
def test_add_to_cart(API):
    products = create_products()

    req = API.patch(
        "/cart/",
        data={
            "id": products[0].id,
            "name": products[0].name,
            "price": products[0].price,
        },
    )
    assert req.status_code == 201
    assert req.data["name"] == products[0].name


@pytest.mark.django_db
def test_get_cart(API):
    products = create_products()

    cart = Cart.objects.all()[0]
    cart.products.add(products[0])
    req = API.get("/cart/")
    print(req.status_code)
    assert req.status_code == 200
    assert req.data["products"] == [
        products[0].id,
    ]


@pytest.mark.django_db
def test_create_order(API):
    products = create_products()

    cart = Cart.objects.all()[0]
    cart.products.add(products[0])
    req = API.post("/orders/")
    print(req.status_code)
    assert req.status_code == 201
    assert req.data["products"] == [
        products[0].id,
    ]


@pytest.mark.django_db
def test_get_order_list(API):
    products = create_products()

    cart = Cart.objects.all()[0]
    cart.products.add(products[0])
    req = API.post("/orders/")
    req = API.get("/orders/")
    print(req.status_code)
    assert req.status_code == 200
    assert len(req.data) == 1


@pytest.mark.django_db
def test_list_products(API):
    create_products()
    req = API.get("/products/")
    assert req.status_code == 200
    assert len(req.data) == 4


@pytest.mark.django_db
def test_create_products_non_admin(API):
    req = API.post("/products/", data={"name": "product5", "price": 15})
    assert req.status_code == 403


@pytest.mark.django_db
def test_create_products_admin(API_ADMIN):
    req = API_ADMIN.post("/products/", data={"name": "product5", "price": 15})
    assert req.status_code == 201
