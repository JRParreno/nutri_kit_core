from rest_framework import generics, permissions, filters

from core.paginate import ExtraSmallResultsSetPagination
from .models import Food, Vitamin
from .serializers import FoodSerializers, VitaminSerializers

class FoodListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = FoodSerializers
    queryset = Food.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'scientificName', 'vitamins__name']
    

class FoodDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = FoodSerializers
    queryset = Food.objects.all()
    

class VitaminListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = VitaminSerializers
    queryset = Vitamin.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    

class VitaminDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = VitaminSerializers
    queryset = Vitamin.objects.all()