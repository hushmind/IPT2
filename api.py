from flask import Flask, make_response, jsonify, request, Response
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import dicttoxml
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin"
app.config["MYSQL_DB"] = "online_selling"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['JWT_SECRET_KEY'] = 'aAbBcCdDeEfFgGhIjJ200ok'  # Change this to a random secret key

mysql = MySQL(app)
jwt = JWTManager(app)

# Helper function to convert data to the desired format
def output_format(data, format='json'):
    if format == 'xml':
        xml_data = dicttoxml.dicttoxml(data, custom_root='result', attr_type=False)
        # Convert XML to string and prettify
        xml_pretty = ET.tostring(ET.fromstring(xml_data), encoding='utf8', method='xml')
        return Response(xml_pretty, mimetype='application/xml')
    else:  # Default to JSON
        return jsonify(data)

# Helper function to fetch data with parameters to prevent SQL injection
def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    data = cur.fetchall()
    cur.close()
    return data

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # TODO: Validate username and password against your user database
    if username == 'admin' and password == 'aAbBcCdDeEfFgGhIjJ200ok':  # Replace with real user validation
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

# Product Routes
@app.route("/products", methods=["GET"])
def get_products():
    format = request.args.get('format', default='json').lower()
    search_query = request.args.get('search', default='')
    query = "SELECT * FROM Product WHERE product_name LIKE %s"
    data = data_fetch(query, ('%' + search_query + '%',))
    return output_format(data, format)

@app.route("/products", methods=["POST"])
def add_product():
    cur = mysql.connection.cursor()
    info = request.get_json()
    product_ID = info["product_ID"]
    product_name = info["product_name"]
    price = info["price"]
    cur.execute(
        "INSERT INTO Product (product_ID, product_name, price) VALUES (%s, %s, %s)",
        (product_ID, product_name, price)
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "Product added successfully", "rows_affected": rows_affected}), 201)

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    info = request.get_json()
    product_name = info["product_name"]
    price = info["price"]
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE Product SET product_name = %s, price = %s WHERE product_ID = %s",
        (product_name, price, product_id)
    )
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "Product updated successfully"}), 200)

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Product WHERE product_ID = %s", (product_id,))
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "Product deleted successfully"}), 200)

# User Routes
@app.route("/users", methods=["GET"])
def get_users():
    format = request.args.get('format', default='json').lower()
    search_query = request.args.get('search', default='')
    query = "SELECT * FROM User WHERE Username LIKE %s"
    data = data_fetch(query, ('%' + search_query + '%',))
    return output_format(data, format)

@app.route("/users", methods=["POST"])
def add_user():
    cur = mysql.connection.cursor()
    info = request.get_json()
    User_ID = info["User_ID"]
    Username = info["Username"]
    Email = info["Email"]
    cur.execute(
        "INSERT INTO User (User_ID, Username, Email) VALUES (%s, %s, %s)",
        (User_ID, Username, Email)
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "User added successfully", "rows_affected": rows_affected}), 201)

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    info = request.get_json()
    username = info["username"]
    email = info["email"]
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE User SET Username = %s, Email = %s WHERE User_ID = %s",
        (username, email, user_id)
    )
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "User updated successfully"}), 200)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM User WHERE User_ID = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "User deleted successfully"}), 200)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)