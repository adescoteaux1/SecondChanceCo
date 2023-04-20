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
    cursor.execute('SELECT first_name, last_name, sellerID, phone, email1 FROM Sellers')

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
    cursor.execute('select * from Sellers where SellerID = {0}'.format(sellerID))
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
@sellers.route('/seller/<sellerID>/post', methods=['GET'])
def get_most_posts(sellerID):
    cursor = db.get_db().cursor()
    query = 'SELECT productID, product_name, descr, unitPrice FROM Products WHERE sellerID = {0}'.format(sellerID)
    
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


#This adds a new post for a seller
@sellers.route('/seller/<sellerID>/products', methods=['POST'])
def add_post(sellerID):
    data = request.get_json()
    picture = data['picture']
    descr = data['descr']
    product_name = data['product_name']
    unitPrice = data['unitPrice']


    # insert the new post into the database
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Products (picture, descr, sellerID, product_name, unitPrice)
        VALUES (%s, %s, %s, %s, %s)
    '''
    values = (picture, descr, sellerID, product_name, unitPrice)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Post added successfully'})

# update email2 of the seller
@sellers.route('/seller/<sellerID>/email', methods=['PUT'])
def update_seller_email(sellerID):
    data = request.get_json()
    email2 = data['email2']

    # update the email address for the seller in the database
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Sellers
        SET email2 = %s
        WHERE sellerID = %s
    '''
    values = (email2, sellerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Seller email2 updated successfully'})



# This deleates a seller given a specific sellerID
@sellers.route('/seller/<sellerID>', methods=['DELETE'])
def delete_seller(sellerID):
    cursor = db.get_db().cursor()
    query = '''
    DELETE FROM Sellers
    WHERE sellerID = %s
    '''
    values = (sellerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Seller deleted successfully'})

# update post name, price, and decription
@sellers.route('/seller/<sellerID>/posts/<productID>', methods=['PUT'])
def update_post(sellerID, productID):
    data = request.get_json()
    product_name = data['product_name']
    unitPrice = data['unitPrice']
    description = data['descr']

    # update the post in the database
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Products
        SET product_name = %s, unitPrice = %s, descr = %s
        WHERE productID = %s AND sellerID = %s
    '''
    values = (product_name, unitPrice, description, productID, sellerID)
    cursor.execute(query, values)
    db.get_db().commit()

    # check if the post was updated
    if cursor.rowcount == 0:
        return jsonify({'message': 'Post not found for this seller'})

    return jsonify({'message': 'Post updated successfully'})


# delete a specifc post
@sellers.route('/seller/<sellerID>/posts/<productID>', methods=['DELETE'])
def delete_post(sellerID, productID):
    # delete the post from the database
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Products
        WHERE productID = %s AND sellerID = %s
    '''
    values = (productID, sellerID)
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({'message': 'Post deleted successfully'})

# connects seller ID and seller name
@sellers.route('/sellers/namepairs', methods=['GET'])
def seller_namepairs():
    cursor = db.get_db().cursor()
    query = ''' 
    SELECT sellerID as value, first_name as label
    From Sellers 
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