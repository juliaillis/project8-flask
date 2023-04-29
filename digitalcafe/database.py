import pymongo
import database as db

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

if "branches" in products_db.list_collection_names():
    products_db["branches"].drop()

branches = [
    {"code": "1", "name": "Katipunan"},
    {"code": "2", "name": "Tomas Morato"},
    {"code": "3", "name": "Eastwood"},
    {"code": "4", "name": "Tiendesitas"},
    {"code": "5", "name": "Arcovia"}
]

products_db["branches"].insert_many(branches)

branches = {
    1: {"name":"Katipunan","phonenumber":"09179990000"},
    2: {"name":"Tomas Morato","phonenumber":"09179990001"},
    3: {"name":"Eastwood","phonenumber":"09179990002"},
    4: {"name":"Tiendesitas","phonenumber":"09179990003"},
    5: {"name":"Arcovia","phonenumber":"09179990004"},
}

def get_product(code):
    products_coll = products_db["products"]

    product = products_coll.find_one({"code":code})

    return product

def get_products():
    product_list = []

    products_coll = products_db["products"]

    for p in products_coll.find({}):
        product_list.append(p)

    return product_list

def get_branch(code):
    branches_coll = products_db["branches"]

    branch = branches_coll.find_one({"code": code})

    return branch

def get_branches():
    branch_list = []

    branches_coll = products_db["branches"]

    for b in branches_coll.find({}):
        branch_list.append(b)

    return branch_list

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

def get_past_orders(user_id):
    orders = db.orders.find({'user_id': user_id, 'status': 'complete'})
    return [Order(o['date'], o['total']) for o in orders]

class Order:
    def __init__(self, date, total):
        self.date = date
        self.total = total
