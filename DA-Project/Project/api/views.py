from django.shortcuts import render
from order.models import Order, OrderItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.db.models import Q
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework import filters
from shop.models import *
from rest_framework.parsers import FileUploadParser, MultiPartParser
from account.models import *
from news.models import News
# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =  ["transaction_id", "status", "customer__email"]

# @api_view(['GET',])
# def order_list(request):
#     orders = Order.objects.all().order_by("-created_at")
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# @api_view(['GET',])
# def order_detail(request, pk):
#     order = Order.objects.get(id=pk)
#     serializer = OrderSerializer(order, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# def order_update(request, pk):
#     order = Order.objects.get(id=pk)
#     serializer= OrderSerializer(instance=order, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    
    def list(self, request):
        try:
            params = request.query_params['search']
            print(params)
            queryset = Product.objects.filter(Q(version__name__icontains=params)).order_by("-created_at")
        except:
            queryset = Product.objects.all().order_by("-created_at")
        serializer = self.serializer_class(queryset, context={'request':request}, many=True)
        for data in serializer.data:
            id = data["version"]
            try:
                name = Version.objects.get(id=id).name
                data["product_name"] = name
            except:
                pass
        return Response(serializer.data)


class VariationViewSet(viewsets.ModelViewSet):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer

    def create(self, request, *args, **kwargs):
        variation_exist = Variation.objects.filter(product_id=request.data['product']
                                            , color__iexact=request.data['color']
                                            ).exists()
        if variation_exist == False:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Create Success'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request):
        try:
            params = request.query_params['search']
            queryset = Version.objects.filter(Q(name__icontains=params)).order_by("-create_at")
        except:
            queryset = Version.objects.all().order_by("-created_at")
        serializer = self.serializer_class(queryset, context={'request':request}, many=True)
        return Response(serializer.data)

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all().order_by("-create_at")
    serializer_class = SeriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =  ["category__name", "name"]

    def create(self, request, *args, **kwargs):
        data = request.data
        series_exists = Series.objects.filter(category_id=data['category'], name__iexact=data['name']).exists()
        if series_exists == False:
            category = Category.objects.get(id=data['category'])
            series = Series.objects.create(category=category, name=data['name'])
            series.save()
            return Response({'message': 'Create Success'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("-updated_at")
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =  ["name"]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-last_login")
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =  ["email", "full_name", "address"]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = ReviewRating.objects.all().order_by("-updated_at")
    serializer_class = ReviewSerializer

    def update(self, request, *args, **kwargs):
        review = ReviewRating.objects.get(id=request.data['id'])
        review.status = True
        review.save()
        return Response({'message': 'Create Success'}, status=status.HTTP_201_CREATED)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by("-updated_at")
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

# @api_view(['GET',])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     for data in serializer.data:
#         id = data["version"]
#         try:
#             name = Product.objects.get(version__id=id).version.name
#             data["product_name"] = name
#         except:
#             pass
        
#     return Response(serializer.data)

# @api_view(['POST',])
# def product_update(request, pk):
#     products = Product.objects.get(id=pk)
#     serializer = ProductSerializer(instance=products, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)



# @api_view(['GET',])
# def variation_list(request):
#     variations = Variation.objects.all()
#     serializer = VariationSerializer(variations, many=True)
#     return Response(serializer.data)


# @api_view(['POST',])
# def variation_update(request, pk):
#     variation = Variation.objects.get(id=pk)
#     serializer = VariationSerializer(instance=variation, data=request.data)
#     if serializer.is_valid():
#         print("ok")
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         print(serializer.errors)
#         return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET',])
# def series_list(request):
#     series = Series.objects.all()
#     serializer = SeriesSerializer(series, many=True)
#     return Response(serializer.data)


# class OrderSearchList(generics.ListAPIView):
#     queryset = Order.objects.all().order_by("-created_at")
#     serializer_class = OrderSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields =  ["transaction_id", "status", "customer__email"]

