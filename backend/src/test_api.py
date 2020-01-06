import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api import app
from manage import Category, Item, db_drop_and_create_all


class ItemTestCase(unittest.TestCase):

    def setUp(self):

        app.config.from_object('config')
        self.app = app.test_client()

        #db_drop_and_create_all()

    # executed after each test
    def tearDown(self):
        pass

# ----------------------------------------------------------------------------
# Create >> Category
# ----------------------------------------------------------------------------

    # successful operation
    def test_create_question(self):
        new_category = {'name':'Category 02 BB'}

        response = self.app.post('/categories', json = new_category)
        data = json.loads(response.data)

        category = (Category.query.filter(Category.name == new_category['name']).first())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])
        (self.assertEqual(data['category']['name'],new_category['name']))

# ----------------------------------------------------------------------------
# Read >> All Categories
# ----------------------------------------------------------------------------
# successful operation

    def test_get_categories(self):

        response = self.app.get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

# expected error / s
# NONE
# ----------------------------------------------------------------------------









# ----------------------------------------------------------------------------
# Make the tests executable
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
