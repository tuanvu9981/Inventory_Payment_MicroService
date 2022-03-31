### Payment of the micro-service system

* Requirements: 
    * redis-om (which requires python >= 3.7)
    * fastAPI 
    
* After installing python3.9, Pycharm using python3.9 as main interpreter **COULDN'T** create its own virtual environment. 
* Solution: 
```
sudo apt-get install python3-distutils
```

* Starting app with command: 
```
uvicorn main:app --reload --port=8001
```

* Redis Stream
  * Processing an order will take 5 seconds. If we delete **ORDERED** product within this 5 seconds,
  the customer will HAVE TO PAY FOR **A NOT EXISTING PRODUCT**
    
  * Inventory: Before subtract the number of ordered products, we need to check if exists.
  ```                
  try:
     product = Product.get(obj['project_id'])
     product.quantity -= int(obj['quantity'])
     product.save()
  except:
     redis.xadd('refund_order', obj, '*')
  ```

  * If ORDERED product doesn't exist, we'll send the received object of Order to the stream **refund_order**.
  The Payment Micro-Service, which is listening to this stream, will catch and process this, then change status of ORDER to **REFUND**, which means customers dont have to pay for a non-exist product.