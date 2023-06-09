from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
   path('BuyStock/',views.VerifyRequest.as_view(),name='VerifyRequest'),
]
