from django.db import models
import uuid
from user_login.models import User, Celebrity

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='items')

class Auction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    status = models.CharField(max_length=10, choices=[('running', 'Running'), ('sold', 'Sold')], default='running')
    winning_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='won_auctions')
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='auctions')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='auctions')

class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='payments')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='payments')
    amount_in_rupees = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50)
