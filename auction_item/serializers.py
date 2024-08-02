# auction_items/serializers.py
from rest_framework import serializers
from .models import Item, Auction, Bid, Payment
from user_login.models import User

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class AuctionSerializer(serializers.ModelSerializer):
    current_bid_user = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = '__all__'

    def get_current_bid_user(self, obj):
        if obj.winning_user:
            return UserSerializer(obj.winning_user).data
        return None

class BidSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
