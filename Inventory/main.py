from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=config.HOST,
    port=config.PORT,
    password=config.PASSWORD,
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
     # return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk=pk)
    return {
        'id' : product.pk,
        'name' : product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.get("/products/{id}")
def get(id: str):
    return Product.get(pk=id)

@app.post("/products")
def create(product: Product):
    return product.save()

@app.delete("/products/{id}")
def delete(id: str):
    return Product.delete(pk=id)