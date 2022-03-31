from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time
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
    # password=config.PASSWORD,
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str #pending, completed, refunding

    class Meta:
        database = redis

@app.get('/orders/{pk}')
def get(pk: str):
    # order = Order.get(pk)
    # redis.xadd('refund_order',order.dict(),'*')
    # return order
    return Order.get(pk)

@app.post("/orders")
async def create(request: Request):
    # request: id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])

    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    order_completed(order)

    return order

def order_completed(order: Order):
    time.sleep(5)
    # stop 5 seconds --> wait to be processed
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')    # '*' --> auto-generated ID
