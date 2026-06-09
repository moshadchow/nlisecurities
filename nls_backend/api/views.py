from django.shortcuts import render
from .models import About,AboutImage,Sliders,Services,Products,Features,Offers,BoardMembers,\
    Events,Clients,Faqs,PrivacyPolicy,ManComs,Teams,IPO_Offer,MarketNews,Branch,\
    Category,Research


from .serializers import AboutSerializer,AboutImageSerializer, ResearchFileSerializer,SlidersSerializer,\
    ServicesSerializer,ProductsSerializer,FeaturesSerializer,OffersSerializer,\
    BoardMembersSerializer,EventsSerializer,ClientsSerializer,FaqsSerializer,\
    ContactSerializer, PrivacyPolicySerializer,ManComsSerializer,TeamsSerializer,\
    IPO_OfferSerializer,MarketNewsSerializer,BranchSerializer,\
    CategorySerializer,ResearchFileSerializer

from django.db import connections
from django.http import JsonResponse
from collections import defaultdict
# from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def Abouts(request):
    about = About.objects.first()  # safer
    if not about:
        return Response(
            {"error": "No Privacy Policy found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serialized_data = AboutSerializer(about)
    return Response(serialized_data.data)

@api_view(['GET'])
def AboutImages(request,pk=None):
    if pk is not None:
        try:
            data = AboutImage.objects.get(pk=pk)
            serializedData = AboutImageSerializer(data)
            return Response(serializedData.data)
        except Services.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:    
        data = AboutImage.objects.all()
        serializedData = AboutImageSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def Sliders_view(request):
    data = Sliders.objects.all()
    serializedData = SlidersSerializer(data, many= True )
    return Response(serializedData.data)

@api_view(['GET'])
def Services_view(request,pk=None):
    if pk is not None:
        try:
         data = Services.objects.get(pk=pk)
         serializedData = ServicesSerializer(data)
        except Services.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = Services.objects.all()
        serializedData = ServicesSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def Products_view(request,pk=None):
    if pk is not None:
        try:
         data = Products.objects.get(pk=pk)
         serializedData = ProductsSerializer(data)
        except Products.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = Products.objects.all()
        serializedData = ProductsSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def Features_view(request,pk=None):
    if pk is not None:
        try:
         data = Features.objects.get(pk=pk)
         serializedData = FeaturesSerializer(data)
        except Features.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = Features.objects.all()
        serializedData = FeaturesSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def Offers_view(request,pk=None):
    if pk is not None:
        try:
         data = Offers.objects.get(pk=pk)
         serializedData = OffersSerializer(data)
        except Offers.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = Offers.objects.all()
        serializedData = OffersSerializer(data, many=True)
    
    return Response(serializedData.data)


@api_view(['GET'])
def BoardMembers_view(request,pk=None):
    if pk is not None:
        try:
         data = BoardMembers.objects.get(pk=pk)
         serializedData = BoardMembersSerializer(data)
        except BoardMembers.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = BoardMembers.objects.all()
        serializedData = BoardMembersSerializer(data, many=True)
    
    return Response(serializedData.data)

@api_view(['GET'])
def ManComs_view(request,pk=None):
    if pk is not None:
        try:
         data = ManComs_view.objects.get(pk=pk)
         serializedData = ManComsSerializer(data)
        except ManComs.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = ManComs.objects.all()
        serializedData = ManComsSerializer(data, many=True)
    
    return Response(serializedData.data)

@api_view(['GET'])
def Teams_view(request):
    data = Teams.objects.all()
    serializedData = TeamsSerializer(data, many= True )
    return Response(serializedData.data)

@api_view(['GET'])
def Events_view(request,pk=None):
    if pk is not None:
        try:
         data = Events.objects.get(pk=pk)
         serializedData = EventsSerializer(data)
        except Events.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = Events.objects.all()
        serializedData = EventsSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def News_view(request, pk=None):
    try:
        if pk is not None:
            data = MarketNews.objects.filter(market=pk)
            if not data.exists():
                return Response(
                    {"detail": "No news found for this market."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializedData = MarketNewsSerializer(data, many=True)

        else:
            data = MarketNews.objects.all()
            serializedData = MarketNewsSerializer(data, many=True)

        return Response(serializedData.data)

    except Exception as e:
        # Catch any unexpected error
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def Clients_view(request):
    data = Clients.objects.all()
    serializedData = ClientsSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def Faqs_view(request):
    data = Faqs.objects.all()
    serializedData = FaqsSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['POST'])
def Contact_view(request):
    data =  request.data
    serializedData = ContactSerializer(data=data)
    if serializedData.is_valid():
        serializedData.save()
        return Response(serializedData.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializedData.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Policy_view(request):
    policy = PrivacyPolicy.objects.first()  # safer
    if not policy:
        return Response(
            {"error": "No Privacy Policy found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serialized_data = PrivacyPolicySerializer(policy)
    return Response(serialized_data.data)


@api_view(['GET'])
def IPO_view(request):
    data = IPO_Offer.objects.all()
    serializedData = IPO_OfferSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
def Top_share_price_by(request, pk=None):

    db = connections['default']

    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM api_share_prices where market=%s", [pk])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    if not rows:
        return Response([])

    # Convert to list of dicts (like model instances -> serializer)
    data = []
    for row in rows:
        item = dict(zip(columns, row))
        data.append(item)

    # Apply sorting based on pk
    if pk == "Gainer":
        data.sort(
            key=lambda x: (x["change_val"] / x["ycp"]) if x["ycp"] else 0,
            reverse=True
        )
    elif pk == "Loser":
        data.sort(
            key=lambda x: (x["change_val"] / x["ycp"]) if x["ycp"] else 0
        )
    elif pk == "Value":
        data.sort(
            key=lambda x: x["value_mn"],
            reverse=True
        )
    elif pk == "Volume":
        data.sort(
            key=lambda x: x["volume"],
            reverse=True
        )

    # Send back only top 10
    return Response(data)


@api_view(['GET'])
def Branch_view(request,pk=None):
    if pk is not None:
        try:
         data = Branch.objects.filter(category=pk)
         serializedData = BranchSerializer(data, many=True)
        except Branch.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data = Branch.objects.all()
        serializedData = BranchSerializer(data, many=True)
    return Response(serializedData.data)

@api_view(["GET"])
def research_grouped_view(request, pk=None):
    if pk is None:
        return Response({"error": "Category ID is required."}, status=400)

    # Filter researches by category id
    researches = Research.objects.filter(category=pk)

    if not researches.exists():
        return Response({"error": "No research found for this category."}, status=404)

    serializer = ResearchFileSerializer(
        researches, many=True, context={"request": request}
    )

    response_data = {
        "category": pk,
        "name": researches.first().title,  # assuming category has name field
        "files": serializer.data
    }

    return Response(response_data)

@api_view(["GET"])
def category_list(request):
    categories = Category.objects.prefetch_related("files").all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def market_info(request, pk=None):
    db = connections['default']

    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM api_market_info WHERE market = %s LIMIT 1",
            [pk]
        )
        row = cursor.fetchone()

        if not row:
            return JsonResponse({"error": "No data found"}, status=404)

        columns = [col[0] for col in cursor.description]
        data = dict(zip(columns, row))

    return JsonResponse(data, safe=False)

@api_view(["GET"])
def minutes_index(request, pk=None):
    db = connections['default']

    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM api_minute_data WHERE market = %s",
            [pk]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse({"error": "No data found"}, status=404)

    # Build the grouped structure
    result = {}
    for id,market, name, time, index_value in rows:
        if name not in result:
            result[name] = []

        result[name].append({
            "time": time,
            "index": index_value
        })

    return JsonResponse(result, safe=False)

@api_view(["GET"])
def market_index(request, pk=None):
    db = connections['default']

    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM api_market_index WHERE market = %s",
            [pk]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse({"error": "No data found"}, status=404)

    # Build the grouped structure
    result = []
    for id,market, name, value, change, percent, arrow in rows:
        result.append({
            "index": name,
            "value": value,
            "change":change,
            "percent":percent,
            "arrow":arrow
        })

    return JsonResponse(result, safe=False)

@api_view(["GET"])
def sector_wise_inst(request):
    db = connections['default']

    with db.cursor() as cursor:
        cursor.execute("SELECT id, sector_id, sector, symbol FROM api_sector_inst")
        rows = cursor.fetchall()

    if not rows:
        return JsonResponse({"error": "No data found"}, status=404)

    result = {}

    for id, sector_id, sector, symbol in rows:
        if sector_id not in result:
            result[sector_id] = {
                "sector_id": sector_id,
                "sector": sector,
                "symbols": []
            }

        result[sector_id]["symbols"].append(symbol)

    # You can return the dict or list depending on your API preference
    return JsonResponse(list(result.values()), safe=False)

@api_view(["GET"])
def ticker_price(request, pk = None):
    db = connections['default']

    with db.cursor() as cursor:
        cursor.execute(
           "SELECT id, market, inst, price, change_val, percent, arrow "
            "FROM api_ticker_price WHERE market = %s"
           ,[pk])
        rows = cursor.fetchall()

    if not rows:
        return JsonResponse({"error": "No data found"}, status=404)

    result = []

    for row in rows:
        _id, market, inst, price, change, percent, arrow = row

        result.append({
            "id": _id,
            "market": market,
            "inst": inst,
            "price": float(price),
            "change": float(change),
            "percent": float(percent),
            "arrow": arrow
        })

    # You can return the dict or list depending on your API preference
    return JsonResponse(result, safe=False)