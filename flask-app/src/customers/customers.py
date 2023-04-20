from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select first_name, last_name, customerID\
        , phone, email1, city, state, country, zip from Customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<customerID>', methods=['GET'])
def get_customer(customerID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Customers where customerID = {0}'.format(customerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete a customer with a particular customerID
@customers.route('/customers/<customerID>', methods=['DELETE'])
def customer_delete(customerID):
    # delete customer from database
    cursor = db.get_db().cursor()
    query = ''' 
    DELETE FROM Customers 
    WHERE customerID = %s
    ''' 
    values = (customerID,)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Customer deleted successfully'})

# Connects customer name and customer id 
@customers.route('/customers/namepairs', methods=['GET'])
def customer_namepairs():
    cursor = db.get_db().cursor()
    query = ''' 
    SELECT customerID as value, first_name as label
    From Customers 
    ''' 
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Connects product name and product id 
@customers.route('/customers/products/namepairs', methods=['GET'])
def product_namepairs():
    cursor = db.get_db().cursor()
    query = ''' 
    SELECT productID as value, product_name as label
    From Products 
    ''' 
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get the total price of a customer's cart with particular customerID
@customers.route('/customers/<customerID>/cart', methods=['GET'])
def get_cart(customerID):
    cursor = db.get_db().cursor()
    query = '''SELECT (round(sum(db.unitPrice), 2)) AS "TotalPrice"
    FROM (SELECT DISTINCT prod_carts.productID, unitPrice
    FROM prod_carts
    JOIN Products P on prod_carts.productID = P.productID
    WHERE cartID = (SELECT Cart.cartID FROM Cart where customerID = %s)) AS db;'''
    values = (customerID)
    cursor.execute(query, values)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# View customer's cart with particular customerID
@customers.route('/customers/<customerID>/viewcart', methods=['GET'])
def get_viewcart(customerID):
    cursor = db.get_db().cursor()
    query = '''SELECT pc.productID AS "ProductID", P.product_name AS "Name", P.descr AS "Description", P.picture AS "Photolink", P.unitPrice AS "uPrice"
    FROM Cart
    JOIN prod_carts pc on Cart.cartID = pc.cartID
    JOIN Products P on pc.productID = P.productID
    where customerID = %s
    '''
    values = (customerID)
    cursor.execute(query, values)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# not sure if this works
# add a new product into a customers cart
@customers.route('/customers/<customerID>/cart', methods=['POST'])
def add_to_cart(customerID):
    data = request.get_json()
    productID = data['productID']
    cursor = db.get_db().cursor()
    query = 'INSERT INTO prod_carts (productID, cartID) VALUES (%s, (SELECT cartID FROM Cart WHERE customerID = %s))'
    values = (productID, customerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Product added successfully'})

# Delete a product from a customers cart
@customers.route('/customers/<customerID>/cart/<productID>', methods=['DELETE'])
def cart_product_delete(customerID, productID):
    cursor = db.get_db().cursor()
    query = '''DELETE FROM prod_carts
    WHERE cartID = (SELECT Cart.cartID FROM Cart where customerID = %s) and productID = %s;
    '''
    values = (customerID, productID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Item deleted from cart successfully'})

# Get a specific customers orders
@customers.route('/customers/<customerID>/orders', methods=['GET'])
def get_orders(customerID):
    cursor = db.get_db().cursor()
    cursor.execute('select orderID from Orders where customerID = {0}'.format(customerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# adds a new order for a customer
@customers.route('/customers/<customerID>/orders', methods=['POST'])
def add_order(customerID):
    data = request.get_json()
    city = data['city']
    state = data['state']
    country = data['country']
    zip = data['zip']
    # insert the new post into the database
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Orders (statusID, city, state, country, zip, customerID)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (0, city, state, country, zip, customerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Order made successfully'})


# update address of the customer
@customers.route('/customers/<customerID>/address', methods=['PUT'])
def update_customer_address(customerID):
    data = request.get_json()
    city = data['city']
    state = data['state']
    country = data['country']
    zip = data['zip']

    # update the address for the customer in the database
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Customers
        SET city = %s, state = %s, country = %s, zip = %s
        WHERE customerID = %s 
    '''
    values = (city, state, country, zip, customerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Customer address updated successfully'})

# Get all Products
@customers.route('/customer/products', methods=['GET'])
def get_products():
    cursor = db.get_db().cursor()
    cursor.execute('select productID, product_name, descr, picture, unitPrice, first_name, last_name\
    from Products join Sellers using (sellerID)')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response