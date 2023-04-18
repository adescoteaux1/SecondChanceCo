from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select first_name, last_name, customerID\
        , phone, email1 from Customers')
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

# Get the total price of a customer's cart with particular customerID
@customers.route('/customers/<customerID>/cart', methods=['GET'])
def get_cart(customerID):
    cursor = db.get_db().cursor()
    cursor.execute('select total_price from Cart where customerID = {0}'.format(customerID))
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
    query = '''SELECT pc.productID AS "Product ID", P.product_name AS "Name", P.descr AS "Description", P.picture AS "Link to Photo"
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
    query = 'INSERT INTO prod_carts (productID, cartID) VALUES (%s, (SELECT cartID FROM Cart WHERE customerID = {0}))'.format(customerID)
    values = (productID,)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Product added successfully'})

# Delete a product from a customers cart
@customers.route('/customers/<customerID>/<cart>/<productID>', methods=['DELETE'])
def cart_product_delete(customerID, productID):
    cursor = db.get_db().cursor()
    query = '''
    DELETE FROM Cart join prod_carts 
    WHERE customerID = {0}'.format(customerID) and productID = {0}'.format(productID)
    '''
    values = (productID,)
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
    zip = data['unitPrice']
    # insert the new post into the database
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO orders (statusID, city, state, country, zip, customerID)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (0, city, state, country, zip, customerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Order made successfully'})


# update address of the customer
@customers.route('/customer/<customerID>/email', methods=['PUT'])
def update_customer_address(customerID):
    data = request.get_json()
    city = data['city']
    state = data['state']
    country = data['country']
    zip = data['unitPrice']

    # update the address for the customer in the database
    cursor = db.get_db().cursor()
    query = '''
        UPDATE customers
        SET city = %s, state = %s, country = %s, zip = %s
        WHERE customerID = {0}'.format(customerID)
    '''
    values = (city, state, country, zip, customerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Customer address updated successfully'})

# Get all Products
@customers.route('/customer/products', methods=['GET'])
def get_products():
    cursor = db.get_db().cursor()
    cursor.execute('select product_name, unitPrice, picture, descr, first_name, last_name\
        from Products join Sellers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response