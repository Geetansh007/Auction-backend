from django.urls import path
from .views import create_auction, place_bid

urlpatterns = [
    path('create_auction/', create_auction, name='create-auction'),
    path('place_bid/<uuid:auction_id>/', place_bid, name='place-bid'),
]
