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

# needs to be done
# Put a new product into a customers cart
@customers.route('/customers/<customerID>', methods=['PUT'])
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

# Delete a product from a customers cart
@customers.route('/customers/<customerID>/<cart>/<productID>', methods=['DELETE'])
def cart_product_delete(customerID, productID):
    cursor = db.get_db().cursor()
    query = '''
    DELETE FROM customers join cart join prod_carts 
    WHERE customerID = {0}'.format(customerID) and productID = {0}'.format(productID)
    '''
    values = (productID,)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Item deleted from cart successfully'})

# Get a specific customers orders
@customers.route('/customers/<customerID>/<orders>', methods=['GET'])