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

    # executed after each test
    def tearDown(self):
        pass

# ----------------------------------------------------------------------------
# Create >> Category
# ----------------------------------------------------------------------------

# successful operation

    def test_create_category(self):
        new_category = {'name': 'Category 03 CC'}

        response = self.app.post('/categories', json=new_category)
        data = json.loads(response.data)

        category = (Category.query.filter(Category.name == new_category['name']).first())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])
        (self.assertEqual(data['category']['name'], new_category['name']))

# expected error / s

    def test_create_category_400(self):
        new_category = {'id': '5'}

        response = self.app.post('/categories', json=new_category)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


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
# Update >> Categories
# ----------------------------------------------------------------------------

# successful operation

    def test_update_category(self):

        new_category = {'name': 'Category 02 BB Updated!'}
        response = self.app.patch('/categories/2', json=new_category)
        data = json.loads(response.data)

        category = (Category.query.filter(Category.name == new_category['name']).first())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])
        (self.assertEqual(data['category']['name'], new_category['name']))

# expected error / s

    def test_update_category_400(self):

        new_category = {'name': None}
        response = self.app.patch('/categories/2', json=new_category)
        self.assertEqual(response.status_code, 400)

    def test_update_category_404(self):

        new_category = {'name': 'Category 02 BB Updated!'}
        response = self.app.patch('/categories/999', json=new_category)
        self.assertEqual(response.status_code, 404)

# ----------------------------------------------------------------------------
# Delete >> Category
# ----------------------------------------------------------------------------

# successful operation

    def test_delete_category(self):

        response = self.app.delete('/categories/3')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 3)

# expected error / s

    def test_delete_category_404(self):

        response = self.app.delete('/categories/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

# ----------------------------------------------------------------------------
# Create >> Item
# ----------------------------------------------------------------------------

# successful operation

    def test_create_item(self):

        new_item = {
            'category_id': 2,
            'name': 'Item 04 - name DD',
            'description': 'Lorem ipsum dolor sit amet - description of Item 04 DD',
            'price': 140
        }

        response = self.app.post('/items', json=new_item)
        data = json.loads(response.data)

        item = (Item.query.filter(Item.name == new_item['name']).first())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['item'])
        (self.assertEqual(data['item']['name'], new_item['name']))

# expected error / s

    def test_create_item_400(self):

        new_item = {
            'category_id': 2,
            'name': None,
            'description': 'Lorem ipsum dolor sit amet - description of Item 04 DD',
            'price': 130
        }

        response = self.app.post('/items', json=new_item)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


# ----------------------------------------------------------------------------
# Update >> Item
# ----------------------------------------------------------------------------

# successful operation

    def test_update_item(self):

        new_item = {
            'category_id': 2,
            'name': 'Item 04 - name DD NEW',
            'description': 'Lorem ipsum dolor sit amet - description of Item 04 DD',
            'price': 140
        }

        response = self.app.patch('/items/4', json=new_item)
        data = json.loads(response.data)

        item = (Item.query.filter(Item.name == new_item['name']).first())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['item'])
        (self.assertEqual(data['item']['name'], new_item['name']))

# expected error / s

    def test_update_item_400(self):

        new_item = {
            'category_id': None,
            'name': 'Item 04 - name DD NEW',
            'description': 'Lorem ipsum dolor sit amet - description of Item 04 DD',
            'price': 140
        }

        response = self.app.patch('/items/4', json=new_item)
        self.assertEqual(response.status_code, 400)

    def test_update_item_404(self):

        new_item = {
            'category_id': None,
            'name': 'Item 04 - name DD NEW',
            'description': 'Lorem ipsum dolor sit amet - description of Item 04 DD',
            'price': 140
        }

        response = self.app.patch('/items/999', json=new_item)
        self.assertEqual(response.status_code, 404)

# ----------------------------------------------------------------------------
# Delete >> Item
# ----------------------------------------------------------------------------

# successful operation

    def test_delete_itemAA(self):

        response = self.app.delete('/items/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

# expected error / s

    def test_delete_item_404(self):

        response = self.app.delete('/items/999')
        self.assertEqual(response.status_code, 404)


# ----------------------------------------------------------------------------
# Make the tests executable
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
