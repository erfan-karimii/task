from django.test import SimpleTestCase , Client
from django.urls import reverse
from unittest.mock import patch  ,MagicMock
from taskapi.celery import verify_user,TimeoutException
import random
import json

# Create your tests here.


class TestViewVerifyRequest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:VerifyRequest')

    @patch('taskapi.celery.verify_user.delay', return_value=None)
    def test_view_post_right_data(self,mock_delay):
        data = {
            "user": "user1",
            "stockname": "stock1",
            "quantity": "23"
            }
        response =  self.client.post(self.url,data=data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, 'receive')

    @patch('taskapi.celery.verify_user.delay', return_value=None)
    def test_view_post_negetive_quantity(self,mock_delay):
        data = {
            "user": "user1",
            "stockname": "stock1",
            "quantity": "-10"
            }
        response =  self.client.post(self.url,data=data)
        self.assertEqual(response.status_code,422) #422 Unprocessable Content
        
    @patch('taskapi.celery.verify_user.delay', return_value=None)
    def test_view_post_wrong_data(self,mock_delay):
        data = {
            "user": "user3",
            "stockname": "stock1",
            "quantity": "10"
            }
        response =  self.client.post(self.url,data=data)
        self.assertEqual(response.status_code,422) #422 Unprocessable Content


class TestVerifyUserTask(SimpleTestCase):
    @patch('random.randint', return_value=3)
    def test_verify_user_task_under_alarm_time_right_data(self,mock_sleep):
        data = {
            'user_id':1,
            'price_stock':200,
            'quantity_input':2,
            'user_credit':20000
            }
        result = verify_user(**data)
        self.assertEqual(result,{'Accept': ''})
    

    @patch('random.randint', return_value=5)
    @patch('taskapi.celery.time_out', return_value=3)
    def test_verify_user_task_upper_alarm_time_right_data(self,mock_sleep,mock_time_out):
        data = {
            'user_id':1,
            'price_stock':200,
            'quantity_input':2,
            'user_credit':20000
            }
        with self.assertRaises(TimeoutException):
            result = verify_user(**data)
            
