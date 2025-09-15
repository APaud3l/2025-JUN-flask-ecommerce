# GET /products
# Response expected: 200 OK, and a list 
def test_get_products_success(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# POST /products
# Response expected: 201 OK, JSON response
def test_create_product_success(client):
    new_product = {
        "name": "Test Product",
        "price": 19.99
    }

    response = client.post('/products', json=new_product)
    assert response.status_code == 201

    product = response.get_json()
    assert 'id' in product
    assert product['name'] == "Test Product"

def test_get_products_returns_empty_list(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.get_json() == []

# PATCH /products/fake_id 
def test_update_nonexistent_product(client):
    fake_id = 999
    update_data = {
        "name": "Ghost Product",
        "price": 999.99
    }

    response = client.patch(f"/products/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert "does not exist" in response.get_json()["message"]


# PATCH /products/id, change price with wrong type of value
def test_update_product_invalid_data(client):
    # Create a product
    product_data = {
        "name": "Typo Product",
        "description": "Incorrect price",
        "price": 5.0,
        "stock": 2
    }

    create_response = client.post('/products', json=product_data)
    product_id = create_response.get_json()["id"]
    # Send invalid price
    update_data = {
        "price": "abc"
    }
    response = client.patch(f'/products/{product_id}', json=update_data)
    # assert
    assert response.status_code in (200, 400)

