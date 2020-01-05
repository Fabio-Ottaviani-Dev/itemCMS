import sys
from flask import Flask, request, abort, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from utilities.errorhandler import http_error_handler
#from auth.auth0 import AuthTest
from auth.auth import AuthError, requires_auth
from manage import Category, Item, db_drop_and_create_all

from datetime import datetime
now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
http_error_handler(app, jsonify)

# ----------------------------------------------------------------------------
# Set up CORS and CORS Headers
# ----------------------------------------------------------------------------

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE')
    return response

# ----------------------------------------------------------------------------
# db_drop_and_create
# ----------------------------------------------------------------------------

@app.route('/reset-db', methods=['GET'])
def reset_db():
    db_drop_and_create_all()
    return jsonify({
        'success': True,
        'message': 'db_drop_and_create_all: --> {} @DONE! '.format(date_time)
    }), 200

# ----------------------------------------------------------------------------
# index / sys.path TEST
# ----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def hello_dude():
	return jsonify({
        'sys.path': sys.path,
        'message': 'Hello, datetime: - {}'.format(date_time)
    }), 200

# ----------------------------------------------------------------------------
# Auth TEST
# ----------------------------------------------------------------------------
# @app.route('/auth', methods=['GET'])
# def test_auth():
# 	return jsonify(AuthTest())
# ----------------------------------------------------------------------------

@app.route('/login-results', methods=['GET'])
def login_results():
    return jsonify({
        'success':  True,
        'access_token info': 'Look on the address bar and grab your access token from the url'
    }), 200

# ----------------------------------------------------------------------------
# Create >> Category
# ----------------------------------------------------------------------------
# @TEST
    # OK 201 | curl -X POST -H "Content-Type: application/json" -d '{"name":"New Category N. 3"}' http://127.0.0.1:5000/categories
    # OK 400 | curl -X POST -H "Content-Type: application/json" -d '{"id":"100"}' http://127.0.0.1:5000/categories
# **DONE**
# ----------------------------------------------------------------------------

@app.route('/categories', methods=['POST'])
# @requires_auth('create:category')
# pass: --> payload
def create_category():

    name = request.json.get('name', None)

    if name is None:
        abort(400)

    try:
        category = Category(name = name)
        category.insert()

        return jsonify({
            'success':  True,
            'category': category.format()
        }), 201 # 201=Created

    except:
        abort(422)

# ----------------------------------------------------------------------------
# Read >> All Categories
# ----------------------------------------------------------------------------
# @TEST
    # OK 200 | curl -X GET http://127.0.0.1:5000/categories
# ----------------------------------------------------------------------------

@app.route('/categories', methods=['GET'])
def get_all_categories():

    categories      = Category.query.order_by(Category.id).all()
    result          = [category.format() for category in categories]
    total_results   = len(categories)

    if total_results == 0:
        abort(404)

    return jsonify({
        'success':          True,
        'categories':       result,
        'total_categories': total_results
    }), 200

# ----------------------------------------------------------------------------
# Update >> Categories
# ----------------------------------------------------------------------------
# @TEST
    # OK 404 | curl -X PATCH -H "Content-Type: application/json" -d '{"name":"New Category N. 3 REV"}' http://127.0.0.1:5000/categories/99
    # OK 400 | curl -X PATCH -H "Content-Type: application/json" -d '{"Name":"New Category N. 3 REV"}' http://127.0.0.1:5000/categories/3
    # OK 200 | curl -X PATCH -H "Content-Type: application/json" -d '{"name":"New Category N. 3 REV"}' http://127.0.0.1:5000/categories/3
# **DONE**
# ----------------------------------------------------------------------------

@app.route('/categories/<int:category_id>', methods=['PATCH'])
# @requires_auth('update:category')
# pass: --> payload
def update_category(category_id):

    category = Category.query.get_or_404(category_id)

    name = request.json.get('name', None)

    if name is None:
        abort(400)

    try:
        if name:
            category.name = name

        category.update()
    except:
        abort(400)

    response = category.format()

    return jsonify({
        'success':  True,
        'category': response
    }), 200

# ----------------------------------------------------------------------------
# Delete >> Category
# ----------------------------------------------------------------------------
# @TODO: (if it is not associated with any items)
# @TEST
    # OK 404 | curl -X DELETE http://127.0.0.1:5000/categories/99
    # OK 200 | curl -X DELETE http://127.0.0.1:5000/categories/6
# ----------------------------------------------------------------------------

@app.route('/categories/<int:category_id>', methods=['DELETE'])
# @requires_auth('delete:category')
# pass: --> payload
def delete_category(category_id):

    category = Category.query.get_or_404(category_id)

    try:
        category.delete()
    except exc.SQLAlchemyError:
        abort(500)

    return jsonify({
        'success':  True,
        'delete':   category_id
    }), 200

