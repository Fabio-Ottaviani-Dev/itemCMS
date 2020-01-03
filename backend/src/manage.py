# Doc: https://flask-migrate.readthedocs.io/en/latest/

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# ----------------------------------------------------------------------------
# db_drop_and_create_all, data
# ----------------------------------------------------------------------------

def db_drop_and_create_all():

    db.drop_all()
    db.create_all()

    db.session.add(Category(id = 1, name = "Category 01 AA"))
    db.session.add(Category(id = 2, name = "Category 02 BB"))
    db.session.commit()

    db.session.add(Item(id = 1, category_id = 1, name = "Item 01 AA", description = "Lorem ipsum dolor sit amet - Item 01 AA", price = 110))
    db.session.add(Item(id = 2, category_id = 1, name = "Item 02 AA", description = "Lorem ipsum dolor sit amet - Item 02 AA", price = 120))
    db.session.add(Item(id = 3, category_id = 2, name = "Item 03 AA", description = "Lorem ipsum dolor sit amet - Item 03 AA", price = 130))
    db.session.commit()

# ----------------------------------------------------------------------------
# category
# ----------------------------------------------------------------------------

class Category(db.Model):
    __tablename__   = 'categories'
    id              = db.Column(db.Integer, primary_key=True)
   #id              = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name            = db.Column(db.String(150), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id':   self.id,
            'name': self.name
        }

    def __repr__(self):
        return 'Category: --> id: {} | name: {}'.format(self.id, self.name)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# ----------------------------------------------------------------------------
# category
# ----------------------------------------------------------------------------

class Item(db.Model):
    __tablename__   = 'items'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    category_id     = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name            = db.Column(db.String(150), unique=True, nullable=False)
    description     = db.Column(db.String, nullable=False)
    price           = db.Column(db.Integer, primary_key=True, nullable=False)

    def format(self):
        return {
            'id':           self.id,
            'category_id':  self.category_id,
            'name':         self.name,
            'description':  self.description,
            'price':        self.price
        }

    def __repr__(self):
        return '<Item {}>'.format(self.name)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# ----------------------------------------------------------------------------

if __name__ == '__main__':
    manager.run()
