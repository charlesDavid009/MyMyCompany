from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Items, Viewers, PostLikes, SubViewers

# Create your tests here.

User = get_user_model()

class BlogTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cfe", password="somepassword")
        Items.objects.create(title="Great Minds",
                                        details ="Welcome to my channel",
                                        owner=self.user
                                        )
        Items.objects.create(title="Great Minds",
                                        details="Welcome to my channel",
                                        owner=self.user
                                        )
        Items.objects.create(title="Great Minds",
                                        details="Welcome to my channel",
                                        owner=self.user
                                        )

    def test_create_blog(self):
        blog_obj = Items.objects.create(title="Great Minds", details ="Welcome to my channel", owner=self.user)
        self.assertEqual(blog_obj.id, 4)
        self.assertEqual(blog_obj.owner, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepassword")
        return client

    def test_item_list(self):
        client = self.get_client()
        response = client.get('/Blog/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        print(response.json())

    def test_item_details(self):
        client = self.get_client()
        response = client.get('/Blog/1/details/')
        self.assertEqual(response.status_code, 200)
        print(response.json())