# ----------------------------------------------------------------------------
# Create >> Item
# ----------------------------------------------------------------------------
# @TODO: check if category_id exist then insert
# @TEST
    # OK 201
    # curl -X POST -H "Content-Type: application/json" -d '{
    #   "category_id":"2",
    #   "name":"New Item curl Test 2",
    #   "description":"New Item curl Test 2 > description",
    #   "price":"210"
    # }' http://127.0.0.1:5000/items

    # OK 400
    # curl -X POST -H "Content-Type: application/json" -d '{
    #   "category_id":"2",
    #   "description":"New Item curl Test 2 > description",
    #   "price":"210"
    # }' http://127.0.0.1:5000/items
# **DONE**
# ----------------------------------------------------------------------------

@app.route('/items', methods=['POST'])
# @requires_auth('create:item')
# pass: --> payload
def create_item():

    category_id     = request.json.get('category_id', None)
    name            = request.json.get('name', None)
    description     = request.json.get('description', None)
    price           = request.json.get('price', None)

    if category_id is None or name is None or description is None or price is None:
        abort(400)

    try:

        item = Item(
            category_id = category_id,
            name        = name,
            description = description,
            price       = price
        )

        item.insert()

        return jsonify({
            'success':  True,
            'item': item.format()
        }), 201 # 201=Created

    except:
        abort(422)

# ----------------------------------------------------------------------------
# Read >> items TEST
# https://stackoverflow.com/questions/11530196/flask-sqlalchemy-query-specify-column-names
# ----------------------------------------------------------------------------

@app.route('/items', methods=['GET'])
def get_items():

    items = Item.query.order_by(Item.name).all()

    data = db.session.query(
        Item.id,
        Category.name.label('category'),
        Item.name,
        Item.description,
        Item.price
    ).filter(Item.category_id == Category.id).all()

    print("\n\n items : -->", items[0])
    # RETURN: items : --> <class 'manage.Item'>: {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x110c56610>, 'description': 'Lorem ipsum dolor sit amet - Item 01 AA', 'name': 'Item 01 AA', 'id': 1, 'price': 110, 'category_id': 1}

    print("\n\n data : -->", data[0])
    # RETURN: data : --> (1, 'Category 01 AA', 'Item 01 AA', 'Lorem ipsum dolor sit amet - Item 01 AA', 110)

    result = [item.format() for item in items]
    total_results = len(items)

    if total_results == 0:
        abort(404)

    return jsonify({
        'success':  True,
        'items':   result
    }), 200

# ----------------------------------------------------------------------------
# Update >> Item
# @TEST
# OK 201
    # curl -X PATCH -H "Content-Type: application/json" -d '{
    #   "category_id":"2",
    #   "name":"Item Update, curl Test PATCH id 1",
    #   "description":"Item Update, curl Test PATCH id 1 description",
    #   "price":"210"
    # }' http://127.0.0.1:5000/items/1

# OK 404 with item_id = 10000
# OK 400 & 500
# ----------------------------------------------------------------------------

@app.route('/items/<int:item_id>', methods=['PATCH'])
# @requires_auth('update:item')
# pass: --> payload
def update_item(item_id):

    item = Item.query.get_or_404(item_id)

    try:
        category_id     = request.json.get('category_id', None)
        name            = request.json.get('name', None)
        description     = request.json.get('description', None)
        price           = request.json.get('price', None)

        if category_id is None or name is None or description is None or price is None:
            abort(400)

        item.category_id    = category_id
        item.name           = name
        item.description    = description
        item.price          = price
        item.name           = name

        item.update()
        response = item.format()

        return jsonify({
            'success':  True,
            'category': response
        }), 200

    except exc.SQLAlchemyError:
        db.session.rollback()
        abort(500)
    except:
        db.session.rollback()
        abort(400)
    finally:
        db.session.close()

# ----------------------------------------------------------------------------
# Delete >> Item
    # OK 404 | curl -X DELETE http://127.0.0.1:5000/items/99
    # OK 200 | curl -X DELETE http://127.0.0.1:5000/items/1


@app.route('/items/<int:item_id>', methods=['DELETE'])
# @requires_auth('delete:item')
# pass: --> payload
def delete_item(item_id):

    item = Item.query.get_or_404(item_id)

    try:
        item.delete()
    except exc.SQLAlchemyError:
        abort(500)

    return jsonify({
        'success':  True,
        'delete':   item_id
    }), 200

# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app.run(host='0.0.0.0')
