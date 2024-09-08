from rest_framework import generics, permissions, filters

from core.paginate import ExtraSmallResultsSetPagination
from .models import Food, FoodFavorite, Vitamin, VitaminFavorite
from .serializers import (FoodFavoriteSerializer, FoodSerializers, VitaminFavoriteSerializer, 
                          VitaminSerializers, FoodFavoriteListSerializer, VitaminFavoriteListSerializer)

class FoodListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = FoodSerializers
    queryset = Food.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'scientificName', 'vitamins__name']
    

class FoodDetailView(generics.RetrieveAPIView):
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
    

class VitaminDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = VitaminSerializers
    queryset = Vitamin.objects.all()


class FoodFavoriteCreateView(generics.CreateAPIView):
    serializer_class = FoodFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class FoodFavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = FoodFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        food = generics.get_object_or_404(Food, id=self.kwargs['food_id'])
        return generics.get_object_or_404(
            FoodFavorite,
            food=food,
            user_profile=self.request.user.profile
        )


class FoodFavoriteListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = FoodFavoriteListSerializer
    queryset = FoodFavorite.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['food__name',]

    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user.profile)


class VitaminFavoriteListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = VitaminFavoriteListSerializer
    queryset = VitaminFavorite.objects.all()
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['vitamin__name',]

    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user.profile)

class VitaminFavoriteCreateView(generics.CreateAPIView):
    serializer_class = VitaminFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class VitaminFavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = VitaminFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        vitamin = generics.get_object_or_404(Vitamin, id=self.kwargs['vitamin_id'])
        return generics.get_object_or_404(
            VitaminFavorite,
            vitamin=vitamin,
            user_profile=self.request.user.profile
        )