from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Shop, Review_Shop
from base.serializers import ShopSerializer

# Create your views here.
from rest_framework import status


# All Shops
@api_view(['GET'])
def getShops(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    shops = Shop.objects.filter(

        name__icontains=query
        
        ).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(shops, 10)

    try:
        shops = paginator.page(page)
    except PageNotAnInteger:
        shops = paginator.page(1)
    except EmptyPage:
        shops = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ShopSerializer(shops, many=True)
    return Response({'shops': serializer.data, 'page': page, 'pages': paginator.num_pages}) 
    

# getTopShops
@api_view(['GET'])
def getTopShops(request):
    shops = Shop.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data)


# One Shop
@api_view(['GET'])
def getShop(request, pk):
    shop = Shop.objects.get(_id=pk)
    serializer = ShopSerializer(shop, many=False)
    return Response(serializer.data) 


# createShopReview
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createShopReview(request, pk):
    user = request.user
    shop = Shop.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = shop.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Shop already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review_Shop.objects.create(
            user=user,
            shop=shop,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = shop.review.all()
        shop.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        shop.rating = total / len(reviews)
        shop.save()

        return Response('Review Added')