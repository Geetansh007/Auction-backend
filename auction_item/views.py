from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Item, Auction, Bid
from .serializers import ItemSerializer, AuctionSerializer, BidSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_auction(request):
    if not hasattr(request.user, 'celebrity'):
        return Response({'error': 'Only celebrities can create auctions'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.copy()
    data['celebrity'] = str(request.user.celebrity.id)
    data['start_time'] = timezone.now()
    data['end_time'] = timezone.now() + timedelta(hours=24)
    data['current_bid'] = data.get('starting_bid', 0)
    item_data = {
        'name': data.get('item_name'),  
        'image': data.get('item_image'),  
        'celebrity': str(request.user.celebrity.id)
    }
    item_serializer = ItemSerializer(data=item_data)
    if item_serializer.is_valid():
        item = item_serializer.save()
        data['item'] = str(item.id)
    else:
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AuctionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_bid(request, auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
        if auction.status != 'running':
            return Response({'error': 'Auction is not running'}, status=status.HTTP_400_BAD_REQUEST)
        
        if hasattr(request.user, 'celebrity') and auction.celebrity.id == request.user.celebrity.id:
            return Response({'error': 'Celebrities cannot bid on their own auctions'}, status=status.HTTP_403_FORBIDDEN)
        
        bid_amount = request.data.get('bid_amount')
        if bid_amount is None or bid_amount <= auction.current_bid + 1000:
            return Response({'error': 'Bid amount must be at least 1000 more than the current bid'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'auction': str(auction_id),
            'user': str(request.user.id),
            'item': str(auction.item.id),
            'bid_amount': bid_amount
        }
        
        serializer = BidSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            auction.current_bid = bid_amount
            auction.winning_user = request.user
            auction.save()
            return Response({
                'auction': AuctionSerializer(auction).data,
                'bid': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Auction.DoesNotExist:
        return Response({'error': 'Auction not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
