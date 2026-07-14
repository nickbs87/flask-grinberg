from selenium import webdriver
import unittest
from app import create_app, db, fake
from app.models import User, Role
import threading
from selenium.webdriver.common.by import By
import re
import os
from werkzeug.serving import make_server

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        try:
            cls.client = webdriver.Chrome(options=options)
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            #suppress loggin to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            # create the database and populate with some fake data
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # add an administrator user
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john',
                         password='cat',
                         role=admin_role,
                         confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # start the Flask server in a thread
            os.environ['FLASK_RUN_FROM_CLI'] = 'false'
            cls.server = make_server('127.0.0.1', 5000, cls.app)
            cls.server_thread = threading.Thread(target=cls.server.serve_forever)
            cls.server_thread.start()


    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the Flask server and the browser
            cls.server.shutdown()
            cls.client.quit()
            cls.server_thread.join()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger', self.client.page_source))

        # navigate to login page
        self.client.find_element(By.LINK_TEXT, 'Log In').click()
        self.assertIn('<h1>Login</h1>', self.client.page_source)

        # log in
        self.client.find_element(By.NAME, 'email').send_keys('john@example.com')
        self.client.find_element(By.NAME, 'password').send_keys('cat')
        self.client.find_element(By.NAME, 'submit').click()
        self.assertTrue(re.search('Hello,\s+john', self.client.page_source))

        # navigate to the user's profile page
        self.client.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn('<h1>john</h1>', self.client.page_source)
