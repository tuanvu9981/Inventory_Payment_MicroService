from main import Product, redis
import time

key = 'order_completed'
group = 'inventory_group'

try:
    redis.xgroup_create(key,group)
    # def xgroup_create(self, name: KeyT, groupname: GroupT, id: StreamIdT = "$", mkstream: bool = False) -> ResponseT:
except:
    print('Group already exists')

while True:
    try:
        results = redis.xreadgroup(group,key,{key: '>'}, None)
        # print(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                # product = Product.get(obj['project_id'])
                # NOT FOUND --> return HashModel --> None ?

                # if product:
                #     print(product)
                #     product.quantity -= int(obj['quantity'])
                #     product.save()
                # else:
                #     redis.xadd('refund_order', obj, '*')

                try:
                    product = Product.get(obj['project_id'])
                    product.quantity -= int(obj['quantity'])
                    product.save()
                except:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
