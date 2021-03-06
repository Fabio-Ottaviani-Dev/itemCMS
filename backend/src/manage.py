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

    db.session.add(Category(name="Category 01 AA"))
    db.session.add(Category(name="Category 02 BB"))
    db.session.commit()

    db.session.add(Item(category_id=1, name="Item 01 - name AA", description="Lorem ipsum dolor sit amet - description of Item 01 AA", price=110))
    db.session.add(Item(category_id=1, name="Item 02 - name BB", description="Lorem ipsum dolor sit amet - description of Item 02 BB", price=120))
    db.session.add(Item(category_id=2, name="Item 03 - name CC", description="Lorem ipsum dolor sit amet - description of Item 03 CC", price=130))
    db.session.commit()

# ----------------------------------------------------------------------------
# Category
# ----------------------------------------------------------------------------


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

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

    # def __repr__(self):
    #     return 'Category: --> id: {} | name: {}'.format(self.id, self.name)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# ----------------------------------------------------------------------------
# Item
# ----------------------------------------------------------------------------


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship("Category", backref="items")
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

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
            'id':           self.id,
            'category':     {'id': self.category.id, 'name': self.category.name},
            'name':         self.name,
            'description':  self.description,
            'price':        self.price
        }

    # def __repr__(self):
    #     return '<Item {}>'.format(self.name)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# ----------------------------------------------------------------------------


if __name__ == '__main__':
    manager.run()
