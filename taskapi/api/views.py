from django.shortcuts import render
import redis
from rest_framework.response import Response
from .serializers import VerifySerializers
from rest_framework.views import APIView
import json
from taskapi.celery import verify_user
# Create your views here.
redis_data = redis.Redis(host='localhost', port=6379, db=0)


class VerifyRequest(APIView):
    serializer_class = VerifySerializers
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_input = serializer.data['user']
            stockname = serializer.data['stockname']
            quantity_input = serializer.data['quantity']

            user_str = redis_data.get(user_input)
            user = json.loads(user_str)
            user_credit = user.get('credit')
            user_id = user.get('id')
            
            stock_str = redis_data.get(stockname)
            stock = json.loads(stock_str)
            price_stock = stock.get('price')[0]
            verify_user.delay(user_id,price_stock,quantity_input,user_credit)

            return Response("receive",status=200)
            # if price_stock * quantity_input < user_credit:
            #     return Response("Accept",status=200)
            # else:
            #     return Response({"Deny":"not enough credit"},status=422)
        
        return Response({"Deny":serializer.errors},status=422)
    

