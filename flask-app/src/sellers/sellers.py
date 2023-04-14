from flask import Blueprint, request, jsonify, make_response
import json
from src import db


sellers = Blueprint('sellers', __name__)

# Get all the sellers from the database
@sellers.route('/sellers', methods=['GET'])
def get_sellers():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT first_name, last_name, sellerID, phone, email1 FROM products')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Get details for a specific seller with particular userID
@sellers.route('/seller/<sellerID>', methods=['GET'])
def get_seller(sellerID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from sellers where SellerID = {0}'.format(SellerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# get all the posts from a specific seller
@sellers.route('/mostExpensive')
def get_most_posts(sellerID):
    cursor = db.get_db().cursor()
    query = '''
        SELECT product_name, unitPrice 
        FROM products
        WHERE sellerID = {0}'.format(SellerID)
    '''
    cursor.execute(query)
       # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


