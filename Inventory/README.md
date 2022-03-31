### Inventory of the micro-service system

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
uvicorn main:app --reload 
```
* Redis Stream

  * After an order is processed, it will send an Order object to stream **order_completed**
  ```
  def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
  ```
  
  * The Inventory micro-service, which is listening to this stream, will:
    * Catch the Order object
    * Get the product_id inside Order object 
    * Subtract the quantity of corresponding product inside the Inventory 