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
    cursor.execute('select * from customers where customerID = {0}'.format(customerID))
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
    cursor = db.get_db().cursor()
    query = 'DELETE FROM customers WHERE customerID = {0}'.format(customerID)
    values = (customerID,)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Customer deleted successfully'})

# Get the total price of a customer's cart with particular customerID
@customers.route('/customers/<customerID>/<cart>', methods=['GET'])
def get_cart(customerID):
    cursor = db.get_db().cursor()
    cursor.execute('select total_price from cart where customerID = {0}'.format(customerID))
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
    cartID = data['cartID']

    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO cart join prod_carts (productID, cartID)
        VALUES (%s, %s)
        Where customerID = {0}'.format(customerID)
    '''
    values = (productID, cartID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Product added successfully'})

# Delete a product from a customers cart
@customers.route('/customers/<customerID>/<cart>/<productID>', methods=['DELETE'])
def cart_product_delete(customerID, productID):
    cursor = db.get_db().cursor()
    query = '''
    DELETE FROM cart join prod_carts 
    WHERE customerID = {0}'.format(customerID) and productID = {0}'.format(productID)
    '''
    values = (productID,)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Item deleted from cart successfully'})

# Get a specific customers orders
@customers.route('/customers/<customerID>/<orders>', methods=['GET'])
def get_orders(customerID):
    cursor = db.get_db().cursor()
    cursor.execute('select orderID from orders where customerID = {0}'.format(customerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete a customer with the specified customerID
@customers.route('/customers/<customerID>', methods=['DELETE'])
def delete_customer(customerID,):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM customers customerID = {0}'.format(customerID)
    values = (customerID,)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Customer deleted successfully'})

# adds a new order for a customer
@customers.route('/customers/<customerID>/orders', methods=['POST'])
def add_order(customerID):
    data = request.get_json()
    statusID = data['statusID']
    order_date = data['order_date']
    city = data['city']
    state = data['state']
    country = data['country']
    zip = data['unitPrice']
    customerID = data['customerID']
    managerID = data['managerID']
    orderID = data['orderID']


    # insert the new post into the database
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO orders (statusID, order_date, city, state, country, zip, customerID, managerID, orderID)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    values = (statusID, order_date, city, state, country, zip, customerID, managerID, orderID)
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