from django.test import Client
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
# Create your tests here.

class LogInView(APITestCase):
    def test_post(self):
        c=Client()
        data = {'id': 'ssar', 'password':1234}
        res = c.post('login/', data)
        self.assertEqual(res.status_code, 200)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)

