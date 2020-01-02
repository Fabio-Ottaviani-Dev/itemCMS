import sys

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from utilities.errorhandler import http_error_handler
from auth.auth0 import AuthTest
from manage import Category, Item, db_drop_and_create_all

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
http_error_handler(app, jsonify)

# ----------------------------------------------------------------------------
# db_drop_and_create
# ----------------------------------------------------------------------------

@app.route('/reset-db')
def reset_db():
    db_drop_and_create_all()
    return jsonify({
        'success': True,
        'message': 'db_drop_and_create_all @DONE!'
    }), 200

# ----------------------------------------------------------------------------
# sys.path TEST
# ----------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def hello_dude():
	return jsonify({'sys.path':sys.path, 'message':'Hello, Dude - Test N. 05'})

# ----------------------------------------------------------------------------
# Auth TEST
# ----------------------------------------------------------------------------
@app.route('/auth')
def test_auth():
	return jsonify(AuthTest())
# ----------------------------------------------------------------------------
# Read >> items TEST
# ----------------------------------------------------------------------------

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.order_by(Item.name).all()
    data  = db.session.query(Item, Category).filter(Item.category_id == Category.id)
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
