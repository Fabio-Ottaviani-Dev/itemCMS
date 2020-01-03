import sys
from flask import Flask, request, abort, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from utilities.errorhandler import http_error_handler
from auth.auth0 import AuthTest
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

@app.route('/reset-db')
def reset_db():
    db_drop_and_create_all()
    return jsonify({
        'success': True,
        'message': 'db_drop_and_create_all: --> {} @DONE! '.format(date_time)
    }), 200

# ----------------------------------------------------------------------------
# Create >> Category
# ----------------------------------------------------------------------------
# @TEST
    # OK 201 | curl -X POST -H "Content-Type: application/json" -d '{"name":"New Category N. 3"}' http://127.0.0.1:5000/categories
    # OK 400 | curl -X POST -H "Content-Type: application/json" -d '{"id":"100"}' http://127.0.0.1:5000/categories
# **DONE**

@app.route('/categories', methods=['POST'])
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

@app.route('/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id):

    name = request.json.get('name', None)

    if name is None:
        abort(400)

    category = Category.query.get_or_404(category_id)

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
# @TEST
    # OK 404 | curl -X DELETE http://127.0.0.1:5000/categories/99
    # OK 200 | curl -X DELETE http://127.0.0.1:5000/categories/6

@app.route('/categories/<int:category_id>', methods=['DELETE'])
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
# sys.path TEST
# ----------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def hello_dude():
	return jsonify({'sys.path':sys.path, 'message':'Hello, Dude - {}'.format(date_time)})

# ----------------------------------------------------------------------------
# Auth TEST
# ----------------------------------------------------------------------------
@app.route('/auth')
def test_auth():
	return jsonify(AuthTest())
# ----------------------------------------------------------------------------
# Read >> items TEST
# https://stackoverflow.com/questions/11530196/flask-sqlalchemy-query-specify-column-names
# ----------------------------------------------------------------------------

@app.route('/items', methods=['GET'])
def get_items():

    items1 = Item.query.order_by(Item.name).all()

    #data1  = db.session.query(Item, Category).filter(Item.category_id == Category.id)

    # data2 = db.session.query(
    #     Item.id,
    #     Category.name.label('category'),
    #     Item.name,
    #     Item.description,
    #     Item.price
    # ).filter(Item.category_id == Category.id)

    items = db.session.query(Item, Category).filter(Item.category_id == Category.id).all()

    result = [item.format() for item in items]

    total_results = len(items)

    if total_results == 0:
        abort(404)

    return jsonify({
        'success':  True,
        'items':   result
    }), 200

# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app.run(host='0.0.0.0')
